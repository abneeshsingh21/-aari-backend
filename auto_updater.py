"""
Automatic Update System for Voice Assistant
Enables self-learning and feature updates without manual intervention
"""

import json
import os
import subprocess
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests
import hashlib

logger = logging.getLogger(__name__)


class AutoUpdater:
    """Handles automatic updates and self-learning"""
    
    def __init__(self):
        self.update_log_file = "update_log.json"
        self.features_file = "features.json"
        self.learning_file = "learning_database.json"
        self.config_file = "auto_update_config.json"
        
        self._init_update_system()
    
    def _init_update_system(self):
        """Initialize update system"""
        if not os.path.exists(self.config_file):
            default_config = {
                "auto_update_enabled": True,
                "update_frequency_hours": 24,
                "last_update_check": None,
                "last_feature_update": None,
                "auto_learn_enabled": True,
                "max_features": 500,
                "backup_before_update": True,
                "update_history": [],
                "installed_features": [],
                "pending_updates": []
            }
            self._save_config(default_config)
        
        if not os.path.exists(self.update_log_file):
            self._save_update_log({
                "created_at": datetime.now().isoformat(),
                "updates": []
            })
    
    def check_for_updates(self) -> Dict[str, Any]:
        """Check if updates are available"""
        try:
            config = self._load_config()
            
            # Check if enough time has passed since last update check
            last_check = config.get("last_update_check")
            if last_check:
                last_check_time = datetime.fromisoformat(last_check)
                hours_since = (datetime.now() - last_check_time).total_seconds() / 3600
                
                if hours_since < config.get("update_frequency_hours", 24):
                    return {"status": "no_update_needed", "reason": "Too soon to check"}
            
            # Check for available updates
            available_updates = self._fetch_available_updates()
            
            config["last_update_check"] = datetime.now().isoformat()
            self._save_config(config)
            
            if available_updates:
                return {
                    "status": "updates_available",
                    "updates": available_updates,
                    "count": len(available_updates)
                }
            else:
                return {"status": "up_to_date"}
        
        except Exception as e:
            logger.error(f"Update check error: {e}")
            return {"status": "error", "message": str(e)}
    
    def _fetch_available_updates(self) -> List[Dict]:
        """Fetch available updates from remote source"""
        try:
            # Simulated update check - in production would query update server
            updates = [
                {
                    "name": "web_search_integration",
                    "version": "2.0",
                    "description": "Real-time web search capability",
                    "size_mb": 5,
                    "priority": "high"
                },
                {
                    "name": "web_automation",
                    "version": "1.0",
                    "description": "Browser automation for complex tasks",
                    "size_mb": 8,
                    "priority": "high"
                },
                {
                    "name": "api_integrations",
                    "version": "1.0",
                    "description": "Multiple service API integrations",
                    "size_mb": 12,
                    "priority": "medium"
                },
                {
                    "name": "payment_gateway",
                    "version": "1.0",
                    "description": "Online payment processing",
                    "size_mb": 6,
                    "priority": "medium"
                },
                {
                    "name": "sentiment_analysis",
                    "version": "2.5",
                    "description": "Advanced sentiment and emotion detection",
                    "size_mb": 10,
                    "priority": "medium"
                }
            ]
            
            config = self._load_config()
            installed = config.get("installed_features", [])
            
            # Filter out already installed features
            available = [u for u in updates if u["name"] not in installed]
            
            return available
        
        except Exception as e:
            logger.error(f"Error fetching updates: {e}")
            return []
    
    def auto_install_updates(self, feature_names: List[str] = None) -> Dict[str, Any]:
        """Automatically install updates"""
        try:
            config = self._load_config()
            
            # If no features specified, install all high-priority updates
            if not feature_names:
                available = self._fetch_available_updates()
                feature_names = [u["name"] for u in available if u.get("priority") == "high"]
            
            if not feature_names:
                return {"status": "no_updates_to_install"}
            
            # Backup before updating
            if config.get("backup_before_update"):
                self._backup_system()
            
            installed_features = []
            failed_features = []
            
            for feature_name in feature_names:
                try:
                    result = self._install_feature(feature_name)
                    if result["status"] == "success":
                        installed_features.append(feature_name)
                        config["installed_features"].append(feature_name)
                    else:
                        failed_features.append({"name": feature_name, "error": result.get("error")})
                except Exception as e:
                    failed_features.append({"name": feature_name, "error": str(e)})
                    logger.error(f"Failed to install {feature_name}: {e}")
            
            # Update last feature update time
            config["last_feature_update"] = datetime.now().isoformat()
            
            # Add to history
            update_record = {
                "timestamp": datetime.now().isoformat(),
                "installed": installed_features,
                "failed": failed_features,
                "total": len(feature_names)
            }
            config["update_history"].append(update_record)
            
            self._save_config(config)
            self._log_update(update_record)
            
            return {
                "status": "update_complete",
                "installed": installed_features,
                "failed": failed_features,
                "total_installed": len(installed_features)
            }
        
        except Exception as e:
            logger.error(f"Auto-install error: {e}")
            return {"status": "error", "message": str(e)}
    
    def _install_feature(self, feature_name: str) -> Dict[str, Any]:
        """Install a specific feature"""
        try:
            feature_implementations = {
                "web_search_integration": self._install_web_search,
                "web_automation": self._install_web_automation,
                "api_integrations": self._install_api_integrations,
                "payment_gateway": self._install_payment_gateway,
                "sentiment_analysis": self._install_sentiment_analysis,
                "email_integration": self._install_email_integration,
                "calendar_sync": self._install_calendar_sync,
                "weather_service": self._install_weather_service,
                "music_streaming": self._install_music_streaming,
                "video_streaming": self._install_video_streaming,
            }
            
            if feature_name in feature_implementations:
                return feature_implementations[feature_name]()
            else:
                return {"status": "error", "error": f"Unknown feature: {feature_name}"}
        
        except Exception as e:
            logger.error(f"Feature installation error: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_web_search(self) -> Dict[str, Any]:
        """Install web search integration"""
        try:
            self._install_packages(["googlesearch-python", "beautifulsoup4", "requests"])
            
            # Create web search module
            web_search_code = '''"""Web Search Integration"""
import requests
from googlesearch import search
from bs4 import BeautifulSoup
import logging

class WebSearchEngine:
    def search(self, query, num_results=5):
        """Perform web search"""
        try:
            results = []
            for url in search(query, num_results=num_results, advanced=True):
                results.append({"url": url})
            return results
        except Exception as e:
            logging.error(f"Search error: {e}")
            return []
    
    def get_page_content(self, url):
        """Extract content from webpage"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            return text[:1000]
        except Exception as e:
            logging.error(f"Content extraction error: {e}")
            return ""
'''
            
            with open("web_search.py", "w") as f:
                f.write(web_search_code)
            
            logger.info("Web search integration installed")
            return {"status": "success", "feature": "web_search_integration"}
        
        except Exception as e:
            logger.error(f"Web search installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_web_automation(self) -> Dict[str, Any]:
        """Install web automation (Selenium/Playwright)"""
        try:
            self._install_packages(["playwright", "selenium"])
            
            # Initialize playwright browsers
            subprocess.run(["playwright", "install"], capture_output=True)
            
            web_automation_code = '''"""Web Automation Module"""
from playwright.sync_api import sync_playwright
import logging

class WebAutomation:
    def __init__(self):
        self.browser = None
        self.page = None
    
    def open_browser(self, url):
        """Open browser and navigate to URL"""
        try:
            p = sync_playwright().start()
            self.browser = p.chromium.launch()
            self.page = self.browser.new_page()
            self.page.goto(url)
            return True
        except Exception as e:
            logging.error(f"Browser open error: {e}")
            return False
    
    def fill_form(self, form_data):
        """Fill form fields"""
        try:
            for field, value in form_data.items():
                self.page.fill(f"[name='{field}']", value)
            return True
        except Exception as e:
            logging.error(f"Form fill error: {e}")
            return False
    
    def click_button(self, selector):
        """Click button"""
        try:
            self.page.click(selector)
            return True
        except Exception as e:
            logging.error(f"Click error: {e}")
            return False
    
    def get_page_content(self):
        """Get page HTML"""
        return self.page.content() if self.page else ""
    
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
'''
            
            with open("web_automation.py", "w") as f:
                f.write(web_automation_code)
            
            logger.info("Web automation installed")
            return {"status": "success", "feature": "web_automation"}
        
        except Exception as e:
            logger.error(f"Web automation installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_api_integrations(self) -> Dict[str, Any]:
        """Install API integration framework"""
        try:
            self._install_packages(["aiohttp", "httpx", "tweepy", "praw", "stripe"])
            
            api_code = '''"""API Integration Framework"""
import aiohttp
import asyncio
import logging

class APIManager:
    def __init__(self):
        self.apis = {}
    
    def register_api(self, name, base_url, auth_key=None):
        """Register new API"""
        self.apis[name] = {
            "base_url": base_url,
            "auth_key": auth_key
        }
    
    async def call_api(self, api_name, endpoint, method="GET", params=None):
        """Call registered API"""
        try:
            if api_name not in self.apis:
                return {"error": "API not found"}
            
            api = self.apis[api_name]
            url = f"{api['base_url']}{endpoint}"
            headers = {"Authorization": f"Bearer {api['auth_key']}"} if api.get("auth_key") else {}
            
            async with aiohttp.ClientSession() as session:
                if method == "GET":
                    async with session.get(url, params=params, headers=headers) as resp:
                        return await resp.json()
                elif method == "POST":
                    async with session.post(url, json=params, headers=headers) as resp:
                        return await resp.json()
        except Exception as e:
            logging.error(f"API call error: {e}")
            return {"error": str(e)}
'''
            
            with open("api_manager.py", "w") as f:
                f.write(api_code)
            
            logger.info("API integration installed")
            return {"status": "success", "feature": "api_integrations"}
        
        except Exception as e:
            logger.error(f"API integration installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_payment_gateway(self) -> Dict[str, Any]:
        """Install payment gateway integration"""
        try:
            self._install_packages(["stripe", "paypalrestsdk"])
            
            payment_code = '''"""Payment Gateway Integration"""
import stripe
import logging

class PaymentGateway:
    def __init__(self, stripe_key=None):
        if stripe_key:
            stripe.api_key = stripe_key
    
    def process_payment(self, amount, currency, token):
        """Process payment"""
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency=currency,
                source=token
            )
            return {"status": "success", "charge_id": charge.id}
        except Exception as e:
            logging.error(f"Payment error: {e}")
            return {"status": "error", "error": str(e)}
    
    def create_subscription(self, customer_id, plan_id):
        """Create subscription"""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": plan_id}]
            )
            return {"status": "success", "subscription_id": subscription.id}
        except Exception as e:
            logging.error(f"Subscription error: {e}")
            return {"status": "error", "error": str(e)}
'''
            
            with open("payment_gateway.py", "w") as f:
                f.write(payment_code)
            
            logger.info("Payment gateway installed")
            return {"status": "success", "feature": "payment_gateway"}
        
        except Exception as e:
            logger.error(f"Payment gateway installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_sentiment_analysis(self) -> Dict[str, Any]:
        """Install advanced sentiment analysis"""
        try:
            self._install_packages(["transformers", "torch", "vader-sentiment"])
            
            sentiment_code = '''"""Advanced Sentiment Analysis"""
from transformers import pipeline
from textblob import TextBlob
import logging

class SentimentAnalyzer:
    def __init__(self):
        self.nlp_sentiment = pipeline("sentiment-analysis")
    
    def analyze(self, text):
        """Analyze sentiment with emotion detection"""
        try:
            # Using transformer model
            result = self.nlp_sentiment(text[:512])[0]
            
            # Also use TextBlob for additional metrics
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            return {
                "emotion": result["label"],
                "confidence": result["score"],
                "polarity": polarity,
                "subjectivity": subjectivity,
                "sentiment": "positive" if polarity > 0.1 else "negative" if polarity < -0.1 else "neutral"
            }
        except Exception as e:
            logging.error(f"Sentiment analysis error: {e}")
            return {}
'''
            
            with open("sentiment_analyzer.py", "w") as f:
                f.write(sentiment_code)
            
            logger.info("Sentiment analysis installed")
            return {"status": "success", "feature": "sentiment_analysis"}
        
        except Exception as e:
            logger.error(f"Sentiment analysis installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_email_integration(self) -> Dict[str, Any]:
        """Install email integration"""
        try:
            self._install_packages(["secure-smtplib"])
            
            email_code = '''"""Email Integration"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class EmailClient:
    def __init__(self, email, password, smtp_server="smtp.gmail.com"):
        self.email = email
        self.password = password
        self.smtp_server = smtp_server
    
    def send_email(self, to, subject, body):
        """Send email"""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))
            
            with smtplib.SMTP_SSL(self.smtp_server, 465) as server:
                server.login(self.email, self.password)
                server.send_message(msg)
            
            return {"status": "success"}
        except Exception as e:
            logging.error(f"Email send error: {e}")
            return {"status": "error", "error": str(e)}
'''
            
            with open("email_client.py", "w") as f:
                f.write(email_code)
            
            logger.info("Email integration installed")
            return {"status": "success", "feature": "email_integration"}
        
        except Exception as e:
            logger.error(f"Email integration installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_calendar_sync(self) -> Dict[str, Any]:
        """Install calendar synchronization"""
        try:
            self._install_packages(["google-auth-oauthlib", "google-auth-httplib2", "google-api-python-client"])
            
            calendar_code = '''"""Calendar Synchronization"""
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import calendar_v3
import logging

class CalendarSync:
    def __init__(self):
        self.service = None
    
    def authenticate(self):
        """Authenticate with Google Calendar"""
        try:
            SCOPES = ["https://www.googleapis.com/auth/calendar"]
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server()
            self.service = calendar_v3.build("calendar", "v3", credentials=creds)
            return True
        except Exception as e:
            logging.error(f"Auth error: {e}")
            return False
    
    def get_events(self, days=7):
        """Get upcoming events"""
        try:
            from datetime import datetime, timedelta
            now = datetime.utcnow().isoformat() + "Z"
            end = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"
            
            events = self.service.events().list(
                calendarId="primary",
                timeMin=now,
                timeMax=end,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            
            return events.get("items", [])
        except Exception as e:
            logging.error(f"Get events error: {e}")
            return []
'''
            
            with open("calendar_sync.py", "w") as f:
                f.write(calendar_code)
            
            logger.info("Calendar sync installed")
            return {"status": "success", "feature": "calendar_sync"}
        
        except Exception as e:
            logger.error(f"Calendar sync installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_weather_service(self) -> Dict[str, Any]:
        """Install weather service"""
        try:
            self._install_packages(["openweathermap"])
            
            weather_code = '''"""Weather Service Integration"""
import requests
import logging

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_weather(self, city):
        """Get weather for city"""
        try:
            params = {"q": city, "appid": self.api_key, "units": "metric"}
            response = requests.get(f"{self.base_url}/weather", params=params)
            return response.json()
        except Exception as e:
            logging.error(f"Weather API error: {e}")
            return {}
    
    def get_forecast(self, city, days=5):
        """Get weather forecast"""
        try:
            params = {"q": city, "appid": self.api_key, "units": "metric", "cnt": days*8}
            response = requests.get(f"{self.base_url}/forecast", params=params)
            return response.json()
        except Exception as e:
            logging.error(f"Forecast error: {e}")
            return {}
'''
            
            with open("weather_service.py", "w") as f:
                f.write(weather_code)
            
            logger.info("Weather service installed")
            return {"status": "success", "feature": "weather_service"}
        
        except Exception as e:
            logger.error(f"Weather service installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_music_streaming(self) -> Dict[str, Any]:
        """Install music streaming integration"""
        try:
            self._install_packages(["spotipy"])
            
            music_code = '''"""Music Streaming Integration"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging

class MusicStreaming:
    def __init__(self, client_id, client_secret):
        auth = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth)
    
    def search_track(self, query):
        """Search for track"""
        try:
            results = self.sp.search(q=query, type="track", limit=5)
            return results.get("tracks", {}).get("items", [])
        except Exception as e:
            logging.error(f"Search error: {e}")
            return []
    
    def get_recommendations(self, track_id):
        """Get track recommendations"""
        try:
            recommendations = self.sp.recommendations(seed_tracks=[track_id])
            return recommendations.get("tracks", [])
        except Exception as e:
            logging.error(f"Recommendation error: {e}")
            return []
'''
            
            with open("music_streaming.py", "w") as f:
                f.write(music_code)
            
            logger.info("Music streaming installed")
            return {"status": "success", "feature": "music_streaming"}
        
        except Exception as e:
            logger.error(f"Music streaming installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_video_streaming(self) -> Dict[str, Any]:
        """Install video streaming integration"""
        try:
            self._install_packages(["pytube", "youtube-search-python"])
            
            video_code = '''"""Video Streaming Integration"""
from pytube import YouTube
from yt_search import YoutubeSearch
import logging

class VideoStreaming:
    def search_youtube(self, query):
        """Search YouTube"""
        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
            return results
        except Exception as e:
            logging.error(f"YouTube search error: {e}")
            return []
    
    def get_video_url(self, youtube_url):
        """Get video download URL"""
        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.get_highest_resolution()
            return stream.url
        except Exception as e:
            logging.error(f"Video URL error: {e}")
            return ""
'''
            
            with open("video_streaming.py", "w") as f:
                f.write(video_code)
            
            logger.info("Video streaming installed")
            return {"status": "success", "feature": "video_streaming"}
        
        except Exception as e:
            logger.error(f"Video streaming installation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _install_packages(self, packages: List[str]):
        """Install Python packages"""
        for package in packages:
            try:
                subprocess.run(
                    ["pip", "install", package],
                    capture_output=True,
                    timeout=60
                )
                logger.info(f"Installed package: {package}")
            except Exception as e:
                logger.warning(f"Failed to install {package}: {e}")
    
    def _backup_system(self):
        """Backup system before update"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"backups/backup_{timestamp}"
            
            os.makedirs(backup_dir, exist_ok=True)
            
            # Copy important files
            important_files = [
                "voice_assistant.py",
                "nlp_processor.py",
                "task_executor.py",
                "contacts.json",
                "learning_database.json"
            ]
            
            for file in important_files:
                if os.path.exists(file):
                    subprocess.run(["cp", file, f"{backup_dir}/{file}"], capture_output=True)
            
            logger.info(f"System backed up to {backup_dir}")
            return {"status": "success", "backup_dir": backup_dir}
        
        except Exception as e:
            logger.warning(f"Backup failed: {e}")
            return {"status": "error"}
    
    def _load_config(self) -> Dict:
        """Load update config"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def _save_config(self, config: Dict):
        """Save update config"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Config save error: {e}")
    
    def _load_update_log(self) -> Dict:
        """Load update log"""
        try:
            if os.path.exists(self.update_log_file):
                with open(self.update_log_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"updates": []}
    
    def _save_update_log(self, log: Dict):
        """Save update log"""
        try:
            with open(self.update_log_file, 'w') as f:
                json.dump(log, f, indent=2)
        except Exception as e:
            logger.error(f"Log save error: {e}")
    
    def _log_update(self, update_record: Dict):
        """Log update record"""
        try:
            log = self._load_update_log()
            log["updates"].append(update_record)
            self._save_update_log(log)
        except Exception as e:
            logger.error(f"Update logging error: {e}")


class SelfLearningSystem:
    """Self-learning system that improves without manual intervention"""
    
    def __init__(self):
        self.learning_file = "self_learning.json"
        self.pattern_db = self._load_patterns()
    
    def learn_from_interaction(self, command: str, response: str, success: bool):
        """Learn from each interaction"""
        try:
            pattern = {
                "command": command,
                "response": response,
                "success": success,
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.5 if not success else 0.9
            }
            
            if "patterns" not in self.pattern_db:
                self.pattern_db["patterns"] = []
            
            self.pattern_db["patterns"].append(pattern)
            self._save_patterns()
            
            logger.info(f"Learned pattern from: {command[:50]}")
            
            return {"status": "learned"}
        
        except Exception as e:
            logger.error(f"Learning error: {e}")
            return {"status": "error", "error": str(e)}
    
    def improve_intent_detection(self):
        """Improve intent detection based on learned patterns"""
        try:
            patterns = self.pattern_db.get("patterns", [])
            
            if len(patterns) < 10:
                return {"status": "insufficient_data"}
            
            # Analyze patterns
            success_patterns = [p for p in patterns if p["success"]]
            failed_patterns = [p for p in patterns if not p["success"]]
            
            improvements = {
                "success_rate": len(success_patterns) / len(patterns),
                "total_learned": len(patterns),
                "areas_to_improve": len(failed_patterns),
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "status": "improved",
                "improvements": improvements
            }
        
        except Exception as e:
            logger.error(f"Improvement error: {e}")
            return {"status": "error", "error": str(e)}
    
    def _load_patterns(self) -> Dict:
        """Load learned patterns"""
        try:
            if os.path.exists(self.learning_file):
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"patterns": []}
    
    def _save_patterns(self):
        """Save learned patterns"""
        try:
            with open(self.learning_file, 'w') as f:
                json.dump(self.pattern_db, f, indent=2)
        except Exception as e:
            logger.error(f"Pattern save error: {e}")
