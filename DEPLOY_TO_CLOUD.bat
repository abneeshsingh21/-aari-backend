@echo off
REM Deploy AARI Backend to Heroku Cloud
REM This makes AARI work 24/7 without your laptop

color 0B
title AARI Cloud Deployment Helper

echo.
echo ================================
echo  AARI Backend Cloud Deployment
echo ================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not installed
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Heroku CLI not installed
    echo Download from: https://devcenter.heroku.com/articles/heroku-cli
    echo.
    echo After installing, run this script again
    pause
    exit /b 1
)

echo ✓ Git installed
echo ✓ Heroku CLI installed
echo.

REM Navigate to backend
cd /d "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

REM Initialize git if not already done
if not exist .git (
    echo Initializing Git repository...
    git init
    git config user.email "aari@voiceassistant.com"
    git config user.name "AARI Assistant"
)

REM Login to Heroku
echo.
echo Logging in to Heroku...
heroku login

REM Create Heroku app
set /p APP_NAME="Enter app name (e.g., my-aari-backend): "

echo.
echo Creating Heroku app: %APP_NAME%
heroku create %APP_NAME%

REM Add files to git
echo.
echo Adding files to git...
git add .
git commit -m "Initial AARI backend deployment"

REM Deploy to Heroku
echo.
echo Deploying to Heroku... (this may take 2-3 minutes)
git push heroku master

REM Get the URL
echo.
echo ================================
echo  Deployment Complete!
echo ================================
echo.
echo Your backend is now live at:
heroku info -s | findstr /R "^web_url="
echo.
echo Next steps:
echo 1. Copy the URL above
echo 2. Open Android app
echo 3. Go to Settings
echo 4. Update Backend URL to: https://your-app-name.herokuapp.com/api
echo.
pause
