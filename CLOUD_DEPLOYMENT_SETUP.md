# Deploy AARI Backend to Cloud (24/7 Always Available)

## 🎯 Why Deploy to Cloud?

**Problems with PC-only backend:**
- PC must stay on 24/7 (wastes electricity)
- If PC crashes, AARI stops working
- Can't use AARI when PC is off

**Benefits of cloud deployment:**
- ✅ Always available 24/7
- ✅ Accessible from anywhere
- ✅ Auto-restart on failure
- ✅ Free or very cheap ($0-15/month)
- ✅ Works even if your PC is off

---

## 🚀 Option 1: Deploy on Heroku (EASIEST - Free with limitations)

### Why Heroku?
- Free tier available
- Simple deployment (5 minutes)
- Great for testing
- Easy to upgrade later

### Step 1: Create Heroku Account
1. Visit: https://www.heroku.com
2. Click "Sign Up"
3. Enter email, password
4. Verify email
5. Create account

### Step 2: Install Heroku CLI
**Windows:**
```powershell
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or use Windows Package Manager:
winget install Heroku.CLI

# Verify installation
heroku --version
```

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
heroku --version
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
heroku --version
```

### Step 3: Create Procfile

In `backend/Procfile` (already exists), ensure it contains:
```
web: gunicorn app:app
```

If it doesn't exist, create it:
```powershell
cd "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"
echo "web: gunicorn app:app" | Out-File -Encoding UTF8 Procfile
```

### Step 4: Create runtime.txt

In `backend/runtime.txt`, specify Python version:
```
python-3.11.6
```

### Step 5: Deploy to Heroku

**First time setup:**
```powershell
cd "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

# Login to Heroku
heroku login
# Follow the browser prompt to authenticate

# Create new Heroku app
heroku create aari-voice-assistant
# Alternative: heroku create (Heroku will generate a name)

# Add Python buildpack
heroku buildpacks:add heroku/python

# Set environment variables
heroku config:set GOOGLE_API_KEY=your_actual_key_here
heroku config:set SENDER_EMAIL=your_email@gmail.com
heroku config:set SENDER_PASSWORD=your_app_password

# Deploy code
git init
git add .
git commit -m "Initial AARI deployment"
git push heroku main
```

**View your app:**
```powershell
heroku open
# Your app is now at: https://aari-voice-assistant.herokuapp.com
```

**Check logs:**
```powershell
heroku logs --tail
```

### Step 6: Update Android App

In `android/src/main/java/com/voiceassistant/app/ApiClient.java`:

Find:
```java
private static final String BASE_URL = "http://192.168.1.100:5000";
```

Replace with:
```java
private static final String BASE_URL = "https://aari-voice-assistant.herokuapp.com";
```

Then rebuild and reinstall the Android app.

### Testing Heroku Deployment

```powershell
# Test health endpoint
Invoke-WebRequest -Uri "https://aari-voice-assistant.herokuapp.com/api/health"
# Should return: {"status":"healthy"}

# Test status endpoint
Invoke-WebRequest -Uri "https://aari-voice-assistant.herokuapp.com/api/status"
```

---

## 🚀 Option 2: Deploy on Google Cloud Run (Free tier, Scalable)

### Why Google Cloud Run?
- Free tier: 2 million requests/month
- Pay only for what you use
- Automatically scales
- Very reliable

### Step 1: Create Google Cloud Project
1. Visit: https://console.cloud.google.com
2. Click "Create Project"
3. Enter name: "AARI-Assistant"
4. Click "Create"
5. Wait for project creation

### Step 2: Enable Required APIs
```powershell
# In Google Cloud Console:
# 1. Search for "Cloud Run API"
# 2. Click "Enable"
# 3. Search for "Artifact Registry API"
# 4. Click "Enable"
```

### Step 3: Install Google Cloud SDK
**Windows:**
```powershell
# Download from: https://cloud.google.com/sdk/docs/install
# Run installer
# Or use chocolatey:
choco install google-cloud-sdk

# Initialize
gcloud init
```

**macOS:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

### Step 4: Configure Docker

Heroku uses `Dockerfile` if it exists. Update it:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy app code
COPY . .

# Set environment
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--timeout", "120", "app:app"]
```

### Step 5: Deploy to Cloud Run

```powershell
cd "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

# Login to Google Cloud
gcloud auth login

# Set project
gcloud config set project aari-assistant

# Deploy
gcloud run deploy aari-backend `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "GOOGLE_API_KEY=your_key,SENDER_EMAIL=your_email"
```

Your app will be available at:
```
https://aari-backend-xxxxx.a.run.app
```

### Step 6: Update Android App

In `ApiClient.java`:
```java
private static final String BASE_URL = "https://aari-backend-xxxxx.a.run.app";
```

Replace `xxxxx` with your actual Cloud Run service name.

---

## 🚀 Option 3: Deploy on AWS Lambda (Free tier, Serverless)

### Why AWS Lambda?
- Free tier: 1 million requests/month
- Serverless (no server to maintain)
- Pay per invocation
- Integrates with AWS ecosystem

### Step 1: Create AWS Account
1. Visit: https://aws.amazon.com
2. Click "Create Account"
3. Enter details
4. Verify with credit card (won't charge for free tier)

### Step 2: Create Lambda Function

In AWS Console:
1. Go to **Lambda**
2. Click **Create Function**
3. Name: `aari-assistant`
4. Runtime: **Python 3.11**
5. Click **Create**

### Step 3: Create Deployment Package

```powershell
cd "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

# Create deployment folder
mkdir lambda_deploy
cd lambda_deploy

# Copy app files
Copy-Item "..\*.py" .
Copy-Item "..\requirements.txt" .

# Install dependencies
pip install -r requirements.txt -t .

# Create deployment package
Compress-Archive -Path * -DestinationPath function.zip
```

### Step 4: Upload to Lambda

1. In AWS Lambda console
2. Click **Upload from** → **ZIP file**
3. Select `function.zip`
4. Click **Save**

### Step 5: Add API Gateway

1. In Lambda console
2. Click **Add trigger**
3. Select **API Gateway**
4. Create new API (HTTP)
5. Click **Add**

Get your API URL and update Android app.

---

## 🚀 Option 4: Deploy on Render.com (Simple, Free)

### Why Render?
- Free tier with auto-sleep
- Very simple deployment
- Git-based deployment
- Reliable uptime

### Step 1: Create Account
1. Visit: https://render.com
2. Sign up with GitHub
3. Authorize Render

### Step 2: Push to GitHub

```powershell
cd "c:\Users\lenovo\Desktop\aari\VoiceAssistant\backend"

# Create GitHub repo (if not exists)
git init
git add .
git commit -m "AARI backend"
git remote add origin https://github.com/yourusername/aari-backend.git
git push -u origin main
```

### Step 3: Deploy on Render

1. Visit: https://render.com/dashboard
2. Click **New** → **Web Service**
3. Connect your GitHub repo
4. Name: `aari-backend`
5. Runtime: **Python 3.11**
6. Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
7. Start command: `gunicorn app:app`
8. Click **Create**

Your app: `https://aari-backend.onrender.com`

---

## 📊 Comparison of Cloud Options

| Feature | Heroku | Google Cloud | AWS | Render |
|---------|--------|--------------|-----|--------|
| Free Tier | Yes (550 hours) | Yes (2M req/mo) | Yes (1M req/mo) | Yes (limited) |
| Setup Time | 5 min | 10 min | 15 min | 5 min |
| Cost | $7/mo+ | $0-20/mo | $0-10/mo | $7/mo+ |
| Scalability | Good | Excellent | Excellent | Good |
| Ease of Use | Easiest | Medium | Hard | Easy |
| Downtime | Rare | Very Rare | Very Rare | Occasional |
| Best For | Beginners | Production | Enterprise | Learners |

**Recommendation:** Start with **Heroku** (easiest) or **Google Cloud Run** (most reliable free tier)

---

## 🔄 Keep Sync Between Local & Cloud

### Hybrid Mode Setup

Your Android app can use BOTH backends:

```java
// In ApiClient.java

private static final String LOCAL_BACKEND = "http://192.168.1.100:5000";
private static final String CLOUD_BACKEND = "https://aari-voice-assistant.herokuapp.com";

public static void sendCommand(String command, final ApiCallback callback) {
    // Try local first (faster)
    makeRequest(LOCAL_BACKEND, command, new ApiCallback() {
        @Override
        public void onSuccess(JSONObject response) {
            callback.onSuccess(response);
        }

        @Override
        public void onError(String error) {
            // Local failed, try cloud
            makeRequest(CLOUD_BACKEND, command, callback);
        }
    });
}
```

This way:
- ✅ When PC is on: Uses fast local backend
- ✅ When PC is off: Automatically switches to cloud
- ✅ No manual switching needed

---

## 🔐 Security Best Practices

### 1. Protect API Keys
**Never hardcode API keys in app!**

Instead, use environment variables:
```powershell
# Heroku
heroku config:set GOOGLE_API_KEY=sk-xxxxx

# Google Cloud
gcloud run deploy ... --set-env-vars "GOOGLE_API_KEY=sk-xxxxx"

# AWS Lambda
aws lambda update-function-configuration --function-name aari-assistant --environment "Variables={GOOGLE_API_KEY=sk-xxxxx}"
```

### 2. Use HTTPS Only
All cloud deployments use HTTPS (secure).

Local PC: Consider using self-signed certificate:
```python
# In app.py
app.run(ssl_context='adhoc', host='0.0.0.0', port=5000)
```

### 3. Rate Limiting
Add rate limiting to prevent abuse:
```python
# In app.py
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/process-command', methods=['POST'])
@limiter.limit("30 per minute")  # Max 30 requests/min
def process_command():
    # Your code
    pass
```

---

## 📊 Monitoring & Logs

### Heroku
```powershell
heroku logs --tail
heroku logs --tail --dyno web.1
```

### Google Cloud Run
```powershell
gcloud run services describe aari-backend
gcloud logging read "resource.type=cloud_run_revision" --limit 50 --format json
```

### AWS Lambda
```powershell
aws logs tail /aws/lambda/aari-assistant --follow
```

---

## 💰 Cost Estimate

**Monthly costs for 1000 active users:**

| Platform | Estimated Cost |
|----------|---------------|
| Heroku | $7 (cheapest dyno) |
| Google Cloud Run | $2-5 (pay per request) |
| AWS Lambda | $2-5 (pay per request) |
| Render | $7 (starter plan) |

**Free tier:** All support 1000+ requests/month free

---

## 🆘 Troubleshooting Cloud Deployment

### App Won't Start
```powershell
# Check logs
heroku logs --tail

# Restart app
heroku restart

# If still fails, check Procfile exists and is correct
heroku run ls -la
```

### Slow Response Time
```powershell
# Check resource usage
heroku ps

# Upgrade dyno (costs money)
heroku dyno:upgrade web
```

### Environment Variables Not Working
```powershell
# View all env vars
heroku config

# Set correctly
heroku config:set KEY=value

# Restart for changes to take effect
heroku restart
```

### API Requests Failing
1. Check cloud URL is correct
2. Verify API keys are set
3. Check firewall/CORS settings
4. Test with curl:
```powershell
curl -X GET "https://your-cloud-url/api/health"
```

---

## ✅ Final Checklist

- [ ] Choose cloud platform (Heroku recommended)
- [ ] Create account
- [ ] Deploy backend code
- [ ] Set environment variables (API keys)
- [ ] Test health endpoint
- [ ] Update Android app with cloud URL
- [ ] Rebuild and install Android app
- [ ] Test commands with cloud backend
- [ ] Set up hybrid mode (optional)
- [ ] Monitor logs for errors

---

## 🎉 You're All Set!

Your AARI backend is now running 24/7 on the cloud! 

**Next steps:**
1. Install updated Android app
2. Say "Hey AARI" to test
3. Monitor cloud logs for issues
4. Upgrade to paid plan if needed

---

**Your AARI is now always available, everywhere, anytime! 🚀**

Last Updated: November 14, 2025
