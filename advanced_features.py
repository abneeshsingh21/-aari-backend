"""
Advanced Features Module for Voice Assistant
Includes machine learning, pattern recognition, and advanced NLP
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)


class AdvancedFeatures:
    """Advanced features for intelligent assistant"""
    
    def __init__(self):
        self.learning_database = self._load_learning_db()
        self.user_patterns = defaultdict(list)
        self.command_frequency = Counter()
    
    def _load_learning_db(self) -> Dict:
        """Load learning database"""
        db_file = "learning_database.json"
        if os.path.exists(db_file):
            try:
                with open(db_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_db()
        return self._default_db()
    
    def _default_db(self) -> Dict:
        """Default learning database structure"""
        return {
            "user_preferences": {},
            "frequently_used_commands": [],
            "learned_patterns": [],
            "contact_aliases": {},
            "location_mappings": {},
            "time_preferences": {}
        }
    
    def learn_user_preference(self, preference_type: str, data: Any):
        """Learn user preferences over time"""
        if preference_type not in self.learning_database["user_preferences"]:
            self.learning_database["user_preferences"][preference_type] = []
        
        self.learning_database["user_preferences"][preference_type].append({
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_learning_db()
    
    def predict_next_command(self, conversation_history: List[str]) -> str:
        """Predict what user might want next"""
        if not conversation_history:
            return ""
        
        last_command = conversation_history[-1]
        
        # Simple pattern matching
        if "send" in last_command:
            return "Would you like to call them?"
        elif "call" in last_command:
            return "Should I leave a voicemail?"
        elif "search" in last_command:
            return "Would you like to download any results?"
        
        return ""
    
    def detect_user_mood(self, text: str) -> str:
        """Detect user mood from text"""
        happy_words = ["great", "awesome", "excellent", "love", "happy"]
        sad_words = ["sad", "bad", "terrible", "hate", "angry"]
        
        text_lower = text.lower()
        
        happy_count = sum(1 for word in happy_words if word in text_lower)
        sad_count = sum(1 for word in sad_words if word in text_lower)
        
        if happy_count > sad_count:
            return "happy"
        elif sad_count > happy_count:
            return "sad"
        return "neutral"
    
    def suggest_command(self, time_of_day: str = None) -> str:
        """Suggest commands based on time and patterns"""
        if not time_of_day:
            hour = datetime.now().hour
            if 6 <= hour < 12:
                time_of_day = "morning"
            elif 12 <= hour < 18:
                time_of_day = "afternoon"
            else:
                time_of_day = "evening"
        
        suggestions = {
            "morning": ["Check weather", "Read news", "Check calendar"],
            "afternoon": ["Send reminder", "Check emails", "Play music"],
            "evening": ["Play relaxing music", "Set reminders", "Call someone"]
        }
        
        return suggestions.get(time_of_day, ["Ask me anything"])[0]
    
    def track_command_frequency(self, command: str):
        """Track frequency of commands"""
        self.command_frequency[command] += 1
    
    def get_most_used_commands(self, limit: int = 5) -> List[str]:
        """Get most frequently used commands"""
        return [cmd for cmd, _ in self.command_frequency.most_common(limit)]
    
    def create_command_shortcut(self, shortcut_name: str, command: str):
        """Create shortcuts for frequently used commands"""
        self.learning_database["frequently_used_commands"].append({
            "shortcut": shortcut_name,
            "command": command,
            "created_at": datetime.now().isoformat()
        })
        self._save_learning_db()
    
    def learn_contact_alias(self, real_name: str, alias: str):
        """Learn contact nicknames/aliases"""
        self.learning_database["contact_aliases"][alias] = real_name
        self._save_learning_db()
    
    def resolve_alias(self, alias: str) -> str:
        """Resolve alias to real contact name"""
        return self.learning_database["contact_aliases"].get(alias, alias)
    
    def predict_user_intent_pattern(self, recent_commands: List[str]) -> str:
        """Detect patterns in user behavior"""
        if len(recent_commands) < 2:
            return "general"
        
        # Check for work-related pattern
        work_keywords = ["send email", "open", "search", "download"]
        work_count = sum(1 for cmd in recent_commands if any(kw in cmd for kw in work_keywords))
        
        if work_count / len(recent_commands) > 0.5:
            return "work_mode"
        
        # Check for entertainment pattern
        entertainment_keywords = ["play", "music", "video", "search"]
        ent_count = sum(1 for cmd in recent_commands if any(kw in cmd for kw in entertainment_keywords))
        
        if ent_count / len(recent_commands) > 0.5:
            return "entertainment_mode"
        
        return "mixed_mode"
    
    def adaptive_response(self, command: str, user_mood: str) -> str:
        """Generate adaptive responses based on context"""
        base_responses = {
            "happy": "I'm glad you're happy! ",
            "sad": "I'm here to help. ",
            "neutral": "Let me help you with that. "
        }
        
        return base_responses.get(user_mood, "Let me help you. ")
    
    def _save_learning_db(self):
        """Save learning database to file"""
        try:
            with open("learning_database.json", 'w') as f:
                json.dump(self.learning_database, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving learning database: {e}")
    
    def get_context_aware_response(self, command: str, context: Dict) -> str:
        """Generate context-aware response"""
        user_name = context.get("user_name", "User")
        time_of_day = context.get("time_of_day", "afternoon")
        
        if "hello" in command.lower() or "hi" in command.lower():
            greetings = {
                "morning": f"Good morning, {user_name}!",
                "afternoon": f"Good afternoon, {user_name}!",
                "evening": f"Good evening, {user_name}!"
            }
            return greetings.get(time_of_day, f"Hello, {user_name}!")
        
        return f"I'm ready to help you, {user_name}."


class PersonalizationEngine:
    """Personalization engine for user experience"""
    
    def __init__(self):
        self.user_profile = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """Load user profile"""
        if os.path.exists("user_profile.json"):
            try:
                with open("user_profile.json", 'r') as f:
                    return json.load(f)
            except:
                return self._default_profile()
        return self._default_profile()
    
    def _default_profile(self) -> Dict:
        """Default user profile"""
        return {
            "name": "User",
            "timezone": "UTC",
            "language": "en",
            "speech_speed": "normal",
            "theme": "light",
            "privacy_level": "high",
            "interests": [],
            "preferences": {}
        }
    
    def update_profile(self, key: str, value: Any):
        """Update user profile"""
        self.user_profile[key] = value
        self._save_profile()
    
    def _save_profile(self):
        """Save user profile"""
        try:
            with open("user_profile.json", 'w') as f:
                json.dump(self.user_profile, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving profile: {e}")
    
    def get_personalized_greeting(self) -> str:
        """Get personalized greeting"""
        user_name = self.user_profile.get("name", "User")
        hour = datetime.now().hour
        
        if 6 <= hour < 12:
            greeting = f"Good morning, {user_name}! How can I assist you today?"
        elif 12 <= hour < 18:
            greeting = f"Good afternoon, {user_name}! What can I do for you?"
        else:
            greeting = f"Good evening, {user_name}! How may I help you?"
        
        return greeting
