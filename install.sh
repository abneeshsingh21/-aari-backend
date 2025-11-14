#!/bin/bash

# Installation script for macOS and Linux
# AI Voice Assistant Setup

echo "========================================"
echo "AI VOICE ASSISTANT - Installation"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  macOS: brew install python@3.11"
    echo "  Linux: sudo apt-get install python3 python3-pip"
    exit 1
fi

# Navigate to backend
cd "$(dirname "$0")/backend" || exit 1

# Create virtual environment
echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "[2/5] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Download spaCy model
echo "[4/5] Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Setup config
echo "[5/5] Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env and add your API keys"
    echo "  - GOOGLE_API_KEY"
    echo "  - SENDER_EMAIL"
    echo "  - SENDER_PASSWORD"
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run backend: python app.py"
echo "3. Run desktop: python desktop_assistant.py"
echo ""
echo "See README.md for full documentation"
echo "========================================"
