@echo off
REM Deploy AARI to Render.com (Completely FREE)
REM No credit card required, completely free tier

setlocal enabledelayedexpansion

cls
echo.
echo ===============================================
echo   AARI Backend - Deploy to Render (FREE)
echo ===============================================
echo.
echo This deploys AARI to Render cloud - COMPLETELY FREE!
echo No credit card, no paid plans needed.
echo.
echo Prerequisites:
echo   1. GitHub account (free at github.com)
echo   2. Render account (free at render.com)
echo   3. Git installed on your PC
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

cd /d "%~dp0backend"

if not exist ".env" (
    echo ERROR: .env file not found in backend folder!
    echo Please create backend/.env with API keys first
    echo.
    pause
    exit /b 1
)

echo.
echo STEP 1: Create GitHub Account (if you don't have one)
echo Visit: https://github.com/signup
echo Username: (choose any username)
echo Email: (your email)
echo Password: (your password)
echo.
pause

echo.
echo STEP 2: Create GitHub Repository for AARI
echo.
echo Go to: https://github.com/new
echo Repository name: aari-backend
echo Description: AARI Voice Assistant Backend
echo Visibility: Public (required for Render free tier)
echo Click: Create repository
echo.
pause

echo.
echo STEP 3: Push code to GitHub
echo.

REM Check if git repo exists
if not exist ".git" (
    echo Initializing Git repository...
    git init
    git config user.email "aari@voiceassistant.com"
    git config user.name "AARI"
    git add .
    git commit -m "AARI Backend"
)

echo.
echo Pushing code to: https://github.com/abneeshsingh21/aari-backend
echo.

set GITHUB_URL=https://github.com/abneeshsingh21/aari-backend.git

git remote remove origin 2>nul
git remote add origin !GITHUB_URL!
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Failed to push to GitHub
    echo Make sure:
    echo   1. Repository URL is correct
    echo   2. You have push permissions
    echo   3. You're logged into Git
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✓ Code pushed to GitHub!
echo ===============================================
echo.
echo STEP 4: Deploy to Render
echo.
echo Go to: https://render.com
echo Click: Sign up
echo Choose: Sign up with GitHub
echo Connect your GitHub account
echo.
pause

echo.
echo STEP 5: Create new Web Service on Render
echo.
echo Go to: https://dashboard.render.com
echo Click: New + (top right)
echo Choose: Web Service
echo Select: aari-backend repository
echo.
echo Fill in:
echo   Name: aari-backend
echo   Runtime: Python 3
echo   Build Command: pip install -r requirements.txt; python -m spacy download en_core_web_sm
echo   Start Command: gunicorn app:app
echo.
echo Environment Variables (Add these):
echo   GOOGLE_API_KEY = (your key)
echo   SENDER_EMAIL = (your email)
echo   SENDER_PASSWORD = (your app password)
echo.
echo Click: Create Web Service
echo.
echo Wait 2-3 minutes for deployment...
echo.
pause

echo.
echo ===============================================
echo ✓ RENDER DEPLOYMENT COMPLETE!
echo ===============================================
echo.
echo Your app URL will be shown on Render dashboard
echo Example: https://aari-backend.onrender.com
echo.
echo NEXT STEPS:
echo.
echo 1. Copy your Render URL from dashboard
echo.
echo 2. Update Android app file:
echo    android/src/main/java/com/voiceassistant/app/ApiClient.java
echo    
echo    Find:
echo    private static final String CLOUD_BACKEND = "...";
echo    
echo    Change to:
echo    private static final String CLOUD_BACKEND = "https://aari-backend.onrender.com/api";
echo.
echo 3. Rebuild Android APK and install
echo.
echo 4. Test: Say "Hey AARI, what time is it?"
echo.
echo Your AARI now works 24/7 on FREE cloud! ✓
echo.
pause
