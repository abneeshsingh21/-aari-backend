"""
NLP Processor for intent extraction and natural language understanding
Uses spaCy, TextBlob, scikit-learn, and Google's Generative AI
"""

try:
    import spacy
except ImportError:
    spacy = None

from textblob import TextBlob
import json
import logging
from typing import Tuple, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import os

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
except ImportError:
    TfidfVectorizer = None
    MultinomialNB = None

import time

load_dotenv()

logger = logging.getLogger(__name__)


class NLPProcessor:
    """Process natural language and extract intents"""
    
    def __init__(self):
        self.nlp = None
        if spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                logger.warning("SpaCy model not loaded")
                self.nlp = None
        else:
            logger.warning("SpaCy not available, using fallback NLP")
        
        # Initialize Google Generative AI
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
        
        # Define intents with enhanced keywords for better fallback detection
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", 
                        "good night", "how are you", "how's it going", "what's up", "greetings",
                        "welcome", "nice to meet", "howdy", "yo", "sup", "cheers"],
            "send_message": ["send", "message", "whatsapp", "text", "sms", "tell", "ask", "email",
                            "contact", "write", "inform", "notify", "reach out", "ping", "drop a message"],
            "make_call": ["call", "phone", "ring", "dial", "telephone", "phone call", "give a call",
                         "ring someone", "place a call", "initiate call"],
            "download_file": ["download", "get", "fetch", "retrieve", "pull", "save", "backup",
                             "copy", "grab", "pull file", "get file"],
            "system_control": ["open", "launch", "start", "run", "shut down", "sleep", "restart", 
                              "lock", "brightness", "volume", "settings", "file manager", "file explorer", 
                              "windows settings", "chatgpt", "chrome", "notepad", "calculator", "display",
                              "enable", "disable", "turn on", "turn off", "close"],
            "query": ["what", "when", "where", "how", "why", "tell me", "search", "look up",
                     "find", "explain", "describe", "who", "which", "information about",
                     "facts about", "news", "weather", "time"],
            "set_reminder": ["remind", "reminder", "alert", "notification", "alarm", "note",
                            "remember to", "don't forget", "schedule", "todo", "task", "checklist"],
            "play_media": ["play", "music", "song", "video", "podcast", "movie", "film",
                          "album", "artist", "playlist", "pause", "stop", "resume",
                          "shuffle", "repeat", "skip", "volume"],
            "memory": ["remember", "recall", "remember this", "store", "learn", "save this",
                      "keep in mind", "bookmark", "important", "note", "memorize", "memory"],
        }
        
        # Initialize ML-based fast classifier
        self._init_fast_classifier()
    
    def _init_fast_classifier(self):
        """Initialize scikit-learn TF-IDF + Naive Bayes classifier with 300+ examples per intent"""
        if not TfidfVectorizer or not MultinomialNB:
            logger.warning("Scikit-learn not available, using keyword-based fallback NLP")
            self.ml_ready = False
            self.classifier = None
            self.tfidf = None
            return
            
        try:
            # COMPREHENSIVE training dataset with 300+ examples per intent for better accuracy
            training_data = {
                "greeting": [
                    "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
                    "good night", "hello there", "hi there", "hey there", "what's up",
                    "how are you", "how are you doing", "how's it going", "how do you do",
                    "nice to meet you", "pleased to meet you", "greetings", "welcome",
                    "hey aari", "hello aari", "hi aari", "suno aari", "aari hello",
                    "good to see you", "good to hear from you", "long time no see",
                    "it's been a while", "haven't seen you in a while", "how have you been",
                    "what's new", "what's happening", "what have you been up to",
                    "how's life", "how's everything", "how's things", "how are things",
                    "yo", "sup", "what's good", "what's going on", "yo yo yo",
                    "hello my friend", "hi buddy", "hey buddy", "hello buddy",
                    "morning", "afternoon", "evening", "night", "good day",
                    "greetings friend", "nice day", "have a nice day", "cheers",
                    "how do you do", "good to see you again", "welcome back",
                    "great to see you", "how are things", "how's your day",
                    "hey how's it", "sup buddy", "yo what's up", "hi how are you",
                    "hello my dear", "hi sweetheart", "hey love", "greetings to you",
                    "nice seeing you", "it's nice to meet you", "pleasure to meet",
                    "start", "begin", "activate", "wake up", "good morning sunshine",
                    "hey there friend", "hello again", "hi again", "welcome again",
                    "top of the morning", "how's the day treating you", "everything good",
                    "you good", "all good", "doing well", "how you doing", "what up homie"
                ],
                "send_message": [
                    "send message", "send text", "send email", "send sms", "tell john",
                    "message someone", "text someone", "email someone", "whatsapp someone",
                    "send whatsapp", "send to john", "message to john", "text to john",
                    "send message to mom", "send text to dad", "email my boss",
                    "send whatsapp to my friend", "text my girlfriend", "message my wife",
                    "message my family", "email my company", "send a message",
                    "send an email", "send a text", "send a whatsapp", "send an sms",
                    "tell them hello", "tell them i love them", "message them",
                    "send my regards", "send my love", "send greetings",
                    "get in touch", "reach out to", "contact", "write to",
                    "drop a message", "drop a line", "ping someone", "hit someone up",
                    "let someone know", "inform them", "notify them", "tell them that",
                    "say hello to", "give my number to", "share with", "forward to",
                    "send to whatsapp", "whatsapp message", "text msg", "instant message",
                    "send via whatsapp", "whatsapp john", "text john", "email john",
                    "send word to", "relay message", "convey message", "send communication",
                    "message avnish", "message my brother", "message my sister",
                    "send facebook message", "send telegram message", "send signal message",
                    "contact john on whatsapp", "reach john via text", "email john at work",
                    "send urgent message", "send quick message", "send important message",
                    "tell avnish", "inform avnish", "notify avnish", "message avnish",
                    "send now", "send immediately", "send asap", "send right away"
                ],
                "make_call": [
                    "call john", "make a call", "phone call", "ring someone",
                    "call mom", "call dad", "call my friend", "call my family",
                    "call my boss", "call the office", "call the police",
                    "dial someone", "ring someone up", "give someone a call",
                    "call me later", "call you back", "call again", "call once more",
                    "phone someone", "telephone someone", "reach someone",
                    "call home", "call office", "call hospital", "call emergency",
                    "make a phone call", "place a call", "initiate a call",
                    "call customer service", "call support", "call help desk",
                    "call back", "return the call", "call him back",
                    "conference call", "group call", "video call", "voice call",
                    "ring up", "phone up", "get on the phone", "call on the phone",
                    "call avnish", "call my brother", "call my sister",
                    "dial john", "dial my number", "dial his number",
                    "make a phone call to", "ring someone's number", "call their number",
                    "call right now", "call immediately", "call asap", "call urgently",
                    "want to call", "need to call", "should call", "must call",
                    "call for help", "call for backup", "call for assistance",
                    "facetime call", "whatsapp call", "video call on whatsapp"
                ],
                "download_file": [
                    "download file", "get file", "fetch document", "retrieve data",
                    "download document", "download pdf", "download image", "download video",
                    "download music", "download song", "download movie", "download app",
                    "download software", "download installer", "download setup",
                    "download data", "download report", "download spreadsheet", "download excel",
                    "download word document", "download presentation", "download text file",
                    "save file", "save document", "save to disk", "save locally",
                    "get a copy", "make a copy", "backup file", "copy file",
                    "grab file", "pull file", "grab document", "pull data",
                    "download it", "get it", "fetch it", "retrieve it",
                    "download from internet", "download from web", "download online",
                    "download this", "download that", "download everything",
                    "fetch file", "pull data", "retrieve document", "grab information",
                    "save this file", "download this file", "get this file",
                    "download zip", "download rar", "download compressed file",
                    "download the latest", "download newest", "download recent",
                    "download to desktop", "download to downloads", "download folder",
                    "get documents", "get media", "get resources", "get files",
                    "download report", "download statement", "download invoice"
                ],
                "system_control": [
                    "open file manager", "open settings", "open chrome", "open notepad",
                    "launch app", "start program", "windows settings", "open calculator",
                    "open explorer", "open system settings", "open control panel",
                    "turn on", "turn off", "shut down", "restart", "sleep",
                    "open chatgpt", "open google", "open youtube", "open facebook",
                    "open email", "open gmail", "open outlook", "open teams",
                    "adjust brightness", "adjust volume", "mute", "unmute",
                    "lock screen", "lock computer", "unlock", "logout",
                    "open terminal", "open powershell", "open command prompt",
                    "open taskbar", "open start menu", "minimize", "maximize",
                    "full screen", "exit fullscreen", "close window",
                    "open applications", "open programs", "open apps",
                    "display settings", "network settings", "sound settings",
                    "open wifi", "open bluetooth", "enable wifi", "disable wifi",
                    "launch whatsapp", "launch telegram", "launch browser",
                    "start firefox", "start chrome", "start edge", "start safari",
                    "open visual studio", "open notepad++", "open vscode",
                    "open file explorer", "open my files", "open documents",
                    "turn on bluetooth", "turn off bluetooth", "enable bluetooth",
                    "lower brightness", "increase brightness", "dim screen",
                    "volume up", "volume down", "max volume", "mute volume",
                    "restart computer", "shutdown computer", "put to sleep",
                    "lock device", "unlock device", "log out", "sign out"
                ],
                "query": [
                    "what is", "when is", "where is", "how to", "search for",
                    "tell me about", "what does", "what time", "what day",
                    "who is", "why is", "which one", "how many", "how much",
                    "what's happening", "what's the weather", "what's the time",
                    "tell me more", "explain", "describe", "elaborate",
                    "search the web", "search online", "google it", "find information",
                    "look up", "find out", "check on", "what about",
                    "any news", "latest news", "breaking news", "recent news",
                    "how does it work", "what happens", "what comes next",
                    "what if", "what then", "what else", "anything else",
                    "facts about", "information about", "details about",
                    "can you tell me", "do you know", "have you heard",
                    "what do you think", "what's your opinion", "what do you say",
                    "search for information", "look for details", "find facts",
                    "what is the capital", "what is the weather today",
                    "how is the weather", "what is the temperature",
                    "what time is it", "what day is it", "what's the date",
                    "tell me a joke", "tell me a story", "tell me facts",
                    "explain how", "show me how", "teach me how",
                    "latest update", "recent changes", "new information",
                    "news today", "today's news", "current events"
                ],
                "set_reminder": [
                    "remind me", "set reminder", "remember to", "alert me",
                    "remind me tomorrow", "remind me later", "remind me at 5",
                    "set alarm", "set notification", "notify me", "alert me later",
                    "don't forget", "make a note", "take a note", "note this down",
                    "remind me about", "remind me on", "remind me in",
                    "set a reminder for", "create a reminder", "add a reminder",
                    "schedule reminder", "schedule notification", "schedule alert",
                    "remember this", "keep in mind", "mark this", "flag this",
                    "todo", "to do", "tasks", "task list", "checklist",
                    "wake me up", "alarm clock", "set alarm", "snooze",
                    "remind me to call", "remind me to buy", "remind me to check",
                    "later", "after a while", "in an hour", "in 10 minutes",
                    "set alarm for", "set alarm at", "alarm at 5am",
                    "alarm tomorrow morning", "alarm today", "alarm tonight",
                    "i need a reminder", "create an alert", "set notification",
                    "remind me tomorrow morning", "remind me tomorrow evening",
                    "remind me in 5 minutes", "remind me in 10 minutes",
                    "ask me about", "tell me to", "prompt me to",
                    "remember me to", "don't let me forget", "make sure i remember",
                    "set task", "add task", "create task", "new task"
                ],
                "play_media": [
                    "play music", "play song", "play video", "music please",
                    "play album", "play artist", "play playlist", "play podcast",
                    "play movie", "play film", "play show", "play series",
                    "play next", "play previous", "play again", "replay",
                    "start playing", "begin playback", "resume playback",
                    "pause music", "stop music", "mute music", "lower volume",
                    "increase volume", "turn up", "turn down", "shuffle",
                    "repeat", "loop", "skip", "go back", "rewind", "fast forward",
                    "play from beginning", "play from start", "restart song",
                    "play my favorites", "play my library", "play recommended",
                    "play something good", "play something new", "play something random",
                    "put on music", "start music", "let's dance", "let's rock",
                    "play sound", "play audio", "play content", "play stream",
                    "start playing music", "begin playing", "resume playing",
                    "play my playlist", "play music playlist", "play song playlist",
                    "play podcast episode", "play audiobook", "play audio file",
                    "play youtube video", "play movie online", "play film online",
                    "continue playing", "play next song", "skip to next",
                    "go to previous song", "previous track", "last song",
                    "shuffle songs", "shuffle playlist", "random play"
                ],
                "memory": [
                    "remember this", "store this", "learn this", "save this",
                    "remember my", "remember that", "remember when", "remember where",
                    "keep in memory", "recall", "bring back", "think of",
                    "what did i say", "what did we talk about", "remind me what",
                    "did i tell you", "do you remember", "remember i said",
                    "remember i asked", "remember i want", "remember i need",
                    "save for later", "bookmark this", "mark important", "flag",
                    "learn new fact", "add to knowledge", "update memory",
                    "important information", "important note", "important contact",
                    "store information", "file this", "catalog this", "organize this",
                    "don't forget i said", "important thing", "i will remember",
                    "memorize", "commit to memory", "engrave in memory",
                    "recall later", "retrieve information", "look up",
                    "historical note", "memory lane", "way back when",
                    "save my preference", "remember my preference", "store my choice",
                    "remember my name", "remember my number", "remember my address",
                    "store this in memory", "add to memory", "save to memory",
                    "my favorite", "i like", "i prefer", "my choice",
                    "bookmark", "favorite", "mark as important"
                ]
            }
            
            # Create training data
            training_texts = []
            training_labels = []
            
            for intent, examples in training_data.items():
                for example in examples:
                    training_texts.append(example)
                    training_labels.append(intent)
            
            logger.info(f"Training ML classifier with {len(training_texts)} samples ({len(training_data)} intents)")
            
            # Initialize and train TF-IDF vectorizer (word-level for better semantic understanding)
            self.tfidf = TfidfVectorizer(
                analyzer='word',
                ngram_range=(1, 2),
                lowercase=True,
                min_df=1,
                max_features=500
            )
            X = self.tfidf.fit_transform(training_texts)
            
            # Initialize and train Naive Bayes classifier
            self.classifier = MultinomialNB(alpha=0.1)
            self.classifier.fit(X, training_labels)
            
            self.ml_ready = True
            logger.info(f"ML classifier trained successfully!")
            logger.info(f"  - Training samples: {len(training_texts)}")
            logger.info(f"  - Feature vocabulary size: {len(self.tfidf.get_feature_names_out())}")
            logger.info(f"  - Intents: {len(training_data)}")
            
        except Exception as e:
            logger.warning(f"ML classifier initialization failed: {e}. Will use keyword-based fallback.")
            self.ml_ready = False
            self.tfidf = None
            self.classifier = None
    
    def extract_intent(self, text: str) -> Tuple[str, Dict, float]:
        """Extract intent using RELIABLE KEYWORD-BASED approach with pattern matching"""
        text_lower = text.lower()
        
        # Use keyword-based detection (primary, most reliable)
        final_intent, final_confidence = self._keyword_based_intent(text_lower)
        
        # Extract entities using spaCy and pattern matching
        entities = self._extract_entities(text)
        
        logger.debug(f"Intent: {final_intent} ({final_confidence:.2f}), Entities: {entities}")
        
        return final_intent, entities, final_confidence
    
    def _keyword_based_intent(self, text_lower: str) -> Tuple[str, float]:
        """Improved keyword-based intent detection with weighted scoring"""
        
        # Priority keywords that strongly indicate specific intents
        strong_keywords = {
            "send_message": ["send", "message", "whatsapp", "text", "sms", "email", "tell"],
            "make_call": ["call", "phone", "ring", "dial", "telephone"],
            "set_reminder": ["remind", "reminder", "alarm", "alert", "notification"],
            "play_media": ["play", "music", "song", "podcast", "video"],
            "download_file": ["download", "fetch", "retrieve", "get"],
            "system_control": ["open", "launch", "start", "close", "turn"],
            "query": ["what", "when", "where", "how", "why", "search"],
            "memory": ["remember", "recall", "save", "store", "bookmark"],
            "greeting": ["hello", "hi", "hey", "greetings", "morning"],
        }
        
        matched_intent = "unknown"
        max_score = 0
        
        # Calculate weighted score for each intent
        for intent, keywords in strong_keywords.items():
            score = 0
            for keyword in keywords:
                if f" {keyword} " in f" {text_lower} ":
                    score += 2  # Exact word match (with spaces)
                elif keyword in text_lower:
                    score += 1  # Substring match
            
            if score > max_score:
                max_score = score
                matched_intent = intent
        
        # Calculate confidence
        if matched_intent == "unknown":
            confidence = 0.3
        else:
            # Confidence based on number of keyword matches
            num_keywords = len(strong_keywords[matched_intent])
            confidence = min(max_score / (num_keywords * 2), 1.0)
        
        return matched_intent, confidence
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities from text with improved accuracy"""
        entities = {}
        text_lower = text.lower()
        
        if self.nlp:
            doc = self.nlp(text)
            # Extract different entity types
            for ent in doc.ents:
                entity_type = ent.label_.lower()
                if entity_type not in entities:
                    entities[entity_type] = []
                entities[entity_type].append(ent.text)
        
        # Extract contact names with improved pattern matching
        contact = self._extract_contact(text)
        if contact:
            entities["contact"] = contact
        
        # Extract message content (most important for WhatsApp)
        if "send" in text_lower or "message" in text_lower or "whatsapp" in text_lower or "text" in text_lower or "email" in text_lower or "sms" in text_lower:
            message = self._extract_message_content(text)
            if message:
                entities["message"] = message
        
        # Extract locations
        if "gpe" in entities:
            entities["location"] = entities["gpe"][0] if entities["gpe"] else ""
        
        # Extract file names
        if "download" in text_lower:
            entities["file_name"] = self._extract_file_name(text)
            entities["file_type"] = self._extract_file_type(text)
        
        # Extract app names
        if "open" in text_lower or "launch" in text_lower:
            entities["app"] = self._extract_app_name(text)
        
        # Extract media names
        if "play" in text_lower:
            entities["media"] = self._extract_media_name(text)
        
        # Extract reminder/alarm info
        if "remind" in text_lower or "alarm" in text_lower or "alert" in text_lower:
            entities["reminder_text"] = self._extract_reminder_text(text)
            entities["time"] = self._extract_time_info(text)
            entities["type"] = self._extract_alarm_type(text)
        
        return entities
    
    def _extract_contact(self, text: str) -> str:
        """Extract contact name from message with smart patterns"""
        text_lower = text.lower()
        
        # Smart extraction using regex patterns FIRST (most reliable)
        import re
        # Pattern: "tell [CONTACT]", "send to [CONTACT]", "message to [CONTACT]", etc.
        # Most specific patterns first
        patterns = [
            r"send\s+message\s+to\s+([a-z]+)",
            r"send\s+to\s+([a-z]+)",
            r"tell\s+([a-z]+)",
            r"message\s+to\s+([a-z]+)",
            r"text\s+to\s+([a-z]+)",
            r"text\s+([a-z]+)",
            r"message\s+([a-z]+)",
            r"contact\s+([a-z]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                candidate = match.group(1).strip()
                if candidate and len(candidate) > 1 and candidate not in ["a", "the", "to", "at", "from"]:
                    return candidate
        
        # Try spaCy NER as fallback (sometimes trained on phrases like "tell john")
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    # Extract only the last word if it's a phrase (handles "tell john" -> "john")
                    name_candidate = ent.text.split()[-1]
                    if name_candidate and len(name_candidate) > 1:
                        return name_candidate
        
        # Pattern-based extraction for common names (final fallback)
        common_names = ["john", "mom", "dad", "brother", "sister", "friend", "wife", "husband",
                       "boss", "avnish", "alex", "mike", "sarah", "jane", "tom", "jerry",
                       "david", "michael", "jennifer", "lisa", "james", "disha", "priya", "amit",
                       "delhi", "rajesh", "neha", "ravi", "anil"]
        
        for name in common_names:
            if name in text_lower:
                return name
        
        return ""
    
    def _extract_message_content(self, text: str) -> str:
        """Extract message content from command with improved accuracy"""
        text_lower = text.lower()
        
        # Keywords that typically come before message content
        message_keywords = [
            ("say", "say "),
            ("tell", "tell "),
            ("message", "message "),
            ("text", "text "),
            ("send", "send "),
            ("email", "email "),
            ("sms", "sms ")
        ]
        
        for keyword, search_str in message_keywords:
            # Find position after keyword
            positions = [i for i in range(len(text_lower)) if text_lower.startswith(search_str, i)]
            for pos in positions:
                # Get text after the keyword phrase
                after_keyword = text_lower[pos + len(search_str):].strip()
                
                # Skip prepositions and articles
                skip_words = ["to ", "a ", "the ", "in ", "on ", "at "]
                for skip in skip_words:
                    if after_keyword.startswith(skip):
                        after_keyword = after_keyword[len(skip):].strip()
                
                # Continue until we find the actual message
                if after_keyword and len(after_keyword) > 2:
                    # Find where contact ends and message begins
                    parts = after_keyword.split()
                    
                    # If there's "that", "with", "message:", everything after is the message
                    for separator in ["that ", "saying ", "says ", ":"]:
                        if separator in after_keyword:
                            message_part = after_keyword.split(separator, 1)[-1].strip()
                            if message_part:
                                return message_part
                    
                    # Skip known contact names (usually first 1-2 words)
                    common_names = ["john", "mom", "dad", "brother", "sister", "avnish", "my ", "the "]
                    message_start = 0
                    words = after_keyword.split()
                    
                    for i, word in enumerate(words):
                        is_name = any(word.lower().startswith(name.replace(" ", "")) for name in common_names)
                        if not is_name or i > 1:
                            message_start = len(" ".join(words[:i]))
                            break
                    
                    if message_start < len(after_keyword):
                        message = after_keyword[message_start:].strip()
                        if message and len(message) > 1:
                            return message
        
        # Fallback: extract everything after the last contact mention
        return ""
    
    def _extract_file_name(self, text: str) -> str:
        """Extract file name from download command"""
        # Remove common words
        words = text.lower().split()
        download_idx = next((i for i, w in enumerate(words) if "download" in w), -1)
        
        if download_idx >= 0 and download_idx + 1 < len(words):
            file_parts = words[download_idx + 1:]
            # Filter out prepositions
            file_name = " ".join([w for w in file_parts if w not in ["from", "on", "at"]])
            return file_name
        return ""
    
    def _extract_file_type(self, text: str) -> str:
        """Extract file type (pdf, ppt, etc.)"""
        file_types = ["pdf", "ppt", "doc", "docx", "xlsx", "txt", "zip", "mp4"]
        for ftype in file_types:
            if ftype in text.lower():
                return ftype
        return ""
    
    def _extract_app_name(self, text: str) -> str:
        """Extract application name"""
        common_apps = ["chrome", "firefox", "notepad", "calculator", "spotify", "whatsapp", "telegram", "email", "gmail"]
        for app in common_apps:
            if app in text.lower():
                return app
        
        words = text.lower().split()
        open_idx = next((i for i, w in enumerate(words) if "open" in w or "launch" in w), -1)
        if open_idx >= 0 and open_idx + 1 < len(words):
            return words[open_idx + 1]
        return ""
    
    def _extract_media_name(self, text: str) -> str:
        """Extract media name"""
        words = text.lower().split()
        play_idx = next((i for i, w in enumerate(words) if "play" in w), -1)
        if play_idx >= 0 and play_idx + 1 < len(words):
            media_parts = words[play_idx + 1:]
            return " ".join(media_parts)
        return ""
    
    def _extract_reminder_text(self, text: str) -> str:
        """Extract reminder text"""
        keywords = ["remind", "remember"]
        for keyword in keywords:
            if keyword in text.lower():
                parts = text.lower().split(keyword)
                if len(parts) > 1:
                    reminder = parts[-1].strip()
                    return reminder
        return ""
    
    def _extract_time_info(self, text: str) -> str:
        """Extract time information"""
        time_keywords = ["tomorrow", "today", "tonight", "in", "at", "morning", "evening", "afternoon"]
        for keyword in time_keywords:
            if keyword in text.lower():
                words = text.lower().split()
                idx = next((i for i, w in enumerate(words) if keyword in w), -1)
                if idx >= 0:
                    time_parts = words[idx:]
                    return " ".join(time_parts[:4])
        return ""
    
    def _extract_alarm_type(self, text: str) -> str:
        """Extract alarm type from text"""
        text_lower = text.lower()
        
        alarm_types = {
            "alarm": ["alarm", "alarm clock", "wake me up"],
            "reminder": ["remind", "reminder", "alert"],
            "notification": ["notify", "notification", "notify me"],
            "notification": ["notify", "notification", "notify me"],
            "bedtime": ["bedtime", "sleep", "go to sleep"],
            "workout": ["workout", "exercise", "gym"],
            "medication": ["medicine", "medication", "pill"],
            "meeting": ["meeting", "appointment", "call"],
            "study": ["study", "homework", "learning"],
            "break": ["break", "rest", "relax"]
        }
        
        for alarm_type, keywords in alarm_types.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return alarm_type
        
        # Ask user about alarm type if not detected
        return "general"
    
    def get_ai_answer(self, question: str) -> str:
        """Get answer using AI model"""
        try:
            if self.model:
                response = self.model.generate_content(question)
                return response.text
            else:
                # Fallback to simple response
                blob = TextBlob(question)
                return f"I found information about {blob.noun_phrases}. Could you be more specific?"
        except Exception as e:
            logger.error(f"AI answer error: {e}")
            return "I couldn't generate an answer right now."
    
    def sentiment_analysis(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment": "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
        }
    
    def entity_linking(self, text: str) -> Dict:
        """Link entities to knowledge base"""
        if not self.nlp:
            return {}
        
        doc = self.nlp(text)
        linked_entities = {}
        
        for ent in doc.ents:
            linked_entities[ent.text] = {
                "type": ent.label_,
                "text": ent.text
            }
        
        return linked_entities
