@echo off
REM Deploy AARI Backend to Google Cloud Run - FREE
REM This is the best free option with 2M requests/month

color 0B
title AARI - Google Cloud Run Deployment

echo.
echo ====================================
echo  AARI Backend - Google Cloud Deploy
echo ====================================
echo.

REM Check if gcloud CLI is installed
gcloud --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Google Cloud CLI not installed
    echo.
    echo Download from:
    echo https://cloud.google.com/sdk/docs/install
    echo.
    echo After installing, run this script again
    pause
    exit /b 1
)

REM Check if docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker not installed
    echo.
    echo Download from: https://www.docker.com/products/docker-desktop
    echo.
    echo After installing, run this script again
    pause
    exit /b 1
)

echo ✓ Google Cloud CLI installed
echo ✓ Docker installed
echo.

REM Navigate to backend
cd /d "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

REM Login to Google Cloud
echo Logging in to Google Cloud...
gcloud auth login
gcloud config set project <YOUR-PROJECT-ID>

REM Set variables
set PROJECT_ID=
for /f "tokens=*" %%i in ('gcloud config get-value project') do set PROJECT_ID=%%i
set SERVICE_NAME=aari-voice-backend
set REGION=us-central1

echo.
echo Project ID: %PROJECT_ID%
echo Service: %SERVICE_NAME%
echo Region: %REGION%
echo.

REM Deploy to Cloud Run
echo Deploying to Google Cloud Run...
echo This may take 3-5 minutes...
echo.

gcloud run deploy %SERVICE_NAME% ^
  --source . ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --memory 512Mi ^
  --timeout 3600s

REM Get the service URL
echo.
echo ================================
echo  Deployment Complete!
echo ================================
echo.

for /f "tokens=*" %%i in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --format "value(status.address.url)"') do (
    set SERVICE_URL=%%i
    echo Your backend URL:
    echo !SERVICE_URL!
    echo.
    echo Next steps:
    echo 1. Copy the URL above
    echo 2. Update Android app ApiClient.java:
    echo    Change: private static final String BASE_URL = "!SERVICE_URL!/api";
    echo 3. Rebuild and test on Android
)

echo.
echo FREE TIER: 2 million requests per month
echo ALWAYS FREE: No cost for low traffic
echo.
pause
