@echo off
REM AARI One-Click Setup & Launch
REM This script clones, sets up, and runs AARI with one command

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════╗
echo ║   AARI Voice Assistant - One Click Setup    ║
echo ╚══════════════════════════════════════════════╝
echo.

REM Check if already in project
if exist "backend" if exist "VoiceAssistantApp" (
    echo ✓ Already in AARI project directory
    goto skip_clone
)

REM Clone repository
echo [1/4] Cloning repository...
git clone https://github.com/abneeshsingh21/-aari-backend.git aari-app
if !errorlevel! neq 0 (
    echo ✗ Failed to clone repository
    pause
    exit /b 1
)
cd aari-app

:skip_clone

echo ✓ Repository ready
echo.
echo [2/4] Installing dependencies...
cd VoiceAssistantApp
call npm install --legacy-peer-deps > nul 2>&1
if !errorlevel! neq 0 (
    echo ⚠ Some warnings during install, continuing...
)
echo ✓ Dependencies installed
cd ..

echo.
echo [3/4] Verifying backend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://aari-backend-3rs9.onrender.com/api/health' -ErrorAction Stop; Write-Host '✓ Backend is healthy' } catch { Write-Host '⚠ Backend may be starting...' }"

echo.
echo [4/4] Starting services...
echo.
echo ╔══════════════════════════════════════════════╗
echo ║           Services Starting                  ║
echo ╠══════════════════════════════════════════════╣
echo ║ Backend:  https://aari-backend-3rs9.onrender.com
echo ║ Frontend: http://localhost:8081              ║
echo ║ Expo: Starting...                            ║
echo ║                                              ║
echo ║ Android: Scan QR code with Expo Go          ║
echo ║ Desktop: python desktop/run_desktop.py      ║
echo ╚══════════════════════════════════════════════╝
echo.

cd VoiceAssistantApp
call npx expo start

pause
