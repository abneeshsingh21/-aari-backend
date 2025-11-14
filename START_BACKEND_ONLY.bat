@echo off
REM Quick Start Script for AARI
REM Runs: Backend server + Desktop app

setlocal enabledelayedexpansion

set BACKEND_DIR=%~dp0backend

echo.
echo ===============================================
echo   AARI Voice Assistant - Starting...
echo ===============================================
echo.

REM Start Python backend server
cd /d "%BACKEND_DIR%"

echo Starting backend server...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env with your API keys first
    echo.
    pause
    exit /b 1
)

echo.
echo Backend will start on: http://0.0.0.0:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run backend
python app.py
