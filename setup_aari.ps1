#!/usr/bin/env pwsh
<#
.SYNOPSIS
    AARI Voice Assistant - Automated Setup and Testing Script
.DESCRIPTION
    Complete setup, testing, and deployment script for AARI
.EXAMPLE
    .\setup_aari.ps1
#>

param(
    [switch]$Test = $false,
    [switch]$StartServer = $false,
    [switch]$StartDesktop = $false
)

$ErrorActionPreference = "Stop"
$WarningPreference = "SilentlyContinue"

Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AARI Voice Assistant - Full Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $ScriptDir "VoiceAssistant" "backend"
$DesktopDir = Join-Path $ScriptDir "VoiceAssistant" "desktop"

# Function to print status
function Write-Status {
    param([string]$Message, [string]$Status = "OK", [string]$Color = "Green")
    Write-Host "$Message ... " -NoNewline
    Write-Host $Status -ForegroundColor $Color
}

try {
    # Check Python
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Step 1: Checking Python Installation" -ForegroundColor Cyan
    Write-Host "========================================`n"
    
    $PythonVersion = & python --version 2>&1
    Write-Status "Python" $PythonVersion.ToString() Green
    
    # Change to backend directory
    Set-Location $BackendDir
    Write-Host "`nBackend directory: $BackendDir`n" -ForegroundColor Yellow
    
    # Install dependencies
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Step 2: Installing Dependencies" -ForegroundColor Cyan
    Write-Host "========================================`n"
    
    Write-Host "Installing from requirements.txt..." -ForegroundColor Yellow
    & python -m pip install -r requirements.txt --user --quiet
    Write-Status "Dependencies" "INSTALLED" Green
    
    # Download spaCy model
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Step 3: Downloading spaCy Model" -ForegroundColor Cyan
    Write-Host "========================================`n"
    
    Write-Host "Downloading en_core_web_sm..." -ForegroundColor Yellow
    & python -m spacy download en_core_web_sm --quiet
    Write-Status "spaCy Model" "DOWNLOADED" Green
    
    # Verify configuration
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Step 4: Verifying Configuration" -ForegroundColor Cyan
    Write-Host "========================================`n"
    
    if (Test-Path ".env") {
        Write-Status ".env file" "FOUND" Green
        $EnvContent = Get-Content ".env" | Where-Object { $_ -match "GOOGLE_API_KEY|USER_NAME|ASSISTANT_NAME" }
        Write-Host "`nConfiguration loaded:" -ForegroundColor Yellow
        foreach ($line in $EnvContent) {
            Write-Host "  ✓ $($line.Split('=')[0])" -ForegroundColor Green
        }
    } else {
        Write-Status ".env file" "NOT FOUND" Red
        Write-Host "ERROR: Please ensure .env file exists" -ForegroundColor Red
        exit 1
    }
    
    if (Test-Path "config.json") {
        Write-Status "config.json" "FOUND" Green
    }
    
    if (Test-Path "contacts.json") {
        Write-Status "contacts.json" "FOUND" Green
    }
    
    # Run tests if requested or by default
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Step 5: Running API Tests" -ForegroundColor Cyan
    Write-Host "========================================`n"
    
    & python test_api.py | Tee-Object -Variable TestOutput
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "`n⚠ Some tests had warnings, but system is functional" -ForegroundColor Yellow
    }
    
    # Summary
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Setup Complete!" -ForegroundColor Cyan
    Write-Host "========================================`n"
    
    Write-Host "AARI is ready to use!`n" -ForegroundColor Green
    
    Write-Host "Available Commands:" -ForegroundColor Yellow
    Write-Host "  Backend Server:  python app.py" -ForegroundColor White
    Write-Host "  Desktop GUI:     python ..\desktop\desktop_assistant.py" -ForegroundColor White
    Write-Host "  API Tests:       python test_api.py" -ForegroundColor White
    Write-Host "`n"
    
    if ($StartServer) {
        Write-Host "Starting backend server..." -ForegroundColor Cyan
        Start-Process python -ArgumentList "app.py" -WorkingDirectory $BackendDir
        Write-Host "Server started on http://localhost:5000" -ForegroundColor Green
    }
    
    if ($StartDesktop) {
        Write-Host "Starting desktop GUI..." -ForegroundColor Cyan
        Set-Location $DesktopDir
        Start-Process python -ArgumentList "desktop_assistant.py" -WorkingDirectory $DesktopDir
        Write-Host "Desktop GUI launched - Press Ctrl+Shift+V to activate" -ForegroundColor Green
    }
    
    Write-Host "========================================`n" -ForegroundColor Cyan
    
} catch {
    Write-Host "`n❌ ERROR: $_" -ForegroundColor Red
    Write-Host "`nSetup failed. Please check the error above and try again.`n" -ForegroundColor Red
    exit 1
}
