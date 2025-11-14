@echo off
REM Start all services - Backend and Frontend

echo.
echo =========================================
echo   AARI - Starting All Services
echo =========================================
echo.

REM Start Backend
echo [Backend] Starting Flask server...
start cmd /k "cd backend && venv\Scripts\activate.bat && python app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start Frontend
echo [Frontend] Starting Expo server...
start cmd /k "cd VoiceAssistantApp && npm start"

echo.
echo =========================================
echo   Services Starting...
echo =========================================
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8081
echo.
echo Scan the QR code with Expo Go on Android
echo Press Ctrl+C in each window to stop
echo =========================================
echo.

pause
