@echo off
REM AARI - Complete Setup Script for Windows

echo.
echo =========================================
echo   AARI Voice Assistant - Setup
echo =========================================
echo.

REM Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo [1/5] Cloning repository...
git clone https://github.com/abneeshsingh21/-aari-backend.git
cd -aari-backend

echo [2/5] Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo [3/5] Creating .env file...
if not exist .env (
    echo GOOGLE_API_KEY=your_key_here > .env
    echo SENDER_EMAIL=your_email@gmail.com >> .env
    echo SENDER_PASSWORD=your_app_password >> .env
    echo Please edit .env with your API keys
)

cd ..

echo [4/5] Setting up Frontend...
cd VoiceAssistantApp
call npm install

cd ..

echo [5/5] Setup Complete!
echo.
echo =========================================
echo   Setup Completed Successfully!
echo =========================================
echo.
echo Next Steps:
echo 1. Configure backend/.env with your API keys
echo 2. Run backend: cd backend ^& venv\Scripts\activate.bat ^& python app.py
echo 3. Run frontend: cd VoiceAssistantApp ^& npm start
echo.
pause
