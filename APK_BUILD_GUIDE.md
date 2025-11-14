# AARI Android APK - Build & Install Guide

## Quick Build & Install (10 minutes)

### Step 1: Update Backend IP in Android Studio

**File:** `android/src/main/java/com/voiceassistant/app/ApiClient.java`

Find this line and replace with YOUR PC IP:
```java
private static final String BASE_URL = "http://192.168.1.100:5000";
```

Get your IP on Windows:
```powershell
ipconfig
# Look for "IPv4 Address" (like 192.168.x.x)
```

### Step 2: Build APK

**In Android Studio:**
1. Click **Build** menu
2. Select **Build Bundle(s) / APK(s)** → **Build APK(s)**
3. Wait for build to complete (2-5 minutes)
4. Click "Locate" in notification to find APK file

**Or use terminal:**
```powershell
cd "c:\Users\lenovo\Desktop\aari\VoiceAssistant\android"
gradlew.bat assembleDebug
```

### Step 3: Install on Android Device

**Option A: USB Cable (Recommended)**
1. Enable USB Debugging on phone:
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → USB Debugging → ON
2. Connect phone via USB
3. In Android Studio: Click **Run** (green play button)
4. Select device → Install

**Option B: Install APK Manually**
1. Find APK file (usually `android/app/debug/app-debug.apk`)
2. Copy to phone via USB or email
3. On phone: Open file → Tap to install
4. Grant permissions

### Step 4: First Launch

When you open AARI:
1. Grant ALL permissions
2. Go to Settings (⚙️)
3. Enable "Background Mode"
4. Enable "Always Listening"

### Step 5: Test

Say: **"Hey AARI, what time is it?"**

AARI should respond!

---

## ✅ Quick Checklist

- [ ] Backend running on PC (python app.py)
- [ ] Updated IP in ApiClient.java
- [ ] Built APK successfully
- [ ] Installed on Android device
- [ ] Granted all permissions
- [ ] Enabled Background Mode
- [ ] Tested wake word "Hey AARI"
- [ ] Got response to a command

---

**You're done! AARI is ready to use! 🚀**
