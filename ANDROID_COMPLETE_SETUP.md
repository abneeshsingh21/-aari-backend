# AARI Android - Complete Setup Guide (2025)

## 🎯 Your Setup Goals
✅ **Goal 1:** Android app with full features installed and working  
✅ **Goal 2:** Background auto-start without manual opening  
✅ **Goal 3:** Works with "Hey AARI" wake word anytime  
✅ **Goal 4:** Works offline AND with backend server  
✅ **Goal 5:** Backend runs 24/7 (even when PC is off)  
✅ **Goal 6:** Use AARI from anywhere, anytime  

---

## 📊 Architecture Overview

```
Your Android Device
├── AARI App (Frontend)
│   ├── Background Service (Always Running)
│   ├── Voice Recognition Service (Listens for "Hey AARI")
│   ├── Local Database (Offline data)
│   ├── Contact Manager
│   ├── Command Processor
│   └── Auto-start on Boot (BootReceiver)
│
├── Local Storage
│   ├── Cached responses
│   ├── Conversation history
│   ├── Contacts
│   └── User preferences
│
└── Network Connection
    ├── Local: Connects to PC backend (192.168.x.x:5000)
    ├── Cloud: Connects to cloud backend (when PC is off)
    └── Auto-failover: If PC backend down → Cloud backend

Your PC (Backend Option 1 - Local)
├── Python Flask Server (Port 5000)
├── NLP Processing
├── AI Responses
└── External API Integration

Cloud Server (Backend Option 2 - 24/7)
├── AWS / Google Cloud / Heroku
├── 24/7 Running Backend
├── No PC required
└── Always available
```

---

## 🚀 PHASE 1: Backend Setup (Choose One)

### Option A: Local PC Backend (Simple, Free)
**Pros:** Free, fast, full control  
**Cons:** Needs PC running 24/7

**Steps:**
1. Keep `backend/app.py` running on your PC
2. Keep PC connected to internet
3. AARI connects to `http://192.168.1.100:5000` (your PC's IP)

**Command to run:**
```powershell
cd "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"
.\venv\Scripts\Activate.ps1
python app.py
```

**Keep this window open!**

---

### Option B: Cloud Backend (24/7, Works When PC Off)
**Pros:** Always available, 24/7, PC can be off  
**Cons:** Requires $5-15/month (or free trial)

**Best Platforms:**
1. **Heroku** (Easiest) - Free tier available
2. **Google Cloud Run** - $0.15 per million requests
3. **AWS Lambda** - Free tier + pay-per-use
4. **Render.com** - Free with limitations

**Quick Setup (Heroku - Free):**

#### Step 1: Create Heroku Account
```
Visit: https://www.heroku.com/
Sign up with email
```

#### Step 2: Download & Install Heroku CLI
```powershell
# Windows - Download from: https://devcenter.heroku.com/articles/heroku-cli

# Verify installation
heroku --version
```

#### Step 3: Deploy AARI Backend
```powershell
cd "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

# Login to Heroku
heroku login

# Create new app
heroku create aari-assistant

# Add buildpack for Python
heroku buildpacks:add heroku/python

# Deploy code
git init
git add .
git commit -m "Deploy AARI backend"
git push heroku main

# View live URL
heroku open
# Example: https://aari-assistant.herokuapp.com/api/health
```

#### Step 4: Set Environment Variables
```powershell
# Set API keys on Heroku
heroku config:set GOOGLE_API_KEY=your_key_here
heroku config:set SENDER_EMAIL=your_email@gmail.com
heroku config:set SENDER_PASSWORD=your_password
```

**Then update Android to use:**
```java
// In ApiClient.java
private static final String BASE_URL = "https://aari-assistant.herokuapp.com";
```

---

## 📱 PHASE 2: Android App Setup

### Step 1: Open Android Studio
1. Download: https://developer.android.com/studio
2. Install it
3. Open the `android` folder from your workspace

### Step 2: Update Backend IP/URL

**In Android Studio:**
1. Open: `android/src/main/java/com/voiceassistant/app/ApiClient.java`
2. Find this line (around line 20):
```java
private static final String BASE_URL = "http://192.168.1.100:5000";
```

**Choose based on your backend:**
```java
// Option A: Local PC (replace 192.168.1.100 with your PC IP)
private static final String BASE_URL = "http://192.168.1.100:5000";

// Option B: Cloud (Heroku)
private static final String BASE_URL = "https://aari-assistant.herokuapp.com";

// Option C: Google Cloud
private static final String BASE_URL = "https://your-project.cloudfunctions.net";
```

### Step 3: Update AndroidManifest.xml
Ensure these permissions are present (they should be):
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
<uses-permission android:name="android.permission.WAKE_LOCK" />
<uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS" />
```

### Step 4: Build APK

#### Method A: Using Emulator (Quickest)
```
1. Android Studio → AVD Manager
2. Create Virtual Device (Pixel 4, Android 12+)
3. Start the emulator
4. Click Run (Green play button)
5. Select the emulator → Install
```

#### Method B: Using Physical Android Phone (Recommended)
```
1. Enable Developer Mode:
   Settings → About Phone → Tap "Build Number" 7 times
   
2. Enable USB Debugging:
   Settings → Developer Options → USB Debugging → ON
   
3. Connect phone to PC via USB cable
4. In Android Studio → Click Run → Select your device
5. App installs automatically
```

#### Method C: Build APK Manually
```
Android Studio → Build → Build APK(s)
Wait for completion
Copy APK to phone
Install manually
```

---

## 🎯 PHASE 3: Enable Auto-Start & Background Mode

### Step 1: First App Launch
When you open AARI for the first time:
1. **Grant ALL permissions:**
   - ✅ Microphone
   - ✅ Phone
   - ✅ Contacts
   - ✅ SMS
   - ✅ Storage

2. **Go to Settings (⚙️) → Enable:**
   - ✅ "Background Mode"
   - ✅ "Always Listening"
   - ✅ "Listen on Lock Screen"

### Step 2: Disable Battery Optimization

**This is CRITICAL for 24/7 listening!**

**Android 6-8:**
```
Settings → Battery → Battery Optimization
Find AARI → Don't Optimize
```

**Android 9-10:**
```
Settings → Apps & Notifications → Advanced
Special App Access → Battery Optimization
Find AARI → Don't Optimize
```

**Android 11+:**
```
Settings → Apps → AARI → Battery → Battery optimization
Select: Don't optimize
```

### Step 3: Configure Auto-Start on Boot

The BootReceiver should handle this automatically, but verify:

```
Settings → Apps → AARI → Permissions
Ensure: Receive Boot Completed → Allowed
```

### Step 4: Enable Lock Screen Commands

**Android 11+:**
```
Settings → Apps → AARI → Appearance & Behavior
→ Lock Screen Notifications → Show
```

---

## 🔊 PHASE 4: Wake Word Configuration

### Default: "Hey AARI"

### How to Use:
1. **Anytime:** Say **"Hey AARI"** (screen on/off)
2. **AARI responds:** "I'm awake. What can I do?"
3. **You say:** "Send message to John saying hello"
4. **AARI executes:** Sends the message

### Custom Wake Word:
1. Open AARI app
2. Tap **Settings (⚙️)**
3. Under **"Voice Settings"**
4. Change **"Wake Word"** to:
   - "Hey Assistant"
   - "Okay Google" (not recommended)
   - Custom (1-2 words max)

---

## 💡 PHASE 5: Offline Mode (Optional but Recommended)

If laptop is off and no cloud backend:

### AARI Can Still:
- ✅ Type commands
- ✅ Execute local commands (open apps, etc.)
- ✅ Access cached responses
- ✅ Store messages to send later

### AARI Cannot:
- ❌ Do web search
- ❌ Send real messages (queued for later)
- ❌ Get live weather
- ❌ Use AI responses

**Setup:**
1. AARI detects backend is offline
2. Automatically switches to local mode
3. Shows notification: "Local Mode Active"
4. When backend returns, syncs cached data

---

## 🧪 PHASE 6: Testing

### Test 1: Backend Connection
```powershell
Invoke-WebRequest -Uri "http://192.168.1.100:5000/api/health"
# Should return: {"status":"healthy"}
```

### Test 2: Wake Word
1. Open AARI on phone
2. Say: **"Hey AARI"**
3. You should see: "I'm awake"
4. Say: **"What time is it?"**
5. AARI should respond with current time

### Test 3: WhatsApp Message
1. Say: **"Hey AARI"**
2. Say: **"Send WhatsApp to John saying hello"**
3. Check your phone for WhatsApp message

### Test 4: Lock Screen
1. Lock your phone
2. Say: **"Hey AARI"**
3. Say: **"What's the weather?"**
4. AARI responds (works with locked screen!)

### Test 5: Background Mode
1. Close AARI app
2. Wait 30 seconds
3. Say: **"Hey AARI"** (from home screen)
4. AARI should respond (running in background!)

---

## 🌐 PHASE 7: Advanced - Cloud Sync

### Auto-Sync Features:
```json
{
  "sync_enabled": true,
  "sync_interval_minutes": 5,
  "sync_on_wifi_only": false,
  "items_to_sync": [
    "conversation_history",
    "contacts",
    "reminders",
    "custom_commands",
    "learning_data"
  ]
}
```

This means:
- Every 5 minutes, AARI syncs with cloud
- Updates contacts from server
- Uploads conversation logs
- Downloads new features
- Backup your data automatically

### Setup:
Edit `android/src/main/java/com/voiceassistant/app/MainActivity.java`

Find:
```java
// Setup data sync
```

Ensure it's enabled:
```java
if (prefs.getBoolean("sync_enabled", true)) {
    startDataSync();
}
```

---

## 📋 Complete Voice Commands Reference

### Communication
```
"Hey AARI, send WhatsApp to John saying hello"
"Hey AARI, call Mom"
"Hey AARI, send email to work@company.com about meeting"
"Hey AARI, SMS to 5551234567 saying I'm running late"
```

### Information
```
"Hey AARI, what time is it?"
"Hey AARI, what's the weather?"
"Hey AARI, who am I?"
"Hey AARI, what can you do?"
```

### Media & Entertainment
```
"Hey AARI, play Billie Eilish"
"Hey AARI, play nature sounds"
"Hey AARI, open YouTube"
"Hey AARI, search for Python tutorial"
```

### Reminders & Tasks
```
"Hey AARI, remind me to buy groceries tomorrow"
"Hey AARI, set reminder for meeting in 2 hours"
"Hey AARI, remember my password is xyz123"
"Hey AARI, what are my reminders?"
```

### System Control
```
"Hey AARI, turn off the screen"
"Hey AARI, sleep"
"Hey AARI, take screenshot"
"Hey AARI, open settings"
"Hey AARI, unlock phone"
```

### Learning & Advanced
```
"Hey AARI, show my learning progress"
"Hey AARI, check for updates"
"Hey AARI, learn new command"
"Hey AARI, how many times did I call John?"
```

---

## 🛠️ Troubleshooting

### Problem: App Won't Install
**Solution:**
1. Enable Unknown Sources:
   Settings → Security → Unknown Sources → ON
2. Delete old version first
3. Try again

### Problem: Wake Word Not Detecting
**Solution:**
1. Speak clearly and loud
2. Ensure microphone is working
3. Check Background Mode is enabled
4. Restart the app
5. Check battery optimization is disabled

### Problem: Can't Connect to Backend
**Solution:**
1. Verify backend is running
2. Check WiFi is connected
3. Verify correct IP address
4. Check firewall isn't blocking port 5000
5. Try pinging the IP: `ping 192.168.1.100`

### Problem: Crashes at Startup
**Solution:**
1. Clear app cache: Settings → Apps → AARI → Storage → Clear Cache
2. Clear app data: Settings → Apps → AARI → Storage → Clear Data
3. Reinstall the app
4. Check device has 100MB+ free storage

### Problem: No Audio Output
**Solution:**
1. Check volume is not muted
2. Speakers are not plugged in
3. Restart the app
4. Restart the phone

### Problem: Slow Response Time
**Solution:**
1. Ensure good WiFi connection
2. Close other apps
3. Restart phone
4. Check backend server is not overloaded
5. Update backend to latest version

---

## 📱 Device Requirements

**Minimum:**
- Android 6.0 (API 24)
- 2GB RAM
- 100MB free storage
- Microphone

**Recommended:**
- Android 11+ (API 30+)
- 4GB+ RAM
- 500MB free storage
- Headphones with microphone

---

## 🔐 Security & Privacy

### Your Data:
- ✅ Stored locally on your phone
- ✅ Encrypted in transit
- ✅ Never shared with third parties
- ✅ You control all permissions
- ✅ Clear conversation history anytime

### To Clear History:
```
AARI App → Settings → Privacy → Clear History
```

---

## 🚀 You're Ready!

### Quick Start Checklist:
- [ ] Backend running (local or cloud)
- [ ] Android app installed
- [ ] All permissions granted
- [ ] Background mode enabled
- [ ] Battery optimization disabled
- [ ] Tested wake word
- [ ] Tested one command
- [ ] Verified offline sync

### Next Steps:
1. Customize wake word to your preference
2. Add your contacts to contact manager
3. Configure email/WhatsApp credentials
4. Set up cloud backend for 24/7 access
5. Enjoy hands-free assistant!

---

## 📞 Still Need Help?

1. **Backend Issues:** Check `backend/app.py` logs
2. **Android Issues:** Check Android Studio Logcat
3. **Network Issues:** Verify WiFi and firewall settings
4. **API Issues:** Verify API keys in `.env` file

---

## 🎉 Congratulations!

Your AARI Voice Assistant is now ready to help you 24/7 from anywhere on any device!

**Enjoy your intelligent voice assistant! 🚀**

---

**Last Updated:** November 14, 2025  
**Version:** 2.0 - Complete Setup Guide
