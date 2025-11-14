@echo off
REM AARI Complete Setup Script for Windows
REM This script sets up everything needed to run AARI

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo   AARI Voice Assistant - Complete Setup
echo ===============================================
echo.

REM Get current directory
set AARI_ROOT=%~dp0
set BACKEND_DIR=%AARI_ROOT%backend
set ANDROID_DIR=%AARI_ROOT%android

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Download from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/5] Setting up Python virtual environment...
cd /d "%BACKEND_DIR%"
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo [3/5] Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo WARNING: Some dependencies failed to install
) else (
    echo ✓ All dependencies installed
)

echo.
echo [4/5] Downloading spaCy model...
python -m spacy download en_core_web_sm --quiet
echo ✓ spaCy model ready

echo.
echo [5/5] Creating .env file template...
if not exist "%BACKEND_DIR%\.env" (
    (
        echo GOOGLE_API_KEY=your_key_here
        echo SENDER_EMAIL=your_email@gmail.com
        echo SENDER_PASSWORD=your_app_password
    ) > "%BACKEND_DIR%\.env"
    echo ✓ .env template created - Please update with your keys
    echo   Edit: %BACKEND_DIR%\.env
) else (
    echo ✓ .env file already exists
)

echo.
echo ===============================================
echo ✓ SETUP COMPLETE!
echo ===============================================
echo.
echo NEXT STEPS:
echo.
echo 1. Edit API keys in: %BACKEND_DIR%\.env
echo    - GOOGLE_API_KEY: Get from https://makersuite.google.com/app/apikey
echo    - SENDER_EMAIL: Your Gmail address
echo    - SENDER_PASSWORD: Gmail app password
echo.
echo 2. Start backend server:
echo    - Run: START_AARI.bat
echo    - OR: cd backend && venv\Scripts\activate.bat && python app.py
echo.
echo 3. Build Android APK:
echo    - Open %ANDROID_DIR% in Android Studio
echo    - Update IP in ApiClient.java
echo    - Build → Build APK(s)
echo    - Install on your Android device
echo.
echo 4. Configure Android app:
echo    - Grant all permissions
echo    - Enable Background Mode in Settings
echo    - Test: Say "Hey AARI, what time is it?"
echo.
echo ===============================================
echo.
pause
