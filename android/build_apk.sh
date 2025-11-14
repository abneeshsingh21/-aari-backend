#!/bin/bash

# Build AARI Android App
# Usage: ./build_apk.sh

cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "  AARI Android App Build Script"
echo "========================================"
echo ""

# Check if gradlew exists
if [ ! -f "gradlew" ]; then
    echo "Error: gradlew not found. Make sure you're in the android directory."
    exit 1
fi

# Make gradlew executable
chmod +x gradlew

# Build APK (Debug)
echo "Building debug APK..."
./gradlew assembleDebug
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "  Build Complete!"
echo "========================================"
echo ""
echo "APK Location:"
echo "  app/build/outputs/apk/debug/app-debug.apk"
echo ""
echo "To install on device:"
echo "  ./gradlew installDebug"
echo ""
