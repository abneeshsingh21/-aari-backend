@echo off
title AARI Backend Server
color 0B

echo.
echo ====================================
echo    AARI Voice Assistant Backend
echo ====================================
echo.

cd /d "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

echo Activating Python environment...
call venv\Scripts\activate.bat

echo.
echo Starting Flask server on http://localhost:5000
echo Your IP: 192.168.29.110:5000
echo.
echo Press CTRL+C to stop
echo.

python app.py

pause
