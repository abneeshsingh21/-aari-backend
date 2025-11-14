#!/bin/bash
# AARI One-Click Launcher Script
# Download and run this to get started instantly

set -e

echo "╔════════════════════════════════════════╗"
echo "║  AARI Voice Assistant - Quick Launch  ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Detect OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    OS="windows"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    OS="linux"
fi

echo "✓ Operating System: $OS"
echo ""

# Check prerequisites
echo "[1/4] Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git first."
    exit 1
fi
echo "✓ Git installed"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ first."
    exit 1
fi
echo "✓ Node.js installed"

echo ""
echo "[2/4] Cloning repository..."

REPO_URL="https://github.com/abneeshsingh21/-aari-backend.git"
REPO_DIR="aari-assistant"

if [ -d "$REPO_DIR" ]; then
    echo "✓ Repository already exists at $REPO_DIR"
else
    git clone "$REPO_URL" "$REPO_DIR"
    echo "✓ Repository cloned"
fi

cd "$REPO_DIR"

echo ""
echo "[3/4] Installing dependencies..."
cd VoiceAssistantApp
npm install --legacy-peer-deps > /dev/null 2>&1
echo "✓ Dependencies installed"

echo ""
echo "[4/4] Starting services..."
echo ""
echo "╔════════════════════════════════════════╗"
echo "║    Services Starting                   ║"
echo "╠════════════════════════════════════════╣"
echo "║ Backend: https://aari-backend-3rs9... ║"
echo "║ Frontend: http://localhost:8081       ║"
echo "║                                        ║"
echo "║ Android: Scan QR with Expo Go         ║"
echo "║ Desktop: python ../desktop/run_*.py   ║"
echo "╚════════════════════════════════════════╝"
echo ""

npx expo start
