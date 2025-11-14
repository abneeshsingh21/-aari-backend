# AI Voice Assistant - Complete Setup Guide

## 🎤 Introduction
This is a powerful, intelligent voice assistant that works on both desktop (Windows/Mac/Linux) and Android devices. It's designed to be more capable than Alexa and Siri with advanced NLP, task automation, and multi-device support.

## ✨ Features

### Voice Recognition & Processing
- Advanced speech recognition with Google Cloud integration
- Natural language processing using spaCy and TextBlob
- AI-powered responses using Google's Generative AI (Gemini)
- Context-aware conversations
- Multi-language support ready

### Task Execution
- **Messaging**: Send WhatsApp messages, SMS
- **Phone Calls**: Initiate calls to contacts
- **File Downloads**: Download PDFs, PPTs, documents from the internet
- **App Control**: Launch applications on your device
- **Media**: Play music and videos on YouTube
- **Reminders**: Set reminders with natural language time parsing
- **Email**: Send emails to contacts
- **System Control**: Lock screen, sleep, restart, adjust volume
- **Web Search**: Search the internet and open results

### Multi-Device Support
- **Desktop**: Windows, macOS, Linux via desktop GUI
- **Android**: Background service with lock screen activation
- **Server**: REST API for remote access and integration

### Advanced Capabilities
- Sentiment analysis of conversations
- Entity linking and relationship mapping
- Conversation history and learning
- Contact management and learning
- Frequent task tracking
- Hotkey activation (Ctrl+Shift+V on desktop)
- Background service on Android (works with locked screen)

---

## 📋 System Requirements

### Backend (Python)
- Python 3.8+
- 4GB RAM minimum
- Internet connection
- Microphone for voice input

### Android
- Android 6.0+ (API 24+)
- 100MB storage space
- Microphone
- Internet connection

### Desktop
- Windows 7+ / macOS 10.12+ / Linux
- Python 3.8+
- Microphone

---

## 🚀 Installation & Setup

### Step 1: Backend Setup (Python)

#### On Windows:
```powershell
# Navigate to backend folder
cd c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

#### On macOS/Linux:
```bash
cd ~/Desktop/aari/VoiceAssistant/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 2: Configure API Keys

Create `.env` file in the backend folder:

```
GOOGLE_API_KEY=your_google_generative_ai_key_here
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
```

**Getting Google API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add it to `.env`

**Gmail App Password:**
1. Enable 2-factor authentication on Gmail
2. Generate app password at https://myaccount.google.com/apppasswords
3. Add it to `.env`

### Step 3: Run Backend Server

```powershell
# Windows
.\venv\Scripts\Activate.ps1
python app.py
```

The server will start on `http://localhost:5000`

### Step 4: Desktop Client Setup

```powershell
# Install additional desktop dependencies
pip install keyboard pynput pydub

# Run desktop assistant
python desktop\desktop_assistant.py
```

---

## 📱 Android Setup

### Method 1: Build from Source (Using Android Studio)

1. **Install Android Studio**: Download from https://developer.android.com/studio

2. **Open Project**:
   - Click "Open" → Navigate to `VoiceAssistant/android` folder
   - Let Gradle sync complete

3. **Configure Backend IP**:
   - Edit `VoiceRecognitionService.java`
   - Replace `192.168.x.x` with your computer's IP address
   - Find your IP: `ipconfig` on Windows, `ifconfig` on Mac/Linux

4. **Build & Install**:
   - Connect Android device (or use emulator)
   - Click "Run" → Select device
   - Wait for build to complete

### Method 2: Direct APK Installation

1. Build APK: `Build` → `Build APK(s)` in Android Studio
2. Transfer APK to phone
3. Install on phone (enable unknown sources in Settings)

### Android Configuration

After installation on Android:
1. Grant all requested permissions when app starts
2. Go to Settings → Apps → Permissions and enable:
   - Microphone
   - Phone (for calls)
   - Contacts
   - Storage

---

## 💬 Usage Examples

### Voice Commands

**Messaging:**
```
"Send message to John saying hi how are you"
"Send WhatsApp to Sarah hello"
```

**Calls:**
```
"Call mom"
"Call 555-1234"
```

**Downloads:**
```
"Download Python tutorial PDF"
"Get powerpoint presentation from example"
```

**App Control:**
```
"Open Chrome"
"Launch Spotify"
"Start calculator"
```

**Media:**
```
"Play Billie Eilish"
"Play nature sounds"
```

**Reminders:**
```
"Remind me to buy groceries tomorrow"
"Set reminder for meeting in 2 hours"
```

**Searches:**
```
"Search for machine learning tutorials"
"Find restaurants near me"
```

**System Control:**
```
"Lock the screen"
"Sleep"
"Restart computer"
```

---

## 🔧 Configuration

### Contact Management

Edit or create `contacts.json`:

```json
{
  "contacts": {
    "mom": "+1234567890",
    "dad": "+0987654321",
    "john": "+1122334455"
  }
}
```

### Preferences

Settings are stored in `assistant_settings.json` and `context.json`:

```json
{
  "user_name": "Your Name",
  "preferences": {
    "language": "english",
    "voice_speed": "normal",
    "timezone": "UTC",
    "notification_enabled": true,
    "wake_word": "hey assistant"
  }
}
```

---

## 📡 REST API Endpoints

### Process Command
```
POST /api/process-command
Body: {"command": "send message to john"}
```

### Send Message
```
POST /api/send-message
Body: {"contact": "john", "message": "hello"}
```

### Make Call
```
POST /api/make-call
Body: {"contact": "john"}
```

### Download File
```
POST /api/download-file
Body: {"file_name": "tutorial", "file_type": "pdf"}
```

### Open App
```
POST /api/open-app
Body: {"app_name": "chrome"}
```

### Get Status
```
GET /api/status
```

### Health Check
```
GET /api/health
```

---

## 🐛 Troubleshooting

### "Listening error" on Desktop
- Check microphone is properly connected
- Test microphone in System Settings
- Restart the application

### Android App Won't Connect
- Verify backend server is running
- Check firewall isn't blocking port 5000
- Confirm both devices on same Wi-Fi network
- Update IP address in VoiceRecognitionService.java

### Speech Recognition Not Working
- Install PyAudio: `pip install pyaudio`
- On Windows: May need Visual C++ build tools
- Test with: `python -c "import pyaudio"`

### Permissions Issues
- On Android: Go to Settings → Apps → Permissions → Grant all
- On Desktop (Windows): Run as Administrator

### API Key Errors
- Verify Google API key is valid
- Check `.env` file exists and is in correct folder
- Restart backend server after updating `.env`

---

## 🔐 Security & Privacy

- All voice data processed locally on your device (except API calls)
- API communications encrypted (HTTPS)
- No data stored on external servers unless you configure it
- Contact information stored locally only
- Conversation history can be cleared anytime

---

## 📈 Advanced Features

### Adding Custom Commands

Edit `task_executor.py` and add to `_handle_intent`:

```python
elif intent == "custom_action":
    return self._handle_custom_action(entities, command)

def _handle_custom_action(self, entities, command):
    # Your custom code here
    return "Custom action completed"
```

### Training New Intents

Add to `nlp_processor.py`:

```python
"your_intent": ["keyword1", "keyword2", "phrase"],
```

### Database Integration

Extend `context_manager.py` to connect to database:

```python
import sqlite3

def save_to_database(self, data):
    conn = sqlite3.connect('assistant.db')
    # Your database logic
```

---

## 🎓 How It Works

### Architecture Overview

```
User Voice Input
     ↓
[Speech Recognition] (Google Speech-to-Text)
     ↓
[NLP Processing] (spaCy + TextBlob)
     ↓
[Intent Extraction] (Keyword matching + AI)
     ↓
[Entity Extraction] (Named Entity Recognition)
     ↓
[Task Execution] (API calls, system commands)
     ↓
[Response Generation] (Google Gemini AI)
     ↓
[Text-to-Speech] (pyttsx3)
     ↓
User Audio Output
```

### NLP Pipeline

1. **Tokenization**: Break text into words/phrases
2. **Named Entity Recognition**: Identify persons, locations, organizations
3. **Intent Classification**: Determine what user wants
4. **Entity Extraction**: Pull out specific information needed
5. **Sentiment Analysis**: Understand emotional context
6. **Response Generation**: Formulate appropriate response

---

## 🚀 Future Enhancements

- [ ] Real-time conversation with AI
- [ ] Multi-language support (Spanish, French, etc.)
- [ ] Custom wake word training
- [ ] Machine learning for personalized responses
- [ ] Smart home integration (IoT)
- [ ] Calendar and task management
- [ ] Integration with more platforms (Telegram, Facebook)
- [ ] Voice cloning for personalized responses
- [ ] Offline mode with local models

---

## 💡 Tips & Tricks

### Activate from Locked Screen (Android)
1. Install assistant
2. Go to Settings → App permissions → Microphone → Allow
3. Enable "Always" for microphone access

### Create Shortcuts
- Desktop: Ctrl+Shift+V to activate
- Android: Add widget to home screen

### Improve Recognition
- Speak clearly and at normal pace
- Minimize background noise
- Use proper names for contacts
- Train on your voice patterns

### Batch Commands
```
"Send message to john saying hi, then call mom, then play music"
```

### Learn Patterns
- Assistant learns your frequent tasks
- Common commands execute faster
- Personalized responses improve over time

---

## 📞 Support & Feedback

For issues or suggestions:
1. Check troubleshooting section above
2. Review log files in `logs/` folder
3. Test API endpoints directly with tools like Postman
4. Enable debug mode in settings

---

## 📄 License & Attribution

This project uses:
- spaCy: https://spacy.io/
- Google Speech Recognition: https://cloud.google.com/speech-to-text
- pyttsx3: https://github.com/nateshmbhat/pyttsx3
- Flask: https://flask.palletsprojects.com/

---

**Happy Assisting! 🚀**

For more information and updates, keep checking the project folder.
