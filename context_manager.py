"""
Context Manager - Maintains conversation context and user preferences
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ContextManager:
    """Manage conversation context and user state"""
    
    def __init__(self, context_file: str = "context.json"):
        self.context_file = context_file
        self.context = self._load_context()
        self.conversation_memory = []
        self.user_preferences = self.context.get("preferences", {})
    
    def _load_context(self) -> Dict[str, Any]:
        """Load context from file"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_context()
        return self._default_context()
    
    def _default_context(self) -> Dict[str, Any]:
        """Return default context structure"""
        return {
            "user_name": "User",
            "created_at": datetime.now().isoformat(),
            "preferences": {
                "language": "english",
                "voice_speed": "normal",
                "timezone": "UTC",
                "notification_enabled": True,
                "wake_word": "hey assistant"
            },
            "conversation_history": [],
            "learned_contacts": {},
            "frequent_tasks": []
        }
    
    def save_context(self):
        """Save context to file"""
        try:
            with open(self.context_file, 'w') as f:
                json.dump(self.context, f, indent=2)
            logger.info("Context saved")
        except Exception as e:
            logger.error(f"Error saving context: {e}")
    
    def add_to_memory(self, message: str, sender: str = "user"):
        """Add message to conversation memory"""
        self.conversation_memory.append({
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "message": message
        })
        
        # Keep only last 100 messages
        if len(self.conversation_memory) > 100:
            self.conversation_memory = self.conversation_memory[-100:]
    
    def get_memory(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation memory"""
        return self.conversation_memory[-limit:]
    
    def learn_contact(self, name: str, contact_info: Dict):
        """Learn new contact information"""
        self.context["learned_contacts"][name.lower()] = contact_info
        self.save_context()
    
    def learn_frequent_task(self, task_description: str):
        """Track frequently used tasks"""
        tasks = self.context.get("frequent_tasks", [])
        if task_description not in tasks:
            tasks.append(task_description)
            if len(tasks) > 20:
                tasks = tasks[-20:]
            self.context["frequent_tasks"] = tasks
            self.save_context()
    
    def set_preference(self, key: str, value: Any):
        """Set user preference"""
        self.context["preferences"][key] = value
        self.save_context()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        return self.context["preferences"].get(key, default)
    
    def get_wake_word(self) -> str:
        """Get voice assistant wake word"""
        return self.get_preference("wake_word", "hey assistant")
    
    def get_user_name(self) -> str:
        """Get user name"""
        return self.context.get("user_name", "User")
    
    def set_user_name(self, name: str):
        """Set user name"""
        self.context["user_name"] = name
        self.save_context()
    
    def get_context_summary(self) -> str:
        """Get summary of current context"""
        summary = f"""
        User: {self.get_user_name()}
        Language: {self.get_preference('language')}
        Wake Word: {self.get_wake_word()}
        Learned Contacts: {len(self.context.get('learned_contacts', {}))}
        Recent Tasks: {len(self.context.get('frequent_tasks', []))}
        """
        return summary
