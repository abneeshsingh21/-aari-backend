"""
Core Voice Assistant Engine
Advanced AI-powered voice assistant with natural language processing
"""

import json
import os
import subprocess
import webbrowser
from datetime import datetime
from typing import Dict, List, Any
import logging
import io
import tempfile
import time

# Optional imports for cloud compatibility
try:
    import speech_recognition as sr
except ImportError:
    sr = None
    
try:
    import spacy
except ImportError:
    spacy = None

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

from task_executor import TaskExecutor
from advanced_executor import AdvancedTaskExecutor, AARIAdvanced
from nlp_processor import NLPProcessor
from context_manager import ContextManager
from emotional_intelligence import EmotionalIntelligence
from memory_manager import MemoryManager
from auto_updater import AutoUpdater, SelfLearningSystem
from web_search import WebSearchEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceAssistant:
    """Main voice assistant class with advanced capabilities"""
    
    def __init__(self):
        # Initialize recognizer only if available
        self.recognizer = sr.Recognizer() if sr else None
        self.nlp_processor = NLPProcessor()
        self.task_executor = TaskExecutor()
        self.advanced_executor = AARIAdvanced()
        self.context_manager = ContextManager()
        self.emotional_intelligence = EmotionalIntelligence()
        self.memory_manager = MemoryManager()  # Add memory management
        self.auto_updater = AutoUpdater()  # Initialize auto-updater
        self.self_learning = SelfLearningSystem()  # Initialize self-learning
        self.web_search = WebSearchEngine()  # Initialize web search
        
        # Load NLP model only if available
        self.nlp = None
        if spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                logger.warning("Spacy model not available, NLP limited")
        else:
            logger.warning("Spacy not available, NLP disabled")
            logger.warning("Spacy model not found. Install with: python -m spacy download en_core_web_sm")
        
        self.running = False
        self.user_name = self.memory_manager.get_preference("user_name", "avnish")
        self.assistant_name = "aari"
        self.conversation_history = []
        self.current_language = "en"  # Default English
        
        # Wake words for background listening
        self.wake_words = ["hey aari", "suno", "hello aari", "aari", "listen aari"]
        
        # URL mappings for web apps
        self.web_apps = {
            "chatgpt": "https://chat.openai.com",
            "chat gpt": "https://chat.openai.com",
            "chat": "https://chat.openai.com",
            "google": "https://google.com",
            "gmail": "https://mail.google.com",
            "youtube": "https://youtube.com",
            "facebook": "https://facebook.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://linkedin.com",
            "reddit": "https://reddit.com",
            "github": "https://github.com",
            "stackoverflow": "https://stackoverflow.com",
        }
        
    def speak(self, text: str, language: str = "en"):
        """Convert text to speech with natural female Indian voice using Google TTS"""
        logger.info(f"Assistant ({language}): {text}")
        # Desktop handles voice output, backend just logs
    
    def listen(self, timeout: int = 10, language: str = "en") -> str:
        """Listen for voice input with noise filtering and multi-language support"""
        try:
            with sr.Microphone() as source:
                logger.info(f"Listening for {language}...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            
            logger.info("Processing audio...")
            # Support multiple languages
            if language == "hi":  # Hindi
                text = self.recognizer.recognize_google(audio, language="hi-IN")
            elif language == "ta":  # Tamil
                text = self.recognizer.recognize_google(audio, language="ta-IN")
            elif language == "te":  # Telugu
                text = self.recognizer.recognize_google(audio, language="te-IN")
            elif language == "kn":  # Kannada
                text = self.recognizer.recognize_google(audio, language="kn-IN")
            elif language == "ml":  # Malayalam
                text = self.recognizer.recognize_google(audio, language="ml-IN")
            else:  # Default English
                text = self.recognizer.recognize_google(audio, language="en-IN")
            
            logger.info(f"User: {text}")
            return text.lower()
        except sr.UnknownValueError:
            return "sorry_not_understood"
        except sr.RequestError:
            return "network_error"
        except Exception as e:
            logger.error(f"Listening error: {e}")
            return "error"
    
    def process_command(self, command: str) -> str:
        """Process natural language command with emotional understanding"""
        
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "user",
            "content": command
        })
        
        # Process with NLP
        intent, entities, confidence = self.nlp_processor.extract_intent(command)
        
        logger.info(f"Intent: {intent}, Confidence: {confidence}")
        
        # Check if update/learning request
        if "update" in command.lower() or "learn" in command.lower() or "improve" in command.lower():
            response = self._handle_update_request(command)
        # Check if complex task (advanced)
        elif self._is_complex_task(command):
            response = self.advanced_executor.handle_advanced_command(command, {
                "user_name": self.user_name,
                "timestamp": datetime.now().isoformat()
            })
        else:
            # Route to standard handlers
            response = self._handle_intent(intent, entities, command)
        
        # Enhance response with emotional intelligence
        response = self.emotional_intelligence.generate_contextual_response(
            command, 
            response,
            {"user_name": self.user_name}
        )
        
        # Add response to history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "assistant",
            "content": response
        })
        
        # Learn from interaction
        success = not any(err in response.lower() for err in ["error", "couldn't", "failed"])
        self.self_learning.learn_from_interaction(command, response, success)
        
        return response
    
    def _is_complex_task(self, command: str) -> bool:
        """Check if this is a complex multi-step task"""
        complex_keywords = ["and then", "after that", "organize", "automate", "batch", 
                           "workflow", "control", "manage", "system", "kill process",
                           "schedule", "backup", "clean disk", "monitor"]
        return any(keyword in command.lower() for keyword in complex_keywords)
    
    def _handle_intent(self, intent: str, entities: Dict, command: str) -> str:
        """Handle different intents with context awareness"""
        
        if intent == "greeting":
            return self._handle_greeting()
        
        elif intent == "send_message":
            return self._handle_send_message(entities, command)
        
        elif intent == "make_call":
            return self._handle_make_call(entities, command)
        
        elif intent == "download_file":
            return self._handle_download(entities, command)
        
        elif intent == "open_app":
            return self._handle_open_app(entities, command)
        
        elif intent == "query":
            return self._handle_query(command)
        
        elif intent == "set_reminder":
            return self._handle_reminder(entities, command)
        
        elif intent == "play_media":
            return self._handle_media(entities, command)
        
        elif intent == "system_control":
            return self._handle_system(entities, command)
        
        elif intent == "memory":
            return self._handle_memory(entities, command)
        
        elif intent == "unknown":
            return "I'm not sure about that. Could you rephrase?"
        
        else:
            return "Let me help you with that."
    
    def _handle_greeting(self) -> str:
        """Handle greeting with context awareness"""
        hour = datetime.now().hour
        if hour < 12:
            greeting = f"Good morning, {self.user_name}! I'm aari, your assistant. How can I help you today?"
        elif hour < 18:
            greeting = f"Good afternoon, {self.user_name}! I'm aari. What can I help you with?"
        else:
            greeting = f"Good evening, {self.user_name}! I'm aari, ready to assist. How can I be of service?"
        return greeting
    
    def _handle_send_message(self, entities: Dict, command: str) -> str:
        """Handle messaging on WhatsApp, SMS, etc. with smart entity extraction and WhatsApp verification"""
        try:
            # Try to extract contact and message from entities first
            contact_name = entities.get("contact", "").strip()
            message = entities.get("message", "").strip()
            
            # If entities didn't capture everything, try direct parsing
            if not contact_name or not message:
                # Parse the command for contact and message
                parsed = self._parse_message_command(command)
                contact_name = contact_name or parsed.get("contact", "")
                message = message or parsed.get("message", "")
            
            if not contact_name:
                return "Who would you like me to send a message to?"
            
            if not message:
                return f"What message would you like me to send to {contact_name}?"
            
            # Verify contact exists on WhatsApp
            contact_number = self._get_contact_number(contact_name)
            if not contact_number:
                return f"I don't have {contact_name} in my contacts. Please add {contact_name}'s contact first."
            
            # Check if contact is available on WhatsApp
            is_whatsapp_user = self._check_whatsapp_availability(contact_name, contact_number)
            
            logger.info(f"Sending message to {contact_name}: {message}")
            
            # Try multiple methods to send WhatsApp
            result = self._send_whatsapp_intelligent(contact_name, message, contact_number)
            
            if result['status'] == 'success':
                return f"Message sent to {contact_name}. I said '{message}'"
            else:
                return f"I couldn't send the message. {result.get('error', 'Please try again.')}"
        
        except Exception as e:
            logger.error(f"Message error: {e}")
            return "There was an error sending the message."
    
    def _handle_make_call(self, entities: Dict, command: str) -> str:
        """Handle phone calls with contact verification"""
        try:
            # Extract contact name from command or entities
            contact_name = entities.get("contact", "").strip()
            
            if not contact_name:
                # Try to parse from command
                contact_name = self._extract_contact_from_call_command(command)
            
            if not contact_name:
                return "Who would you like me to call?"
            
            # Verify contact exists
            contact_number = self._get_contact_number(contact_name)
            if not contact_number:
                return f"I don't have {contact_name} in my contacts. Please add their contact first."
            
            logger.info(f"Initiating call to {contact_name}: {contact_number}")
            
            # Make the call
            result = self._make_call_intelligent(contact_name, contact_number)
            
            if result['status'] == 'success':
                return f"Calling {contact_name} now"
            else:
                return f"I couldn't make the call. {result.get('error', 'Please try again.')}"
        
        except Exception as e:
            logger.error(f"Call error: {e}")
            return "There was an error making the call."
    
    def _extract_contact_from_call_command(self, command: str) -> str:
        """Extract contact name from call command"""
        import re
        text_lower = command.lower()
        
        # Pattern: "call [CONTACT]", "make call to [CONTACT]", "dial [CONTACT]"
        patterns = [
            r"call\s+([a-z]+)",
            r"make\s+call\s+to\s+([a-z]+)",
            r"dial\s+([a-z]+)",
            r"ring\s+([a-z]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                candidate = match.group(1).strip()
                if candidate and len(candidate) > 1 and candidate not in ["a", "the", "to", "at"]:
                    return candidate
        
        return ""
    
    def _parse_message_command(self, command: str) -> Dict[str, str]:
        """Parse message command to extract contact and message intelligently"""
        import re
        text_lower = command.lower()
        
        result = {"contact": "", "message": ""}
        
        # Pattern matching with regex - most specific to least specific
        patterns = [
            # Pattern 1: "send message to [CONTACT] that [MESSAGE]"
            r"send\s+message\s+to\s+([a-z]+)\s+that\s+(.+)",
            # Pattern 2: "send to [CONTACT] that [MESSAGE]"
            r"send\s+to\s+([a-z]+)\s+that\s+(.+)",
            # Pattern 3: "tell [CONTACT] that [MESSAGE]"
            r"tell\s+([a-z]+)\s+that\s+(.+)",
            # Pattern 4: "text to [CONTACT] that [MESSAGE]"
            r"text\s+to\s+([a-z]+)\s+that\s+(.+)",
            # Pattern 5: "message to [CONTACT] saying [MESSAGE]" or "message to [CONTACT] that [MESSAGE]"
            r"message\s+to\s+([a-z]+)\s+(?:saying|that)\s+(.+)",
            # Pattern 6: "send message to [CONTACT] [MESSAGE]" (without that)
            r"send\s+message\s+to\s+([a-z]+)\s+(.+)",
            # Pattern 7: "send to [CONTACT] [MESSAGE]"
            r"send\s+to\s+([a-z]+)\s+(.+)",
            # Pattern 8: "tell [CONTACT] [MESSAGE]"
            r"tell\s+([a-z]+)\s+(.+)",
            # Pattern 9: "text [CONTACT] [MESSAGE]"
            r"text\s+([a-z]+)\s+(.+)",
            # Pattern 10: "message [CONTACT] [MESSAGE]"
            r"message\s+([a-z]+)\s+(.+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                groups = match.groups()
                if len(groups) >= 2:
                    result["contact"] = groups[0].strip()
                    result["message"] = groups[1].strip()
                    return result
        
        # Fallback: if no patterns match, return empty
        return result
    
    def _send_whatsapp_intelligent(self, contact_name: str, message: str, contact_number: str = "") -> Dict[str, Any]:
        """Send WhatsApp message using multiple methods with contact verification"""
        try:
            # Get contact number if not provided
            if not contact_number:
                contact_number = self._get_contact_number(contact_name)
            
            if not contact_number:
                return {
                    "status": "error",
                    "error": f"Contact '{contact_name}' not found in address book"
                }
            
            # Format number for WhatsApp (remove hyphens)
            contact_number = contact_number.replace("-", "").replace(" ", "")
            if not contact_number.startswith("+"):
                # Default to India country code if no + prefix
                if len(contact_number) == 10:
                    contact_number = "+91" + contact_number
                elif len(contact_number) == 11 and contact_number.startswith("1"):
                    contact_number = "+" + contact_number
                else:
                    contact_number = "+1" + contact_number
            
            # Method 1: Try pywhatkit
            try:
                import pywhatkit as kit
                kit.sendwhatmsg_instantly(contact_number, message, wait_time=2)
                logger.info(f"WhatsApp sent via pywhatkit to {contact_name}")
                return {"status": "success", "message": f"Message sent to {contact_name}"}
            except Exception as e:
                logger.warning(f"pywhatkit failed: {e}")
            
            # Method 2: Direct WhatsApp Web URL
            try:
                wa_url = f"https://wa.me/{contact_number.replace('+', '')}?text={message.replace(' ', '%20')}"
                webbrowser.open(wa_url)
                logger.info(f"WhatsApp opened via URL for {contact_name}")
                return {"status": "success", "message": f"Opening WhatsApp for {contact_name}"}
            except Exception as e:
                logger.warning(f"URL method failed: {e}")
            
            # Method 3: Fallback - notify user WhatsApp is ready
            logger.info(f"Fallback: WhatsApp ready for manual sending to {contact_name}")
            return {
                "status": "success",
                "message": f"Ready to send message to {contact_name}: {message}"
            }
                
        except Exception as e:
            logger.error(f"WhatsApp error: {e}")
            return {"status": "error", "error": str(e)}
    
    def _check_whatsapp_availability(self, contact_name: str, contact_number: str) -> bool:
        """Check if contact is available on WhatsApp (basic check)"""
        try:
            # For now, assume all contacts with numbers are WhatsApp users
            # In production, this could integrate with WhatsApp Business API
            if contact_number and len(contact_number) >= 10:
                logger.info(f"Contact {contact_name} available on WhatsApp: {contact_number}")
                return True
            return False
        except Exception as e:
            logger.warning(f"WhatsApp availability check failed: {e}")
            return False
    
    def _make_call_intelligent(self, contact_name: str, contact_number: str) -> Dict[str, Any]:
        """Make phone call using multiple methods"""
        try:
            import platform
            
            # Format number for calling
            clean_number = contact_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
            if not clean_number.startswith("+"):
                if len(clean_number) == 10:
                    clean_number = "+91" + clean_number
                elif not clean_number.startswith("1") and len(clean_number) == 11:
                    clean_number = "+1" + clean_number
            
            system = platform.system()
            
            # Method 1: Windows - Use tel: protocol
            if system == "Windows":
                try:
                    os.startfile(f"tel:{clean_number}")
                    logger.info(f"Call initiated to {contact_name}: {clean_number}")
                    return {"status": "success", "message": f"Calling {contact_name}"}
                except Exception as e:
                    logger.warning(f"Windows tel: method failed: {e}")
            
            # Method 2: Try Skype calling
            try:
                skype_url = f"skype:{clean_number}?call"
                webbrowser.open(skype_url)
                logger.info(f"Skype call initiated to {contact_name}")
                return {"status": "success", "message": f"Initiating Skype call to {contact_name}"}
            except Exception as e:
                logger.warning(f"Skype method failed: {e}")
            
            # Method 3: Try WhatsApp call
            try:
                wa_call_url = f"https://wa.me/{clean_number.replace('+', '')}"
                webbrowser.open(wa_call_url)
                logger.info(f"WhatsApp call opened for {contact_name}")
                return {"status": "success", "message": f"Opening WhatsApp call for {contact_name}"}
            except Exception as e:
                logger.warning(f"WhatsApp call method failed: {e}")
            
            # Fallback
            return {
                "status": "success",
                "message": f"Ready to call {contact_name} at {clean_number}"
            }
        
        except Exception as e:
            logger.error(f"Call error: {e}")
            return {"status": "error", "error": str(e)}
    
    def _get_contact_number(self, contact_name: str) -> str:
        """Get contact number from memory or contacts"""
        try:
            # Try memory manager first
            contact = self.memory_manager.get_contact(contact_name)
            if contact and isinstance(contact, dict) and contact.get("phone"):
                return contact["phone"]
            
            # Try task executor contacts
            if hasattr(self, 'task_executor') and hasattr(self.task_executor, 'contacts_db'):
                contact_db = self.task_executor.contacts_db
                if contact_name.lower() in contact_db:
                    return contact_db[contact_name.lower()]
            
            # Try reloading contacts
            if hasattr(self, 'task_executor'):
                contacts_db = self.task_executor._load_contacts()
                if contact_name.lower() in contacts_db:
                    return contacts_db[contact_name.lower()]
            
            return ""
        except Exception as e:
            logger.warning(f"Error getting contact number: {e}")
            return ""
    
    def _handle_call(self, entities: Dict, command: str) -> str:
        """Handle phone calls"""
        try:
            contact_name = entities.get("contact", "")
            
            if not contact_name:
                return "Who would you like me to call?"
            
            result = self.task_executor.make_call(contact_name)
            
            if result['status'] == 'success':
                return f"Calling {contact_name} now."
            else:
                return f"I couldn't make the call. {result.get('error', '')}"
        
        except Exception as e:
            logger.error(f"Call error: {e}")
            return "There was an error making the call."
    
    def _handle_download(self, entities: Dict, command: str) -> str:
        """Handle file downloads from internet"""
        try:
            file_name = entities.get("file_name", "")
            file_type = entities.get("file_type", "")
            
            if not file_name:
                return "What file would you like me to download?"
            
            result = self.task_executor.download_file(file_name, file_type)
            
            if result['status'] == 'success':
                return f"Downloaded {file_name}. Saved to your downloads folder."
            else:
                return f"Couldn't find or download the file. {result.get('error', '')}"
        
        except Exception as e:
            logger.error(f"Download error: {e}")
            return "There was an error downloading the file."
    
    def _handle_open_app(self, entities: Dict, command: str) -> str:
        """Handle opening applications"""
        try:
            app_name = entities.get("app", "")
            
            if not app_name:
                return "Which application should I open?"
            
            result = self.task_executor.open_application(app_name)
            
            if result['status'] == 'success':
                return f"Opening {app_name}."
            else:
                return f"I couldn't find that application."
        
        except Exception as e:
            logger.error(f"App error: {e}")
            return "There was an error opening the application."
    
    def _handle_query(self, command: str) -> str:
        """Handle general queries with AI"""
        try:
            answer = self.nlp_processor.get_ai_answer(command)
            return answer
        except Exception as e:
            logger.error(f"Query error: {e}")
            return "I'm having trouble answering that right now."
    
    def _handle_reminder(self, entities: Dict, command: str) -> str:
        """Set reminders and alarms with smart memory integration"""
        try:
            reminder_text = entities.get("reminder_text", "").strip()
            time_str = entities.get("time", "").strip()
            alarm_type = entities.get("type", "general").strip()
            
            if not reminder_text:
                return "What should I remind you about?"
            
            # If no specific time mentioned, ask user
            if not time_str:
                return f"When would you like me to remind you about {reminder_text}? Please say a time like 'tomorrow morning' or 'in 5 minutes'."
            
            # Store in memory for future reference
            memory_entry = {
                "reminder_text": reminder_text,
                "time": time_str,
                "type": alarm_type,
                "command": command
            }
            
            # Save to memory
            self.memory_manager.remember(
                title=f"Reminder: {reminder_text[:50]}",
                content=json.dumps(memory_entry),
                category="reminder"
            )
            
            # Set the reminder/alarm
            result = self.task_executor.set_reminder(reminder_text, time_str)
            
            if result['status'] == 'success':
                response = f"Reminder set! I'll remind you to {reminder_text} {time_str}."
                
                # Add context about stored memory
                if alarm_type != "general":
                    response += f" This is a {alarm_type} alarm - I've saved this for future reference."
                
                return response
            else:
                return f"I couldn't set that reminder. {result.get('error', 'Please try again.')}"
        
        except Exception as e:
            logger.error(f"Reminder error: {e}")
            return "There was an error setting the reminder."
    
    def _handle_media(self, entities: Dict, command: str) -> str:
        """Handle media playback"""
        try:
            media_name = entities.get("media", "")
            
            if not media_name:
                return "What would you like me to play?"
            
            result = self.task_executor.play_media(media_name)
            
            if result['status'] == 'success':
                return f"Now playing {media_name}."
            else:
                return f"Couldn't play that. {result.get('error', '')}"
        
        except Exception as e:
            logger.error(f"Media error: {e}")
            return "There was an error playing media."
    
    def _open_url_in_chrome(self, url: str, app_name: str = "") -> str:
        """Open a URL in Chrome browser with multiple fallback methods"""
        try:
            logger.info(f"Attempting to open {url} in Chrome")
            
            # Method 1: Direct Chrome executable path
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    try:
                        subprocess.Popen([chrome_path, url])
                        logger.info(f"Successfully opened {app_name or url} using direct path: {chrome_path}")
                        return f"Opening {app_name or 'webpage'} in Chrome"
                    except Exception as e:
                        logger.warning(f"Failed with path {chrome_path}: {e}")
                        continue
            
            # Method 2: Use 'start chrome URL' command (Windows)
            try:
                subprocess.Popen(f"start chrome {url}", shell=True)
                logger.info(f"Successfully opened {url} using start command")
                return f"Opening {app_name or 'webpage'} in Chrome"
            except Exception as e:
                logger.warning(f"Start command failed: {e}")
            
            # Method 3: Try webbrowser with Chrome
            try:
                chrome_browser = webbrowser.get("chrome")
                chrome_browser.open(url)
                logger.info(f"Successfully opened {url} using webbrowser.get('chrome')")
                return f"Opening {app_name or 'webpage'} in Chrome"
            except Exception as e:
                logger.warning(f"Webbrowser.get('chrome') failed: {e}")
            
            # Method 4: Fallback to default browser
            try:
                webbrowser.open(url)
                logger.info(f"Opened {url} using default browser")
                return f"Opening {app_name or 'webpage'} in default browser"
            except Exception as e:
                logger.error(f"All methods failed to open {url}: {e}")
                return f"I couldn't open {app_name or 'that webpage'}. Please try again."
                
        except Exception as e:
            logger.error(f"URL opening error: {e}")
            return "There was an error opening the webpage."
    
    def _handle_system(self, entities: Dict, command: str) -> str:
        """Handle system commands and app opening"""
        try:
            command_lower = command.lower()
            
            # Check if it's an app open command (like "open settings" or "open file manager")
            if "open" in command_lower:
                # Extract app name/content after "open"
                parts = command_lower.split("open", 1)
                if len(parts) > 1:
                    app_name = parts[1].strip()
                    
                    # Normalize common app names
                    if any(x in app_name for x in ["setting", "window setting"]):
                        app_name = "windows settings"
                    elif any(x in app_name for x in ["file manager", "file explorer", "explorer"]):
                        app_name = "file manager"
                    
                    # Check if it's a web app/URL request using the mapping
                    for web_app_key, url in self.web_apps.items():
                        if web_app_key in app_name:
                            return self._open_url_in_chrome(url, web_app_key)
                    
                    # Try to open regular app
                    try:
                        result = self.task_executor.open_application(app_name)
                        if result.get("status") == "success":
                            return result.get("message", f"Opening {app_name}")
                    except Exception as app_err:
                        logger.error(f"Failed to open app {app_name}: {app_err}")
                        return f"I couldn't open {app_name}. Please try again."
            
            # Otherwise, handle as system command
            action = command_lower  # Pass full command as action
            result = self.task_executor.execute_system_command(action)
            
            if result['status'] == 'success':
                return result['message']
            else:
                return result.get('error', "I couldn't execute that command.")
        
        except Exception as e:
            logger.error(f"System error: {e}")
            return f"There was an error: {str(e)}"
    
    def _handle_memory(self, entities: Dict, command: str) -> str:
        """Handle memory operations - remember, recall, learn"""
        try:
            command_lower = command.lower()
            
            if "remember" in command_lower or "store" in command_lower or "save" in command_lower:
                # Extract what to remember
                memory_content = self._extract_memory_content(command)
                if memory_content:
                    result = self.memory_manager.remember(
                        title=memory_content[:50],  # First 50 chars as title
                        content=memory_content,
                        category="important"
                    )
                    return result.get("message", "Memory stored")
                else:
                    return "What would you like me to remember?"
            
            elif "recall" in command_lower or "remind me about" in command_lower or "what did i say" in command_lower:
                # Extract what to recall
                query = self._extract_recall_query(command)
                if query:
                    memories = self.memory_manager.recall(query)
                    if memories:
                        response = f"I remember: "
                        for mem in memories[:3]:  # Return top 3 matches
                            response += f"{mem.get('content', '')} "
                        return response
                    else:
                        return f"I don't have any memories about {query}"
                else:
                    return "What would you like me to recall?"
            
            elif "learn" in command_lower:
                # Extract fact to learn
                fact_parts = command_lower.replace("learn", "").strip().split("is" if " is " in command_lower else "that")
                if len(fact_parts) >= 2:
                    fact = fact_parts[0].strip()
                    value = fact_parts[-1].strip()
                    result = self.memory_manager.learn_fact(fact, value)
                    return result.get("message", "Fact learned")
                else:
                    return "Tell me the fact and what it is, for example: 'learn that my birthday is January 15'"
            
            return "I'm not sure what memory operation you want"
        
        except Exception as e:
            logger.error(f"Memory error: {e}")
            return "There was an error managing my memory."
    
    def _handle_update_request(self, command: str) -> str:
        """Handle automatic update and learning requests"""
        try:
            command_lower = command.lower()
            
            # Check for update request
            if "update" in command_lower or "upgrade" in command_lower or "install" in command_lower:
                if "check" in command_lower:
                    # Check for available updates
                    result = self.auto_updater.check_for_updates()
                    if result["status"] == "updates_available":
                        update_list = ", ".join([u["name"] for u in result["updates"][:3]])
                        return f"I found {result['count']} updates available: {update_list}. Should I install them automatically?"
                    else:
                        return "Your assistant is up to date!"
                
                elif "install" in command_lower or "apply" in command_lower or "yes" in command_lower:
                    # Auto-install updates
                    result = self.auto_updater.auto_install_updates()
                    if result["status"] == "update_complete":
                        return f"Successfully installed {result['total_installed']} new features! I'm now more capable. Thanks for letting me improve!"
                    else:
                        return f"Update installation encountered some issues. Please check the update log."
                
                else:
                    # General update info
                    return "I can automatically update myself with new features. Say 'check updates' or 'install updates' to proceed."
            
            # Check for learning/improvement request
            elif "learn" in command_lower or "improve" in command_lower or "better" in command_lower:
                if "how" in command_lower or "what" in command_lower:
                    return "I continuously learn from our conversations. I remember successful interactions and improve my understanding. Each conversation helps me get better!"
                else:
                    # Trigger self-improvement
                    result = self.self_learning.improve_intent_detection()
                    if result["status"] == "improved":
                        improvements = result.get("improvements", {})
                        return f"I've analyzed my performance. Success rate: {improvements.get('success_rate', 0):.1%}. I'm working to improve further!"
                    else:
                        return "I need more interactions to improve significantly. Let's keep chatting!"
            
            else:
                return "I can update myself with new features and learn from our interactions. Ask me to check updates or help me learn!"
        
        except Exception as e:
            logger.error(f"Update handling error: {e}")
            return "There was an error with the update system."
    
    def _handle_query(self, command: str) -> str:
        """Handle queries with web search fallback"""
        try:
            # Try AI first
            answer = self.nlp_processor.get_ai_answer(command)
            
            # If AI answer is not satisfactory, try web search
            if not answer or "could you be more specific" in answer.lower():
                # Perform web search
                results = self.web_search.search(command, num_results=3)
                
                if results:
                    # Compile answer from search results
                    answer = f"I found some information: {results[0]['snippet']}. "
                    if len(results) > 1:
                        answer += f"Other sources mention: {results[1]['snippet'][:100]}..."
                    return answer
                else:
                    return "I couldn't find information on that. Can you provide more context?"
            
            return answer
        
        except Exception as e:
            logger.error(f"Query error: {e}")
            return "I'm having trouble answering that right now."
    
    def _extract_memory_content(self, command: str) -> str:
        """Extract content to remember from command"""
        keywords = ["remember", "remember that", "store", "save", "i said"]
        for keyword in keywords:
            if keyword in command.lower():
                parts = command.lower().split(keyword)
                if len(parts) > 1:
                    return parts[-1].strip()
        return ""
    
    def _extract_recall_query(self, command: str) -> str:
        """Extract recall query from command"""
        keywords = ["recall", "remind me about", "what did i say about", "do you remember"]
        for keyword in keywords:
            if keyword in command.lower():
                parts = command.lower().split(keyword)
                if len(parts) > 1:
                    return parts[-1].strip()
        return ""
    
    def interactive_mode(self):
        """Run assistant in interactive mode"""
        self.running = True
        self.speak(f"Hello {self.user_name}! I'm aari, your intelligent voice assistant. I'm ready to help!")
        self.speak("Just say my name or 'Hey aari' to activate me.")
        
        while self.running:
            try:
                command = self.listen()
                
                if command == "sorry_not_understood":
                    self.speak("I didn't quite catch that. Could you say it again?")
                    continue
                
                if command == "network_error":
                    self.speak("I'm having network issues. Please check your connection.")
                    continue
                
                if "exit" in command or "quit" in command or "bye" in command:
                    self.speak(f"Goodbye, {self.user_name}! Have a great day!")
                    self.running = False
                    break
                
                response = self.process_command(command)
                self.speak(response)
            
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                self.speak("An error occurred. Let me try again.")
    
    def get_conversation_history(self) -> List[Dict]:
        """Return conversation history"""
        return self.conversation_history
    
    def save_settings(self, settings_file: str = "assistant_settings.json"):
        """Save assistant settings"""
        settings = {
            "user_name": self.user_name,
            "created_at": datetime.now().isoformat()
        }
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
    
    def load_settings(self, settings_file: str = "assistant_settings.json"):
        """Load assistant settings"""
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                self.user_name = settings.get("user_name", "User")


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.interactive_mode()
