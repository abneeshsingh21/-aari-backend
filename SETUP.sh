#!/bin/bash

# AARI - Complete Setup Script for macOS/Linux

echo ""
echo "========================================="
echo "   AARI Voice Assistant - Setup"
echo "========================================="
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed. Please install Git first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "[1/5] Cloning repository..."
git clone https://github.com/abneeshsingh21/-aari-backend.git
cd -aari-backend

echo "[2/5] Setting up Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "[3/5] Creating .env file..."
if [ ! -f .env ]; then
    cat > .env << EOF
GOOGLE_API_KEY=your_key_here
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
EOF
    echo "Please edit .env with your API keys"
fi

cd ..

echo "[4/5] Setting up Frontend..."
cd VoiceAssistantApp
npm install

cd ..

echo "[5/5] Setup Complete!"
echo ""
echo "========================================="
echo "   Setup Completed Successfully!"
echo "========================================="
echo ""
echo "Next Steps:"
echo "1. Configure backend/.env with your API keys"
echo "2. Run backend: cd backend && source venv/bin/activate && python app.py"
echo "3. Run frontend: cd VoiceAssistantApp && npm start"
echo ""
