# AARI Voice Assistant

Voice-controlled assistant for Android and Desktop with Python backend and React Native frontend.

**Live Backend:** https://aari-backend-3rs9.onrender.com

## Quick Start

### Windows
```powershell
.\SETUP.bat
.\START_ALL.bat
```

### macOS/Linux
```bash
./SETUP.sh
./START_ALL.sh
```

## Running

**Backend:** `cd backend && source venv/bin/activate && python app.py`

**Frontend:** `cd VoiceAssistantApp && npm start`

**Android:** Scan QR code with Expo Go

**Desktop:** `python desktop/run_desktop.py`

## API
- Health: `GET /api/health`
- Process: `POST /api/process-command`
