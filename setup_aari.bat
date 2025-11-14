@echo off
REM AARI Voice Assistant - Complete Startup Script
REM This script sets up and starts the entire AARI system

echo.
echo ========================================
echo   AARI Voice Assistant - Full Setup
echo ========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo OK - Python found
echo.

REM Navigate to backend
cd /d "%~dp0VoiceAssistant\backend"

echo.
echo ========================================
echo Step 1: Installing Python Dependencies
echo ========================================
echo.
pip install -r requirements.txt --user

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Downloading spaCy Model
echo ========================================
echo.
python -m spacy download en_core_web_sm

if errorlevel 1 (
    echo ERROR: Failed to download spaCy model
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 3: Verifying Configuration
echo ========================================
echo.

REM Check .env file
if not exist ".env" (
    echo ERROR: .env file not found
    echo Please create .env file with required credentials
    pause
    exit /b 1
)

echo OK - .env configuration found

echo.
echo ========================================
echo Step 4: Running API Tests
echo ========================================
echo.
python test_api.py

if errorlevel 1 (
    echo WARNING: Some API tests failed
    echo However, the system may still be functional
    pause
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo AARI is now ready to use!
echo.
echo Available commands:
echo   - Run Backend Server: python app.py
echo   - Run Desktop GUI: python ..\desktop\desktop_assistant.py
echo   - Run API Tests: python test_api.py
echo.
echo Press any key to exit...
pause
