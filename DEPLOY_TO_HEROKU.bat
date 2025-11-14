@echo off
REM Deploy AARI Backend to Heroku (Cloud - 24/7 Running)
REM This allows AARI to work even when your laptop is OFF

setlocal enabledelayedexpansion

cls
echo.
echo ===============================================
echo   AARI Backend - Cloud Deployment (Heroku)
echo ===============================================
echo.
echo This will deploy AARI backend to Heroku cloud
echo Your AARI will work 24/7 even when PC is OFF!
echo.

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Heroku CLI not found!
    echo.
    echo Download and install from:
    echo https://devcenter.heroku.com/articles/heroku-cli
    echo.
    pause
    exit /b 1
)

echo [1/6] Heroku CLI found!
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found!
    echo Download from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [2/6] Git found!
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found in backend folder!
    echo Please create backend/.env with your API keys:
    echo   GOOGLE_API_KEY=...
    echo   SENDER_EMAIL=...
    echo   SENDER_PASSWORD=...
    echo.
    pause
    exit /b 1
)

echo [3/6] API keys configured!
echo.

REM Login to Heroku
echo [4/6] Logging into Heroku...
call heroku login
if errorlevel 1 (
    echo ERROR: Heroku login failed!
    pause
    exit /b 1
)

echo.

REM Initialize git repo if not exists
if not exist ".git" (
    echo [5/6] Initializing Git repository...
    call git init
    call git config user.email "aari@voiceassistant.com"
    call git config user.name "AARI Setup"
    call git add .
    call git commit -m "AARI Backend Initial Commit"
) else (
    echo [5/6] Git repository already exists!
)

echo.
echo [6/6] Deploying to Heroku...
echo.
echo Enter a name for your Heroku app (e.g., aari-voice-assistant):
set /p APP_NAME=

if "!APP_NAME!"=="" (
    set APP_NAME=aari-voice-assistant
)

echo.
echo Creating Heroku app: !APP_NAME!
call heroku create !APP_NAME! 2>nul

if errorlevel 1 (
    echo.
    echo Note: App may already exist. Using existing app.
)

echo.
echo Adding Python buildpack...
call heroku buildpacks:add heroku/python --app !APP_NAME!

echo.
echo Deploying code to cloud...
call git push heroku main 2>nul

if errorlevel 1 (
    echo.
    echo Trying alternative branch name...
    call git branch -M main
    call git push heroku main
)

echo.
echo ===============================================
echo ✓ DEPLOYMENT COMPLETE!
echo ===============================================
echo.
echo Your app is live at:
echo https://!APP_NAME!.herokuapp.com
echo.
echo Test it:
echo.
call heroku open --app !APP_NAME!
echo.

echo Next steps:
echo.
echo 1. Test backend health:
echo    https://!APP_NAME!.herokuapp.com/api/health
echo.
echo 2. Update Android app:
echo    File: android/src/main/java/com/voiceassistant/app/ApiClient.java
echo    Change BASE_URL to: https://!APP_NAME!.herokuapp.com
echo.
echo 3. Rebuild Android APK and install
echo.
echo 4. Your AARI now works 24/7! (PC can be OFF)
echo.
echo View logs:
echo    heroku logs --tail --app !APP_NAME!
echo.

pause
