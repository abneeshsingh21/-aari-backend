# AARI Voice Assistant - Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Start the Backend
**Double-click:** `START_AARI.bat`

OR run in PowerShell:
```powershell
python "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend\run_backend.py"
```

✅ You should see: `Running on http://0.0.0.0:5000`

### Step 2: Start the Desktop App
The script will automatically launch, OR run:
```powershell
python "c:\Users\lenovo\Desktop\aari\VoiceAssistant\desktop\run_desktop.py"
```

✅ You should see a GUI window with "Ready" status (green)

### Step 3: Start Speaking!
**Press:** `Ctrl + Shift + V`  
**Then:** Speak a command  
**Example:** "Hello" or "What time is it?"

---

## 💬 Voice Commands to Try

### Greetings & Info
- "Hello" → Get a personalized greeting
- "What time is it?" → Current time
- "Who are you?" → Learn about AARI
- "What can you do?" → Feature overview

### Communication
- "Send message to [contact] saying [message]" → WhatsApp
- "Call [contact]" → Make a phone call  
- "Send email to [email] about [subject]" → Email

### Media & Search
- "Play [artist/song]" → Music
- "Search for [topic]" → Web search
- "Open [app name]" → Launch application

### Organization
- "Set reminder for [time]" → Create reminder
- "Remember that [fact]" → Store information
- "What was I saying earlier?" → Recall conversation

### Advanced
- "Show my learning progress" → View AI metrics
- "Check for updates" → System updates
- "Install new features" → Add capabilities

---

## 🎯 Control Keys

| Key | Action |
|-----|--------|
| `Ctrl+Shift+V` | Toggle continuous voice listening |
| `🎤 Start Speaking` | One-time voice capture |
| `⌨️ Type` | Type command instead of speaking |
| `🛑 Stop` | Stop listening |

---

## 🔧 Troubleshooting

### Backend Won't Start
1. Close any existing python.exe windows
2. Run: `Get-Process python | Stop-Process -Force`
3. Try again

### Microphone Not Working
1. Check Windows Settings → Privacy → Microphone
2. Ensure microphone is plugged in
3. Use `⌨️ Type` button to type instead

### No Audio Output
1. Check speakers are on
2. Run: `pip install pydub`
3. Install ffmpeg from https://ffmpeg.org/download.html

### Can't Find IP for Android
**Windows Command Prompt:**
```cmd
ipconfig
```
Look for "IPv4 Address" (like 192.168.x.x)

---

## 📱 For Android Users

### Before You Start
1. Get your computer's IPv4 address (see above)
2. Edit `ApiClient.java` in android folder
3. Update line: `private static final String BASE_URL = "http://YOUR_IP:5000/api";`
4. Build and install app

### Android Permissions (Grant All)
- Microphone ✓
- Phone Calls ✓
- Contacts ✓
- SMS ✓
- Storage ✓

### Android Usage
1. Tap microphone button
2. Speak command
3. Hear response
4. Works even with locked screen!

---

## 💡 Pro Tips

1. **Continuous Mode:** Press `Ctrl+Shift+V` once to start always-listening mode. Press again to stop.

2. **Faster Recognition:** Speak clearly and at normal pace. Background noise reduces accuracy.

3. **Learning:** AARI learns from your commands. It gets better over time!

4. **Offline Options:** Use Text mode (`⌨️ Type`) if microphone isn't available.

5. **Contact Management:** Add contacts to `contacts.json` in backend folder for messaging.

---

## 📊 Check System Status

**View Backend Status:**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/status"
```

**View Learning Metrics:**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/learning-status"
```

**Check for Updates:**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/check-updates"
```

---

## 🎁 What You Get

✅ Voice Recognition (Google Cloud)  
✅ Natural Language Processing (spaCy)  
✅ AI Responses (Google Gemini)  
✅ WhatsApp Messaging  
✅ Phone Calling  
✅ Email Sending  
✅ Web Search  
✅ Reminders  
✅ App Launching  
✅ Music Playback  
✅ Smart Learning System  
✅ Multi-Device Support  

---

## 🚀 Next Steps

1. **Explore Features:** Try different voice commands
2. **Test Android:** Build and install on your phone
3. **Add Contacts:** Update `contacts.json` with your contacts
4. **Enable All Features:** Click "Check Updates" in desktop app
5. **Share & Enjoy:** Tell others about AARI!

---

## ❓ Frequently Asked Questions

**Q: Is my voice data safe?**  
A: Voice is processed locally and through secure APIs. No data is stored on external servers.

**Q: Can I use AARI offline?**  
A: Some features work offline (text mode), but voice recognition and web search require internet.

**Q: How do I update AARI?**  
A: Click "Check Updates" in the desktop app, then "Install Updates" for new features.

**Q: Can I use this on Mac/Linux?**  
A: Yes! The code is cross-platform. Just run the same Python scripts on your OS.

**Q: How do I add more contacts?**  
A: Edit `backend/contacts.json` and add entries like: `"john": "+1234567890"`

**Q: Why is speech recognition slow?**  
A: It depends on audio quality and internet speed. Try speaking more clearly.

---

## 📞 Get Help

1. Check the full documentation: `FEATURE_VERIFICATION_REPORT.md`
2. Check the console output for error messages
3. Verify backend is running: `http://localhost:5000/api/health` should return `{"status":"healthy"}`
4. Ensure microphone is enabled in Windows Settings

---

**Enjoy your AARI Voice Assistant! 🎉**

For detailed information, see: `FEATURE_VERIFICATION_REPORT.md`
