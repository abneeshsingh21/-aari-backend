"""
Desktop Voice Assistant Integration
Works on Windows, macOS, and Linux
Natural Female Voice with Multi-Language Support
WITH Auto-Update, Web Search, and Self-Learning
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import json
import logging
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
import platform
import subprocess
import webbrowser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration - supports both local and remote backend
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('BACKEND_URL', 'https://aari-backend-3rs9.onrender.com')

# Allow override for local testing
if os.getenv('LOCAL_BACKEND'):
    API_URL = "http://localhost:5000"

class DesktopVoiceAssistant:
    """Desktop GUI for voice assistant with natural female voice"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AARI - Natural Voice Assistant")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Initialize voice components
        self.recognizer = sr.Recognizer()
        self.listening = False
        self.running = True
        self.language = "en"  # Default English
        self.continuous_mode = False  # Continuous listening mode
        self.processing = False  # Flag to prevent duplicate processing
        self.stop_listening_flag = False  # Flag to stop listening immediately
        
        self.backend_running = False
        self.setup_ui()
        self.root.bind('<Control-Shift-v>', self.toggle_continuous_listening)
        
        # Check backend on startup (after UI is set up)
        self.root.after(500, self.check_backend_status)
    
    def check_backend_status(self):
        """Check if backend is running"""
        try:
            response = requests.get(f"{API_URL}/api/health", timeout=2)
            if response.status_code == 200:
                self.backend_running = True
                self.status_var.set("Ready")
                self.status_label.config(foreground="green")
                self.log_message("✅ Backend connected!", "system")
            else:
                self.backend_running = False
                self.status_var.set("Backend not running")
                self.status_label.config(foreground="red")
                self.log_message("❌ Backend offline. Please start backend first!", "error")
        except Exception as e:
            self.backend_running = False
            self.status_var.set("Backend not running")
            self.status_label.config(foreground="red")
            self.log_message("❌ Cannot connect to backend", "error")
    
    def setup_ui(self):
        """Setup user interface"""
        
        # Title
        title_label = ttk.Label(self.root, text="🎙️ AARI - Natural Voice Assistant",
                               font=("Arial", 20, "bold"))
        title_label.pack(pady=15)
        
        # Language selection
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="en")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                  values=["en (English)", "hi (Hindi)", "ta (Tamil)"],
                                  state="readonly", width=20)
        lang_combo.pack(side=tk.LEFT, padx=10)
        
        # Status frame
        status_frame = ttk.Frame(self.root)
        status_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                      foreground="green", font=("Arial", 12, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)
        
        self.voice_button = ttk.Button(button_frame, text="🎤 Start Speaking",
                                       command=self.start_listening)
        self.voice_button.pack(side=tk.LEFT, padx=5)
        
        self.continuous_btn = ttk.Button(button_frame, text="🔄 Continuous Mode (OFF)",
                                         command=self.toggle_continuous_listening)
        self.continuous_btn.pack(side=tk.LEFT, padx=5)
        
        self.text_button = ttk.Button(button_frame, text="⌨️ Type",
                                      command=self.text_input)
        self.text_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🛑 Stop", command=self.stop_listening).pack(side=tk.LEFT, padx=5)
        
        # Advanced features frame
        advanced_frame = ttk.Frame(self.root)
        advanced_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Button(advanced_frame, text="🔄 Check Updates", 
                  command=self.check_updates).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(advanced_frame, text="⚡ Install Updates", 
                  command=self.install_updates).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(advanced_frame, text="🔍 Web Search", 
                  command=self.open_web_search).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(advanced_frame, text="📊 Learning Status", 
                  command=self.show_learning_status).pack(side=tk.LEFT, padx=5)
        
        # Info label
        info_label = ttk.Label(self.root, text="💬 Conversation (Voice Enabled):",
                              font=("Arial", 10))
        info_label.pack(pady=(10, 5), padx=20, anchor=tk.W)
        
        # Output text area
        self.output_text = tk.Text(self.root, height=14, width=85, wrap=tk.WORD)
        self.output_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.output_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)
    
    def toggle_continuous_listening(self, event=None):
        """Toggle continuous listening mode"""
        self.continuous_mode = not self.continuous_mode
        if self.continuous_mode:
            self.continuous_btn.config(text="🔄 Continuous Mode (ON)")
            self.log_message("🎤 Continuous mode ON - I'm always listening!", "system")
            self.start_continuous_listening()
        else:
            self.continuous_btn.config(text="🔄 Continuous Mode (OFF)")
            self.log_message("🎤 Continuous mode OFF", "system")
            self.stop_listening()
    
    def start_continuous_listening(self):
        """Start continuous listening loop"""
        if self.continuous_mode and not self.listening:
            self.listening = True
            thread = threading.Thread(target=self._continuous_listen_loop, daemon=True)
            thread.start()
    
    def _continuous_listen_loop(self):
        """Continuous listening loop - keeps listening after each command"""
        self.stop_listening_flag = False
        while self.continuous_mode and self.running and not self.stop_listening_flag:
            if self.processing:
                continue  # Wait if processing
            try:
                self._listen_and_process()
                # Don't immediately loop - wait for user to speak naturally
            except Exception as e:
                logger.error(f"Continuous listen error: {e}")
        self.listening = False
        self.stop_listening_flag = False
    
    def on_hotkey(self, event):
        """Handle hotkey press - toggle continuous mode"""
        self.toggle_continuous_listening()
    
    def text_input(self):
        """Get command via text input"""
        if not self.listening:
            self.listening = True
            self.status_var.set("Typing..."  )
            self.voice_button.config(state=tk.DISABLED)
            thread = threading.Thread(target=self._text_input_process, daemon=True)
            thread.start()
    
    def _text_input_process(self):
        """Text input dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Type your command")
        dialog.geometry("400x150")
        dialog.attributes('-topmost', True)
        
        ttk.Label(dialog, text="What do you want to tell AARI?:", 
                 font=("Arial", 11)).pack(pady=10)
        
        entry = ttk.Entry(dialog, width=50, font=("Arial", 11))
        entry.pack(pady=10, padx=20)
        entry.focus()
        
        result = [None]
        
        def on_submit():
            result[0] = entry.get().lower()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        ttk.Button(dialog, text="Send", command=on_submit).pack(side=tk.LEFT, padx=5, pady=10)
        ttk.Button(dialog, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5, pady=10)
        
        dialog.bind('<Return>', lambda e: on_submit())
        
        self.root.wait_window(dialog)
        
        if result[0]:
            self._process_command(result[0])
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start voice recognition in background thread"""
        if not self.listening:
            self.listening = True
            self.status_var.set("Listening...")
            self.status_label.config(foreground="orange")
            self.voice_button.config(state=tk.DISABLED)
            
            thread = threading.Thread(target=self._listen_and_process, daemon=True)
            thread.start()
    
    def _listen_and_process(self):
        """Listen for voice and process command"""
        if self.processing:
            return  # Prevent duplicate processing
        
        self.processing = True
        try:
            self.log_message("🎤 AARI is listening... Speak now!", "system")
            
            command = None
            lang_code = self.lang_var.get().split()[0].strip("(")
            
            # Try using sounddevice first (more reliable)
            try:
                command = self._record_audio_with_sounddevice(lang_code)
            except Exception as e:
                logger.warning(f"Sounddevice failed: {e}, trying PyAudio...")
                # Fallback to PyAudio
                try:
                    command = self._record_audio_with_pyaudio(lang_code)
                except Exception as e2:
                    logger.error(f"PyAudio also failed: {e2}")
                    self.log_message("❌ Microphone not available. Click '⌨️ Type' to type instead.", "error")
                    self.processing = False
                    return
            
            if command:
                self._process_command(command)
            else:
                self.log_message("❌ Sorry, I didn't catch that. Try again!", "assistant")
        
        except Exception as e:
            logger.error(f"Listen error: {e}")
            self.log_message(f"❌ Error: {str(e)}", "error")
        
        finally:
            self.processing = False
            if not self.continuous_mode:
                self.stop_listening()
    
    def _record_audio_with_sounddevice(self, lang_code):
        """Record audio using sounddevice with fast speech detection"""
        logger.info("Recording with sounddevice...")
        sr_rate = 44100  # Sample rate
        duration = 6  # Reduced to 6 seconds for MUCH faster response
        audio_file = None
        
        try:
            # Record audio
            self.log_message("🔴 Recording... Speak now!", "system")
            audio_data = sd.rec(int(sr_rate * duration), samplerate=sr_rate, channels=1, dtype='float32')
            sd.wait()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                audio_file = fp.name
            
            # Write the file (now file handle is closed)
            sf.write(audio_file, audio_data, sr_rate)
            
            # Recognize speech
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                
                # Support multiple languages
                try:
                    if lang_code == "hi":
                        text = recognizer.recognize_google(audio, language="hi-IN")
                    elif lang_code == "ta":
                        text = recognizer.recognize_google(audio, language="ta-IN")
                    else:
                        text = recognizer.recognize_google(audio, language="en-IN")
                    return text.lower()
                except sr.UnknownValueError:
                    logger.warning("Could not understand audio")
                    return None
        
        except Exception as e:
            logger.error(f"Sounddevice recording error: {e}")
            raise
        finally:
            # Clean up temp file
            if audio_file and os.path.exists(audio_file):
                try:
                    os.unlink(audio_file)
                except:
                    pass
    
    def _record_audio_with_pyaudio(self, lang_code):
        """Record audio using PyAudio (fallback) with fast detection"""
        logger.info("Recording with PyAudio...")
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.log_message("🔴 Recording... Speak now!", "system")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Faster noise detection
                # Reduced timeout from 15 to 8 seconds for faster response
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)
                
                # Support multiple languages
                try:
                    if lang_code == "hi":
                        text = recognizer.recognize_google(audio, language="hi-IN")
                    elif lang_code == "ta":
                        text = recognizer.recognize_google(audio, language="ta-IN")
                    else:
                        text = recognizer.recognize_google(audio, language="en-IN")
                    return text.lower()
                except sr.UnknownValueError:
                    logger.warning("Could not understand audio")
                    return None
        
        except Exception as e:
            logger.error(f"PyAudio recording error: {e}")
            raise
    
    def _process_command(self, command):
        """Send command to backend and get response with voice"""
        self.log_message(f"👤 You: {command}", "user")
        
        # Check if backend is running
        if not self.backend_running:
            try:
                response = requests.get(f"{API_URL}/api/health", timeout=2)
                if response.status_code == 200:
                    self.backend_running = True
                else:
                    self.log_message("❌ Backend not running. Start it first!", "error")
                    return
            except:
                self.log_message("❌ Backend not running. Start it first!", "error")
                return
        
        try:
            response = requests.post(
                f"{API_URL}/api/process-command",
                json={"command": command},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                assistant_response = data.get("response", "No response")
                intent = data.get("intent", "")
                contact = data.get("contact", "")
                contact_number = data.get("contact_number", "")
                message = data.get("message", "")
                
                self.log_message(f"🎙️ AARI: {assistant_response}", "assistant")
                
                # Handle special intents for WhatsApp and calling
                if intent == "send_message" and contact and contact_number:
                    self._handle_whatsapp_desktop(contact, message, contact_number)
                elif intent == "make_call" and contact and contact_number:
                    self._handle_call_desktop(contact, contact_number)
                
                # Play voice response
                self._speak_response(assistant_response)
            else:
                self.log_message("❌ API Error", "error")
        
        except requests.exceptions.ConnectionError:
            self.backend_running = False
            self.log_message("❌ Backend not running. Start it first!", "error")
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}", "error")
    
    def _handle_whatsapp_desktop(self, contact: str, message: str, contact_number: str):
        """Handle WhatsApp messaging on desktop"""
        try:
            # Format contact number
            clean_number = contact_number.replace("-", "").replace(" ", "")
            if not clean_number.startswith("+"):
                if len(clean_number) == 10:
                    clean_number = "+91" + clean_number
                elif not clean_number.startswith("1"):
                    clean_number = "+1" + clean_number
            
            # Open WhatsApp Web
            wa_url = f"https://wa.me/{clean_number.replace('+', '')}?text={message.replace(' ', '%20')}"
            webbrowser.open(wa_url)
            
            self.log_message(f"✅ Opening WhatsApp for {contact}... Sending: '{message}'", "system")
        except Exception as e:
            self.log_message(f"❌ WhatsApp Error: {str(e)}", "error")
    
    def _handle_call_desktop(self, contact: str, contact_number: str):
        """Handle phone calling on desktop"""
        try:
            # Format contact number
            clean_number = contact_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
            if not clean_number.startswith("+"):
                if len(clean_number) == 10:
                    clean_number = "+91" + clean_number
                elif not clean_number.startswith("1") and len(clean_number) == 11:
                    clean_number = "+1" + clean_number
            
            system = platform.system()
            
            # Method 1: Try Windows tel: protocol
            if system == "Windows":
                try:
                    os.startfile(f"tel:{clean_number}")
                    self.log_message(f"📞 Calling {contact}...", "system")
                    return
                except Exception as e:
                    logger.warning(f"Tel protocol failed: {e}")
            
            # Method 2: Try Skype
            try:
                skype_url = f"skype:{clean_number}?call"
                webbrowser.open(skype_url)
                self.log_message(f"📞 Opening Skype call to {contact}...", "system")
                return
            except Exception as e:
                logger.warning(f"Skype failed: {e}")
            
            # Method 3: WhatsApp call
            try:
                wa_url = f"https://wa.me/{clean_number.replace('+', '')}"
                webbrowser.open(wa_url)
                self.log_message(f"📱 Opening WhatsApp for call with {contact}...", "system")
            except Exception as e:
                logger.warning(f"WhatsApp call failed: {e}")
        
        except Exception as e:
            self.log_message(f"❌ Call Error: {str(e)}", "error")
    
    def _speak_response(self, text):
        """Speak response using natural Google TTS voice"""
        try:
            lang_code = self.lang_var.get().split()[0].strip("(")
            
            # Use gTTS for natural voice
            tts = gTTS(
                text=text, 
                lang=lang_code, 
                slow=False,
                tld='com'
            )
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.close()
            audio_file = temp_file.name
            
            # Save TTS to file
            tts.save(audio_file)
            
            try:
                # Load audio and boost volume
                sound = AudioSegment.from_mp3(audio_file)
                
                # Volume boost for clarity
                sound = sound + 6  # Moderate boost
                
                # Normalize
                sound = sound.normalize()
                
                # Export to WAV for Windows compatibility
                wav_file = audio_file.replace(".mp3", ".wav")
                sound.export(wav_file, format="wav", bitrate="192k")
                
                # Play audio
                self._play_audio(wav_file)
                
                # Clean up
                if os.path.exists(wav_file):
                    try:
                        os.unlink(wav_file)
                    except:
                        pass
            finally:
                # Clean up MP3
                if os.path.exists(audio_file):
                    try:
                        os.unlink(audio_file)
                    except:
                        pass
                
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            self.log_message(f"💬 [Voice disabled] AARI: {text}", "assistant")
    
    def _play_audio(self, audio_file):
        """Play audio file using platform-specific method - RELIABLE playback"""
        try:
            system = platform.system()
            
            if system == "Windows":
                # Windows: Use winsound (fast and reliable)
                try:
                    import winsound
                    # Ensure file exists before playing
                    if os.path.exists(audio_file):
                        # Play synchronously and wait for completion
                        winsound.PlaySound(audio_file, winsound.SND_FILENAME)
                except Exception as e:
                    logger.warning(f"Winsound failed: {e}, trying PowerShell...")
                    # Fallback: use PowerShell for better audio quality and reliability
                    try:
                        ps_cmd = f"""
                        $player = New-Object System.Media.SoundPlayer
                        $player.SoundLocation = '{audio_file}'
                        $player.PlaySync()
                        """
                        subprocess.run(
                            ["powershell", "-NoProfile", "-Command", ps_cmd],
                            check=False, 
                            capture_output=True,
                            timeout=30
                        )
                    except Exception as ps_e:
                        logger.error(f"PowerShell audio playback also failed: {ps_e}")
                        
            elif system == "Darwin":
                # macOS: Use afplay with better settings
                subprocess.run(
                    ["afplay", "-q", "1", audio_file],
                    check=False,
                    timeout=30
                )
            else:
                # Linux: Use paplay for better audio
                try:
                    subprocess.run(
                        ["paplay", "--device=default", audio_file],
                        check=False,
                        timeout=30
                    )
                except:
                    # Fallback to aplay
                    subprocess.run(
                        ["aplay", "-q", audio_file],
                        check=False,
                        timeout=30
                    )
        except Exception as e:
            logger.error(f"Audio playback error: {e}")
    
    def stop_listening(self):
        """Stop voice recognition"""
        self.listening = False
        self.stop_listening_flag = True  # Stop continuous listening immediately
        self.status_var.set("Ready")
        self.status_label.config(foreground="green")
        self.voice_button.config(state=tk.NORMAL)
    
    def log_message(self, message: str, sender: str = ""):
        """Log message to output text area"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def check_updates(self):
        """Check for available updates"""
        try:
            response = requests.get(f"{API_URL}/api/check-updates", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "updates_available":
                    updates = data.get("updates", [])
                    update_list = "\n".join([f"• {u['name']} v{u.get('version', '?')}: {u.get('description', '')}" 
                                           for u in updates[:5]])
                    self.log_message(f"✅ Found {len(updates)} updates:\n{update_list}\n")
                    messagebox.showinfo("Updates Available", 
                                      f"Found {len(updates)} updates. Click 'Install Updates' to proceed.")
                else:
                    self.log_message("✅ Your assistant is up to date!\n")
                    messagebox.showinfo("No Updates", "Your assistant is already up to date.")
            else:
                self.log_message("❌ Failed to check updates\n")
        except Exception as e:
            self.log_message(f"❌ Error checking updates: {str(e)}\n")
            logger.error(f"Update check error: {e}")
    
    def install_updates(self):
        """Install available updates"""
        if messagebox.askyesno("Install Updates", 
                              "This will install new features. Continue?"):
            self.log_message("⏳ Installing updates... Please wait...\n")
            try:
                response = requests.post(f"{API_URL}/api/install-updates", 
                                       json={}, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "update_complete":
                        installed = data.get("installed", [])
                        self.log_message(f"✅ Successfully installed {len(installed)} features!")
                        self.log_message(f"Installed: {', '.join(installed)}\n")
                        messagebox.showinfo("Updates Installed", 
                                          f"Successfully installed {len(installed)} new features!")
                    else:
                        self.log_message(f"⚠️ Update status: {data.get('status')}\n")
                else:
                    self.log_message("❌ Failed to install updates\n")
            except Exception as e:
                self.log_message(f"❌ Installation error: {str(e)}\n")
                logger.error(f"Installation error: {e}")
    
    def show_learning_status(self):
        """Show self-learning status"""
        try:
            response = requests.get(f"{API_URL}/api/learning-status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                total = data.get("total_interactions", 0)
                successful = data.get("successful_interactions", 0)
                success_rate = data.get("success_rate", 0)
                
                status_msg = f"""
📊 LEARNING STATUS
━━━━━━━━━━━━━━━━━━━━━
Total Interactions: {total}
Successful: {successful}
Success Rate: {success_rate:.1%}
Learning: {'✅ Active' if data.get('learning_enabled') else '❌ Inactive'}
━━━━━━━━━━━━━━━━━━━━━
I'm getting smarter with each conversation! 🧠
"""
                self.log_message(status_msg + "\n")
                messagebox.showinfo("Learning Status", status_msg)
            else:
                self.log_message("❌ Failed to get learning status\n")
        except Exception as e:
            self.log_message(f"❌ Error getting learning status: {str(e)}\n")
            logger.error(f"Learning status error: {e}")
    
    def open_web_search(self):
        """Open web search dialog"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Web Search")
        search_window.geometry("500x400")
        
        ttk.Label(search_window, text="Search Query:").pack(pady=10, padx=10)
        
        search_entry = ttk.Entry(search_window, width=50)
        search_entry.pack(pady=5, padx=10)
        
        result_text = tk.Text(search_window, height=15, width=60, wrap=tk.WORD)
        result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=result_text.yview)
        
        def perform_search():
            query = search_entry.get()
            if query:
                result_text.delete('1.0', tk.END)
                result_text.insert(tk.END, "🔍 Searching...\n")
                search_window.update()
                
                try:
                    response = requests.post(f"{API_URL}/api/web-search",
                                           json={"query": query, "num_results": 5},
                                           timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        results = data.get("results", [])
                        
                        result_text.delete('1.0', tk.END)
                        result_text.insert(tk.END, f"Results for '{query}':\n\n")
                        
                        for i, result in enumerate(results, 1):
                            result_text.insert(tk.END, 
                                             f"{i}. {result.get('title', 'Untitled')}\n")
                            result_text.insert(tk.END,
                                             f"   {result.get('snippet', '')[:200]}...\n")
                            result_text.insert(tk.END,
                                             f"   Source: {result.get('url', '')}\n\n")
                    else:
                        result_text.delete('1.0', tk.END)
                        result_text.insert(tk.END, "❌ Search failed\n")
                except Exception as e:
                    result_text.delete('1.0', tk.END)
                    result_text.insert(tk.END, f"❌ Error: {str(e)}\n")
        
        ttk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
    
    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    app = DesktopVoiceAssistant(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
