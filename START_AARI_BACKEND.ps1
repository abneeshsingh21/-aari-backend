# AARI Backend Auto-Start Script
# This script starts the AARI backend server automatically

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      AARI Voice Assistant - Backend Server Launcher           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Set paths
$BackendPath = "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"
$PythonExe = "C:/Program Files/Python312/python.exe"

# Check if backend folder exists
if (-not (Test-Path $BackendPath)) {
    Write-Host "❌ ERROR: Backend folder not found at $BackendPath" -ForegroundColor Red
    Write-Host "Please ensure AARI is installed correctly." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is installed
if (-not (Test-Path $PythonExe)) {
    Write-Host "❌ ERROR: Python 3.12 not found at $PythonExe" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Prerequisites verified" -ForegroundColor Green
Write-Host ""

# Navigate to backend
Write-Host "📁 Changing to backend directory..." -ForegroundColor Cyan
Set-Location $BackendPath
Write-Host "📍 Current location: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "⚠️  Virtual environment not found!" -ForegroundColor Yellow
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    & $PythonExe -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Check if requirements are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
$RequirementsFile = "$BackendPath\requirements.txt"
if (Test-Path $RequirementsFile) {
    & $PythonExe -c "import flask; import google.generativeai; print('✓ Dependencies found')" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Missing dependencies! Installing..." -ForegroundColor Yellow
        & $PythonExe -m pip install -r requirements.txt --quiet
        Write-Host "✓ Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "✓ All dependencies present" -ForegroundColor Green
    }
}
Write-Host ""

# Check for .env file
Write-Host "🔐 Checking configuration..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Create a .env file with the following content:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "GOOGLE_API_KEY=your_google_generative_ai_key_here" -ForegroundColor Gray
    Write-Host "SENDER_EMAIL=your_email@gmail.com" -ForegroundColor Gray
    Write-Host "SENDER_PASSWORD=your_app_password_here" -ForegroundColor Gray
    Write-Host ""
    Write-Host "You can get API keys from:" -ForegroundColor Yellow
    Write-Host "  - Google API: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
    Write-Host "  - Gmail App Password: https://myaccount.google.com/apppasswords" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to continue anyway (some features may not work)"
} else {
    Write-Host "✓ Configuration file found" -ForegroundColor Green
}
Write-Host ""

# Start the server
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  🚀 Starting AARI Backend Server...                           ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📡 Server will start on: http://localhost:5000" -ForegroundColor Cyan
Write-Host "📡 API Access:          http://192.168.x.x:5000 (replace with your IP)" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏹️  Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

# Start the Flask app
$env:PYTHONUNBUFFERED = 1
& $PythonExe app.py

# Handle script completion
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "Backend server stopped" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to exit"
