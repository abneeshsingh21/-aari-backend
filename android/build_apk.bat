@echo off
REM Build AARI Android App
REM Usage: Run this script from the android directory

cd /d "%~dp0"

echo.
echo ========================================
echo   AARI Android App Build Script
echo ========================================
echo.

REM Check if gradlew exists
if not exist "gradlew.bat" (
    echo Error: gradlew.bat not found. Make sure you're in the android directory.
    pause
    exit /b 1
)

REM Build APK (Debug)
echo Building debug APK...
call gradlew.bat assembleDebug
if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo APK Location:
echo   app\build\outputs\apk\debug\app-debug.apk
echo.
echo To install on device:
echo   gradlew.bat installDebug
echo.
pause
