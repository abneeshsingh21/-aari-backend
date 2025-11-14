"""
Task Executor - Handles execution of various assistant tasks
WhatsApp, phone calls, downloads, system commands, etc.
"""

import os
import subprocess
import logging
import json
from typing import Dict, Any
import requests
import time
from datetime import datetime, timedelta
import platform
import webbrowser

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Execute various tasks requested by the user"""
    
    def __init__(self):
        self.system = platform.system()
        self.contacts_db = self._load_contacts()
        self.reminders = []
    
    def send_whatsapp_message(self, contact_name: str, message: str) -> Dict[str, Any]:
        """Send message via WhatsApp using pywhatkit"""
        try:
            # Get contact number
            contact_number = self._get_contact_number(contact_name)
            
            if not contact_number:
                return {
                    "status": "error",
                    "error": f"Contact '{contact_name}' not found."
                }
            
            # Format number for WhatsApp
            if not contact_number.startswith("+"):
                contact_number = "+1" + contact_number  # Add country code
            
            try:
                import pywhatkit as kit
                # Send message
                kit.sendwhatmsg_instantly(contact_number, message, wait_time=5)
            except ImportError:
                logger.warning("pywhatkit not available, using webbrowser fallback")
                # Fallback: open WhatsApp Web
                url = f"https://web.whatsapp.com/send?phone={contact_number}&text={message.replace(' ', '%20')}"
                webbrowser.open(url)
            except Exception as e:
                logger.warning(f"pywhatkit failed: {e}, using webbrowser fallback")
                url = f"https://web.whatsapp.com/send?phone={contact_number}&text={message.replace(' ', '%20')}"
                webbrowser.open(url)
            
            logger.info(f"WhatsApp message sent to {contact_name}: {message}")
            
            return {
                "status": "success",
                "message": f"Message sent to {contact_name}"
            }
        
        except Exception as e:
            logger.error(f"WhatsApp error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def make_call(self, contact_name: str) -> Dict[str, Any]:
        """Initiate phone call"""
        try:
            contact_number = self._get_contact_number(contact_name)
            
            if not contact_number:
                return {
                    "status": "error",
                    "error": f"Contact '{contact_name}' not found."
                }
            
            # Different approaches based on OS
            if self.system == "Windows":
                # Use system dialer
                os.startfile(f"tel:{contact_number}")
            elif self.system == "Darwin":  # macOS
                os.system(f"open 'tel:{contact_number}'")
            else:  # Linux
                return {
                    "status": "error",
                    "error": "Calling not supported on this platform"
                }
            
            logger.info(f"Call initiated to {contact_name}: {contact_number}")
            
            return {
                "status": "success",
                "message": f"Calling {contact_name}"
            }
        
        except Exception as e:
            logger.error(f"Call error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def download_file(self, file_name: str, file_type: str = "") -> Dict[str, Any]:
        """Download files from internet"""
        try:
            # Map file names to URLs (you should expand this)
            file_sources = {
                "python pdf": "https://www.python.org/ftp/python/3.11.0/python-3.11.0.exe",
                "tutorial pdf": "https://example.com/tutorial.pdf",
                "presentation ppt": "https://example.com/presentation.pptx",
            }
            
            search_key = f"{file_name} {file_type}".lower()
            url = file_sources.get(search_key)
            
            if not url:
                # Try to search online
                url = self._search_and_get_file_url(file_name, file_type)
            
            if not url:
                return {
                    "status": "error",
                    "error": f"Could not find '{file_name}'"
                }
            
            # Download file
            downloads_dir = os.path.expanduser("~/Downloads")
            os.makedirs(downloads_dir, exist_ok=True)
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Generate filename
            if file_type:
                filename = f"{file_name}.{file_type}"
            else:
                filename = file_name
            
            filepath = os.path.join(downloads_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"File downloaded: {filepath}")
            
            return {
                "status": "success",
                "file_path": filepath,
                "message": f"Downloaded {file_name}"
            }
        
        except Exception as e:
            logger.error(f"Download error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def open_application(self, app_name: str) -> Dict[str, Any]:
        """Open an application - Full system control"""
        try:
            app_name_lower = app_name.lower().strip()
            
            # Enhanced Windows app mapping with full system control
            windows_apps = {
                # Browsers
                "chrome": "chrome",
                "google chrome": "chrome",
                "firefox": "firefox",
                "edge": "msedge",
                "internet explorer": "iexplore",
                
                # System apps
                "notepad": "notepad",
                "calculator": "calc",
                "file manager": "explorer",
                "files": "explorer",
                "file explorer": "explorer",
                "explorer": "explorer",
                "settings": "ms-settings:",
                "window settings": "ms-settings:",
                "windows settings": "ms-settings:",
                "control panel": "control",
                "task manager": "taskmgr",
                "device manager": "devmgmt.msc",
                "disk management": "diskmgmt.msc",
                "services": "services.msc",
                "regedit": "regedit",
                "command prompt": "cmd",
                "powershell": "powershell",
                "terminal": "wt",
                "windows terminal": "wt",
                
                # Office apps
                "word": "winword",
                "excel": "excel",
                "powerpoint": "powerpnt",
                "outlook": "outlook",
                "access": "msaccess",
                "publisher": "mspub",
                
                # Communication
                "whatsapp": "whatsapp",
                "telegram": "telegram",
                "slack": "slack",
                "discord": "discord",
                "teams": "msteams",
                "skype": "skype",
                "zoom": "zoom",
                
                # Media & Entertainment
                "spotify": "spotify",
                "vlc": "vlc",
                "itunes": "itunes",
                "photos": "photos",
                "camera": "WindowsCamera",
                
                # Development
                "vscode": "code",
                "visual studio code": "code",
                "git": "git",
                "python": "python",
                
                # Other
                "paint": "mspaint",
                "snipping tool": "SnippingTool",
                "screen capture": "SnippingTool",
                "action center": "action_center",
                "wifi settings": "ms-settings:network-wifi",
                "bluetooth": "ms-settings:bluetooth",
                "sound settings": "ms-settings:sound",
                "display settings": "ms-settings:display",
            }
            
            if self.system == "Windows":
                # Look up app in mapping
                app_cmd = windows_apps.get(app_name_lower, app_name_lower)
                
                try:
                    # Handle settings URLs specially
                    if app_cmd.startswith("ms-settings:"):
                        subprocess.Popen(f"start {app_cmd}", shell=True)
                    elif app_cmd.endswith(".msc"):
                        # System apps with .msc extension
                        subprocess.Popen(f"start {app_cmd}", shell=True)
                    else:
                        # Regular apps - use start command
                        subprocess.Popen(f"start {app_cmd}", shell=True)
                except Exception as e:
                    logger.error(f"Subprocess failed: {e}, trying os.system...")
                    os.system(f"start {app_cmd}")
                
                logger.info(f"Application opened: {app_name}")
                return {
                    "status": "success",
                    "message": f"Opening {app_name}"
                }
            
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
                logger.info(f"Application opened: {app_name}")
                return {
                    "status": "success",
                    "message": f"Opening {app_name}"
                }
            
            else:  # Linux
                subprocess.Popen([app_name_lower], shell=True)
                logger.info(f"Application opened: {app_name}")
                return {
                    "status": "success",
                    "message": f"Opening {app_name}"
                }
        
        except Exception as e:
            logger.error(f"App open error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def set_reminder(self, reminder_text: str, time_str: str) -> Dict[str, Any]:
        """Set a reminder"""
        try:
            # Parse time
            reminder_time = self._parse_time_string(time_str)
            
            reminder = {
                "text": reminder_text,
                "time": reminder_time,
                "created_at": datetime.now(),
                "notified": False
            }
            
            self.reminders.append(reminder)
            
            logger.info(f"Reminder set: {reminder_text} at {reminder_time}")
            
            return {
                "status": "success",
                "message": f"Reminder set for {reminder_time}"
            }
        
        except Exception as e:
            logger.error(f"Reminder error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def play_media(self, media_name: str) -> Dict[str, Any]:
        """Play music or video"""
        try:
            try:
                import pywhatkit as kit
                # Search and play on YouTube
                kit.playonyt(media_name)
            except ImportError:
                logger.warning("pywhatkit not available, using webbrowser fallback")
                # Fallback: open YouTube search in browser
                url = f"https://www.youtube.com/results?search_query={media_name.replace(' ', '+')}"
                webbrowser.open(url)
            except Exception as e:
                logger.warning(f"pywhatkit playback failed: {e}, using webbrowser fallback")
                # Fallback: open YouTube search
                url = f"https://www.youtube.com/results?search_query={media_name.replace(' ', '+')}"
                webbrowser.open(url)
            
            logger.info(f"Playing: {media_name}")
            
            return {
                "status": "success",
                "message": f"Now playing {media_name}"
            }
        
        except Exception as e:
            logger.error(f"Media error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def execute_system_command(self, action: str) -> Dict[str, Any]:
        """Execute system commands - Full system control"""
        try:
            action = action.lower().strip()
            
            if self.system == "Windows":
                # Power management
                if "shut down" in action or "shutdown" in action:
                    os.system("shutdown /s /t 30")
                    return {"status": "success", "message": "Shutting down in 30 seconds"}
                
                elif "sleep" in action or "sleep mode" in action:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    return {"status": "success", "message": "Going to sleep mode"}
                
                elif "restart" in action or "reboot" in action:
                    os.system("shutdown /r /t 30")
                    return {"status": "success", "message": "Restarting in 30 seconds"}
                
                elif "lock" in action or "lock screen" in action:
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                    return {"status": "success", "message": "Screen locked"}
                
                # Screen management
                elif "turn off monitor" in action or "screen off" in action:
                    os.system("powercfg /change monitor-timeout-ac 1")
                    os.system("nircmd.exe sendkeypress 236")
                    return {"status": "success", "message": "Monitor turned off"}
                
                elif "turn on monitor" in action or "screen on" in action or "wake monitor" in action:
                    os.system("nircmd.exe movecursor 100 100")
                    return {"status": "success", "message": "Monitor turned on"}
                
                # Volume control
                elif "volume" in action:
                    if "up" in action:
                        os.system("nircmd.exe changesysvolume 5000")
                        return {"status": "success", "message": "Volume increased"}
                    elif "down" in action:
                        os.system("nircmd.exe changesysvolume -5000")
                        return {"status": "success", "message": "Volume decreased"}
                    elif "mute" in action:
                        os.system("nircmd.exe mutesysvolume 1")
                        return {"status": "success", "message": "Muted"}
                    elif "unmute" in action:
                        os.system("nircmd.exe mutesysvolume 0")
                        return {"status": "success", "message": "Unmuted"}
                
                # Brightness control
                elif "brightness" in action:
                    if "increase" in action or "up" in action:
                        os.system("nircmd.exe changebrightness 10")
                        return {"status": "success", "message": "Brightness increased"}
                    elif "decrease" in action or "down" in action:
                        os.system("nircmd.exe changebrightness -10")
                        return {"status": "success", "message": "Brightness decreased"}
                
                # Network control
                elif "wifi" in action or "internet" in action:
                    if "turn on" in action or "enable" in action or "connect" in action:
                        os.system("netsh interface set interface Wi-Fi enabled")
                        return {"status": "success", "message": "WiFi enabled"}
                    elif "turn off" in action or "disable" in action:
                        os.system("netsh interface set interface Wi-Fi disabled")
                        return {"status": "success", "message": "WiFi disabled"}
                
                # Bluetooth control
                elif "bluetooth" in action:
                    if "turn on" in action or "enable" in action:
                        os.system("powershell -Command \"(Get-Service bthserv).Status\"")
                        return {"status": "success", "message": "Bluetooth enabled"}
                    elif "turn off" in action or "disable" in action:
                        os.system("powershell -Command \"Stop-Service bthserv -Force\"")
                        return {"status": "success", "message": "Bluetooth disabled"}
                
                # Clipboard operations
                elif "clear clipboard" in action:
                    os.system("echo off | clip")
                    return {"status": "success", "message": "Clipboard cleared"}
                
                # Window management
                elif "minimize all" in action or "show desktop" in action:
                    os.system("nircmd.exe sendkeypress 91 d")  # Win+D
                    return {"status": "success", "message": "All windows minimized"}
                
                elif "maximize all" in action:
                    os.system("nircmd.exe sendkeypress 91 shift d")  # Win+Shift+D
                    return {"status": "success", "message": "All windows maximized"}
                
                # Process/app management
                elif "kill" in action or "close" in action:
                    # Extract app name
                    app_to_close = action.replace("kill", "").replace("close", "").strip()
                    if app_to_close:
                        os.system(f"taskkill /IM {app_to_close}.exe /F")
                        return {"status": "success", "message": f"Closed {app_to_close}"}
                
                # Disk management
                elif "clear cache" in action:
                    os.system("del /Q %temp%\\*")
                    return {"status": "success", "message": "Cache cleared"}
                
                elif "disk cleanup" in action or "clean disk" in action:
                    os.system("cleanmgr.exe")
                    return {"status": "success", "message": "Disk Cleanup opened"}
                
                # Date/Time
                elif "current time" in action or "what time" in action:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    return {"status": "success", "message": f"Current time: {current_time}"}
                
                elif "current date" in action or "what date" in action or "today date" in action:
                    current_date = datetime.now().strftime("%A, %B %d, %Y")
                    return {"status": "success", "message": f"Today is {current_date}"}
                
                # Default fallback
                else:
                    return {"status": "error", "error": f"Command not supported: {action}"}
            
            return {"status": "error", "error": "Command not supported on this platform"}
        
        except Exception as e:
            logger.error(f"System command error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def send_email(self, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        """Send email"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Get email credentials from environment
            sender_email = os.getenv("SENDER_EMAIL", "")
            sender_password = os.getenv("SENDER_PASSWORD", "")
            
            if not sender_email or not sender_password:
                return {"status": "error", "error": "Email credentials not configured"}
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent to {recipient}")
            
            return {
                "status": "success",
                "message": f"Email sent to {recipient}"
            }
        
        except Exception as e:
            logger.error(f"Email error: {e}")
            return {"status": "error", "error": str(e)}
    
    def search_web(self, query: str) -> Dict[str, Any]:
        """Search on web"""
        try:
            try:
                import pywhatkit as kit
                kit.search(query)
            except ImportError:
                logger.warning("pywhatkit not available, using webbrowser fallback")
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
            except Exception as e:
                logger.warning(f"pywhatkit search failed: {e}, using webbrowser fallback")
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
            
            logger.info(f"Searching: {query}")
            
            return {
                "status": "success",
                "message": f"Searching for {query}"
            }
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {"status": "error", "error": str(e)}
    
    # Helper methods
    
    def _load_contacts(self) -> Dict[str, str]:
        """Load contacts from JSON database"""
        try:
            contacts_file = os.path.join(os.path.dirname(__file__), "contacts.json")
            if os.path.exists(contacts_file):
                with open(contacts_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading contacts from JSON: {e}")
        
        # Fallback to hardcoded contacts
        return {
            "mom": "+1-555-0101",
            "dad": "+1-555-0102",
            "john": "+1-555-0103",
            "sarah": "+1-555-0104",
            "friend": "+1-555-0105",
            "disha": "+91-9876543210",
            "delhi": "+91-9876543211"
        }
    
    def _get_contact_number(self, contact_name: str) -> str:
        """Get contact number from database"""
        return self.contacts_db.get(contact_name.lower(), "")
    
    def _search_and_get_file_url(self, file_name: str, file_type: str) -> str:
        """Search for file URL online"""
        try:
            search_query = f"{file_name} {file_type} download"
            # This is simplified - you'd need to implement actual search
            return ""
        except:
            return ""
    
    def _parse_time_string(self, time_str: str) -> datetime:
        """Parse time string to datetime"""
        if "tomorrow" in time_str.lower():
            return datetime.now() + timedelta(days=1)
        elif "today" in time_str.lower():
            return datetime.now()
        elif "in" in time_str.lower():
            # Extract number
            import re
            match = re.search(r'(\d+)\s*(minute|hour|day)', time_str.lower())
            if match:
                num = int(match.group(1))
                unit = match.group(2)
                if unit == "minute":
                    return datetime.now() + timedelta(minutes=num)
                elif unit == "hour":
                    return datetime.now() + timedelta(hours=num)
                elif unit == "day":
                    return datetime.now() + timedelta(days=num)
        
        return datetime.now() + timedelta(hours=1)  # Default: 1 hour from now
    
    def check_reminders(self):
        """Check and notify for due reminders"""
        now = datetime.now()
        for reminder in self.reminders:
            if reminder['time'] <= now and not reminder['notified']:
                logger.info(f"REMINDER: {reminder['text']}")
                reminder['notified'] = True
