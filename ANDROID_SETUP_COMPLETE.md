# AARI Android Setup - Complete Guide

## 🎯 Overview
This guide will help you set up AARI on your Android device with:
- ✅ Backend server running 24/7
- ✅ Android app auto-starting on device boot
- ✅ Background voice listening with "Hey AARI" wake word
- ✅ Lock screen commands execution
- ✅ Foreground service for continuous operation

---

## 📋 Prerequisites

### System Requirements
- Android 6.0+ (API 24+)
- 100MB free storage
- Microphone access
- Internet connection
- Windows PC/Mac/Linux with Python 3.8+

### Software Requirements
- Android Studio (latest version)
- Python 3.8+ (Windows/Mac/Linux)
- Git (optional)

---

## 🔧 Step 1: Backend Setup (Desktop PC)

### 1.1 Install Python & Dependencies

#### Windows:
```powershell
# Navigate to backend folder
cd c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install all dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

#### macOS/Linux:
```bash
cd ~/Desktop/aari/VoiceAssistant/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 1.2 Configure API Keys

Create `.env` file in backend folder:

```
GOOGLE_API_KEY=your_google_generative_ai_key
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_app_password
```

**How to get Google API Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key to `.env`

**How to get Gmail App Password:**
1. Enable 2-factor authentication: https://myaccount.google.com/security
2. Go to App passwords: https://myaccount.google.com/apppasswords
3. Select Mail & Windows (or custom)
4. Copy password to `.env`

### 1.3 Start Backend Server

#### Windows (Command Prompt):
```cmd
cd c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend
.\venv\Scripts\Activate.ps1
python app.py
```

The server should start on `http://localhost:5000`

**Expected output:**
```
WARNING in app.run()
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

**Keep this window open!** The server must run continuously.

---

## 📱 Step 2: Android App Setup

### 2.1 Open Project in Android Studio

1. Open Android Studio
2. Click **File** → **Open**
3. Navigate to: `c:\Users\lenovo\Desktop\aari\VoiceAssistant\android`
4. Wait for Gradle to sync (5-10 minutes)

### 2.2 Find Your PC's IP Address

#### On Windows (Command Prompt):
```cmd
ipconfig
```
Look for "IPv4 Address" (usually starts with 192.168.x.x or 10.0.x.x)

#### On macOS (Terminal):
```bash
ifconfig | grep "inet "
```

#### On Linux (Terminal):
```bash
hostname -I
```

**Example:** `192.168.1.100`

### 2.3 Update Backend Server IP

In Android Studio, open: `android/src/main/java/com/voiceassistant/app/ApiClient.java`

Find this line:
```java
private static final String BASE_URL = "http://192.168.x.x:5000";
```

Replace `192.168.x.x` with your PC's actual IP:
```java
private static final String BASE_URL = "http://192.168.1.100:5000";  // Use YOUR IP
```

### 2.4 Build & Install on Android Device

**Option A: Using Physical Device**

1. Enable USB Debugging on Android:
   - Settings → About Phone → Tap Build Number 7 times
   - Settings → Developer Options → Enable USB Debugging
   - Connect phone via USB

2. In Android Studio:
   - Click **Run** (Green Play Button)
   - Select your device
   - Wait for installation (2-5 minutes)

**Option B: Using Android Emulator**

1. In Android Studio:
   - Click **AVD Manager** (phone icon in toolbar)
   - Create a new Virtual Device (Pixel 4, Android 12+)
   - Start the emulator
   - Click **Run** and select the emulator

**Option C: Build APK & Install Manually**

1. Click **Build** → **Build APK(s)**
2. Wait for completion
3. Locate the APK file (usually in `android/app/release/`)
4. Copy to phone via USB or email
5. On phone, open file manager and tap the APK to install

---

## 🚀 Step 3: Enable Auto-Start & Background Service

### 3.1 First Launch Setup

When you open AARI for the first time:

1. **Grant All Permissions** when prompted:
   - ✅ Microphone
   - ✅ Phone
   - ✅ Contacts
   - ✅ Storage
   - ✅ Location (optional)

2. **Enable Background Mode:**
   - Tap **Settings** button (⚙️)
   - Enable **"Background Mode"**
   - This allows AARI to listen for "Hey AARI" even when locked

### 3.2 Configure Auto-Start on Boot

#### Android 6-8:
Settings → Apps → AARI → Permissions → Microphone → Allow → **Always**

#### Android 9-10:
Settings → Apps & Notifications → Special App Access → Microphone → AARI → **Allow all the time**

#### Android 11+:
Settings → Apps → All apps → AARI → Permissions → Microphone → **Allow only while using the app** (or **Allow all the time** for best experience)

### 3.3 Disable Battery Optimization (CRITICAL for Background Service)

**Android 6+:**
1. Settings → Battery
2. Search for **"Battery Optimization"** or **"Battery Saver"**
3. Find **AARI** in the list
4. Tap it → Select **"Don't Optimize"** or **"Unrestricted"**

**Android 9-10:**
1. Settings → Apps & Notifications → Advanced
2. Special App Access → Battery Optimization
3. Find AARI → Tap → Select **"Don't Optimize"**

**Android 11+:**
1. Settings → Apps
2. Find AARI → Tap
3. Battery → Battery optimization → Select **"Don't optimize"**

### 3.4 Allow Wake Lock (Optional but Recommended)

This keeps the app running even when screen is off:

1. Settings → Apps → AARI → Advanced
2. Enable **"Allow to wake device"** or similar option

---

## 🎤 Step 4: Wake Word Configuration

### How to Use AARI

**Default Wake Word:** "Hey AARI"

### Flow:
1. **Anytime:** Say **"Hey AARI"** (even with screen off)
2. **AARI responds:** "I'm awake. Say your command..."
3. **You speak:** "Send message to John saying hello"
4. **AARI executes:** The command

### Custom Wake Word:

In the Android app:
1. Tap **Settings** (⚙️)
2. Under **"Voice Settings"**
3. Change **"Wake Word"** to your preference
4. Available options:
   - "Hey AARI"
   - "Hey assistant"
   - "OK Google" (not recommended - may conflict)
   - Custom (single/two words)

---

## 💬 Example Commands

### Voice Commands You Can Use:

**Messaging:**
```
"Hey AARI, send message to John saying hello how are you"
"Hey AARI, WhatsApp to Sarah"
```

**Calls:**
```
"Hey AARI, call mom"
"Hey AARI, call 5551234567"
```

**Downloads:**
```
"Hey AARI, download Python tutorial"
"Hey AARI, get PowerPoint from Google"
```

**App Control:**
```
"Hey AARI, open Chrome"
"Hey AARI, launch Spotify"
```

**Media:**
```
"Hey AARI, play Billie Eilish"
"Hey AARI, play nature sounds"
```

**Reminders:**
```
"Hey AARI, remind me to buy groceries tomorrow"
"Hey AARI, set reminder for meeting in 2 hours"
```

**Web Search:**
```
"Hey AARI, search for machine learning"
"Hey AARI, find restaurants near me"
```

**System Control:**
```
"Hey AARI, lock the screen"
"Hey AARI, sleep"
"Hey AARI, take a screenshot"
```

---

## 🔍 Troubleshooting

### AARI Won't Listen in Background

**Solution:**
1. Go to **Settings** → **Battery** → **Battery Optimization**
2. Find **AARI** → Select **"Don't Optimize"**
3. Check app permissions → Microphone → Enable "Always"
4. Restart the app

### Can't Connect to Backend Server

**Check:**
1. PC's backend server is running: `http://192.168.1.100:5000` (with YOUR IP)
2. Both phone and PC on **same WiFi network**
3. Update the IP in `ApiClient.java` (Step 2.3)
4. Firewall isn't blocking port 5000:
   ```cmd
   # Windows - Allow port 5000 in firewall
   netsh advfirewall firewall add rule name="Flask" dir=in action=allow protocol=tcp localport=5000
   ```

### Speech Recognition Not Working

**Solution:**
1. Check microphone is working: Settings → Sound → Microphone Test
2. Speak clearly and slowly
3. Minimize background noise
4. Grant microphone permission
5. Restart the app

### App Keeps Stopping

**Solution:**
1. Update Android
2. Clear app cache: Settings → Apps → AARI → Storage → Clear Cache
3. Reinstall the app
4. Check storage space (need at least 100MB)

### Can't Install APK

**Solution:**
1. Settings → Security → Enable "Unknown Sources"
2. Or: Settings → Apps & Notifications → Advanced → Special App Access → Install Unknown Apps → Choose File Manager → Allow
3. Retry installation

---

## 📊 Monitoring Your Setup

### Check Backend Status

In browser, visit:
```
http://192.168.1.100:5000/api/health
```

You should see:
```json
{"status": "healthy"}
```

### Test API Endpoints

**From Android app or web:**
```
GET http://192.168.1.100:5000/api/status
```

Response:
```json
{
  "status": "running",
  "assistant": "AI Voice Assistant",
  "version": "1.0.0"
}
```

### View Backend Logs

On PC where backend is running, logs appear in the console window.

---

## 🎯 Final Checklist

Before considering setup complete:

- [ ] Python backend installed with all dependencies
- [ ] API keys configured in `.env` file
- [ ] Backend server running on PC (window stays open)
- [ ] AARI app installed on Android device
- [ ] Updated IP address in Android app (`ApiClient.java`)
- [ ] Granted all permissions to AARI
- [ ] Enabled Background Mode in AARI settings
- [ ] Disabled battery optimization for AARI
- [ ] Tested wake word: Say "Hey AARI"
- [ ] Tested a command: "Hey AARI, what's the time?"
- [ ] Verified backend health: `http://192.168.1.100:5000/api/health`

---

## 🚀 You're All Set!

### How to Use AARI Going Forward:

1. **Start PC backend:**
   ```
   cd c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend
   .\venv\Scripts\Activate.ps1
   python app.py
   ```

2. **Keep the backend window open** (it runs in background)

3. **On Android phone:**
   - Background service auto-starts
   - Say "Hey AARI" anytime
   - AARI listens and executes commands
   - Works even with locked screen!

4. **To stop AARI on phone:**
   - Open AARI app → Settings → Toggle Background Mode OFF
   - Or: Force stop from Settings → Apps

---

## 📞 Support & Advanced Configuration

### Adding Custom Commands

Edit `android/src/main/java/com/voiceassistant/app/VoiceAssistantService.java`

In `processCommand()` method, add:
```java
else if (command.contains("your_trigger")) {
    handleYourCustom(command);
}
```

### Extending Backend Capabilities

Edit `backend/app.py` to add new API endpoints:
```python
@app.route('/api/your-endpoint', methods=['POST'])
def your_endpoint():
    # Your code here
    return jsonify({"status": "success"})
```

### Contact Management

Edit `backend/contacts.json`:
```json
{
  "contacts": {
    "mom": "+1234567890",
    "john": "+9876543210",
    "sarah": "9123456789"
  }
}
```

---

## 🔒 Security Notes

- All voice data processed locally on your device
- API communications use HTTP (LAN only)
- Contact information stored locally only
- No data sent to external servers unless configured
- Clear conversation history anytime: Settings → Privacy

---

## 📈 Performance Optimization

**If AARI is slow:**

1. Close unnecessary apps on phone
2. Restart phone periodically
3. Ensure PC has good internet connection
4. Update to latest Android version
5. Clear app cache: Settings → Apps → AARI → Storage → Clear Cache

**If backend is slow:**

1. Ensure PC has 4GB+ RAM
2. Disable unnecessary services on PC
3. Update all Python packages: `pip install --upgrade -r requirements.txt`
4. Check internet connection speed: `speedtest.py` or online

---

**Congratulations! AARI is now ready to assist you 24/7! 🎉**

For detailed troubleshooting and advanced features, refer to main README.md

