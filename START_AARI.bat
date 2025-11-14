@echo off
REM AARI Voice Assistant - Start Both Backend and Desktop
REM Fixed version using dedicated launchers

echo ====================================================================
echo          AARI Voice Assistant - Starting Services
echo ====================================================================
echo.

REM Check Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ and add to PATH
    pause
    exit /b 1
)

REM Start Backend Service
echo [1/2] Starting AARI Backend Service...
echo.
start "AARI Backend" python.exe "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend\run_backend.py"
echo ✓ Backend service started in separate window
echo.

REM Wait for backend to initialize
timeout /t 3 /nobreak

REM Start Desktop GUI
echo [2/2] Starting AARI Desktop GUI...
echo.
start "AARI Desktop" python.exe "c:\Users\lenovo\Desktop\aari\VoiceAssistant\desktop\run_desktop.py"
echo ✓ Desktop GUI launched
echo.

echo ====================================================================
echo          Services Starting...
echo ====================================================================
echo.
echo Backend:  http://localhost:5000
echo Desktop:  Starting up...
echo.
echo Press Ctrl+Shift+V in the desktop window to start talking!
echo.
echo To stop services, close both windows or press Ctrl+C in the backend
echo.

pause
