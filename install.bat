INSTALLATION SCRIPT FOR WINDOWS
================================

@echo off
echo ===============================================
echo AI VOICE ASSISTANT - Installation Script
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Navigate to backend folder
cd /d "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

REM Create virtual environment
echo.
echo [1/5] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call .\venv\Scripts\Activate.ps1

REM Install dependencies
echo [3/5] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Download spaCy model
echo [4/5] Downloading spaCy language model...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo WARNING: spaCy model download failed, but continuing...
)

REM Copy .env file
echo [5/5] Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your API keys:
    echo   - GOOGLE_API_KEY
    echo   - SENDER_EMAIL
    echo   - SENDER_PASSWORD
    pause
)

echo.
echo ===============================================
echo Installation Complete!
echo ===============================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: python app.py (to start backend server)
echo 3. In another terminal, run: python desktop\desktop_assistant.py
echo.
echo For more information, see README.md
echo ===============================================
pause
