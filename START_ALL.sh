#!/bin/bash
# Start script for running both backend and frontend

echo "Starting AARI Voice Assistant..."

# Function to cleanup on exit
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "[Backend] Starting Python backend..."
    cd backend
    call venv\Scripts\activate.bat
    python app.py &
    BACKEND_PID=$!
    
    echo "[Frontend] Starting React Native frontend..."
    cd ../VoiceAssistantApp
    npm start &
    FRONTEND_PID=$!
else
    # macOS/Linux
    echo "[Backend] Starting Python backend..."
    cd backend
    source venv/bin/activate
    python app.py &
    BACKEND_PID=$!
    
    echo "[Frontend] Starting React Native frontend..."
    cd ../VoiceAssistantApp
    npm start &
    FRONTEND_PID=$!
fi

echo ""
echo "========================================="
echo "AARI Services Running"
echo "========================================="
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:8081"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================="
echo ""

# Wait for both processes
wait
