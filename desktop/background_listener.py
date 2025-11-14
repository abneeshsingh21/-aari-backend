"""
Background Listener - Runs in background and listens for wake words
Allows AARI to be always-on in the background
"""

import threading
import logging
import speech_recognition as sr
from typing import Callable, List
import time

logger = logging.getLogger(__name__)

class BackgroundListener:
    """Listens for wake words in the background"""
    
    def __init__(self, wake_words: List[str], on_wake_callback: Callable):
        """
        Initialize background listener
        
        Args:
            wake_words: List of wake word phrases (e.g., ["hey aari", "suno", "hello aari"])
            on_wake_callback: Function to call when wake word detected
        """
        self.wake_words = [word.lower() for word in wake_words]
        self.on_wake_callback = on_wake_callback
        self.running = False
        self.listening = False
        self.recognizer = sr.Recognizer()
        self.background_thread = None
    
    def start(self):
        """Start background listening"""
        if self.running:
            logger.warning("Background listener already running")
            return
        
        self.running = True
        self.background_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.background_thread.start()
        logger.info("Background listener started")
    
    def stop(self):
        """Stop background listening"""
        self.running = False
        logger.info("Background listener stopped")
    
    def _listen_loop(self):
        """Main listening loop running in background"""
        while self.running:
            try:
                # Use microphone for continuous listening
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # Listen with short timeout for responsiveness
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)
                
                # Try to recognize speech
                try:
                    text = self.recognizer.recognize_google(audio, language="en-IN")
                    text_lower = text.lower()
                    
                    # Check if wake word detected
                    for wake_word in self.wake_words:
                        if wake_word in text_lower:
                            logger.info(f"Wake word detected: {wake_word}")
                            # Call the callback function
                            if self.on_wake_callback:
                                self.on_wake_callback(text)
                            # Reset after wake
                            break
                
                except sr.UnknownValueError:
                    # Not understood, continue listening
                    pass
                except sr.RequestError as e:
                    logger.warning(f"Network error in background listener: {e}")
                    time.sleep(1)  # Wait before retrying
            
            except sr.RequestError as e:
                logger.warning(f"Microphone error: {e}")
                time.sleep(2)
            except Exception as e:
                logger.error(f"Background listener error: {e}")
                time.sleep(2)
    
    def is_listening(self) -> bool:
        """Check if currently listening"""
        return self.running
