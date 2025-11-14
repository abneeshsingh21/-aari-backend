"""
Memory Manager - Stores and retrieves conversations and user preferences
Persistent storage for AARI's learned information about the user
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

MEMORY_FILE = "aari_memory.json"

class MemoryManager:
    """Manages AARI's memory and learning"""
    
    def __init__(self):
        self.memory_file = MEMORY_FILE
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from persistent storage"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
        
        # Default memory structure
        return {
            "user_name": "avnish",
            "preferences": {},
            "important_conversations": [],
            "reminders": [],
            "contacts": {},
            "learned_facts": {},
            "daily_notes": {}
        }
    
    def save_memory(self):
        """Save memory to persistent storage"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
            logger.info("Memory saved successfully")
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def remember(self, title: str, content: str, category: str = "general") -> Dict[str, Any]:
        """Store important conversation or information"""
        try:
            memory_entry = {
                "title": title,
                "content": content,
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "tags": self._extract_tags(content)
            }
            
            self.memory["important_conversations"].append(memory_entry)
            self.save_memory()
            
            logger.info(f"Memory stored: {title}")
            return {
                "status": "success",
                "message": f"I'll remember: {title}"
            }
        except Exception as e:
            logger.error(f"Memory storage error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def recall(self, query: str) -> List[Dict[str, Any]]:
        """Search and retrieve stored memories"""
        try:
            query_lower = query.lower()
            results = []
            
            # Search in important conversations
            for memory in self.memory["important_conversations"]:
                if (query_lower in memory["title"].lower() or
                    query_lower in memory["content"].lower() or
                    query_lower in str(memory.get("tags", [])).lower()):
                    results.append(memory)
            
            # Search in learned facts
            for fact_key, fact_value in self.memory["learned_facts"].items():
                if query_lower in fact_key.lower() or query_lower in str(fact_value).lower():
                    results.append({
                        "title": fact_key,
                        "content": fact_value,
                        "category": "learned_fact",
                        "timestamp": ""
                    })
            
            return results
        except Exception as e:
            logger.error(f"Recall error: {e}")
            return []
    
    def set_preference(self, key: str, value: Any) -> Dict[str, Any]:
        """Store user preference"""
        try:
            self.memory["preferences"][key] = value
            self.save_memory()
            logger.info(f"Preference set: {key} = {value}")
            return {
                "status": "success",
                "message": f"Preference saved: {key}"
            }
        except Exception as e:
            logger.error(f"Preference error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Retrieve user preference"""
        return self.memory["preferences"].get(key, default)
    
    def add_contact(self, name: str, phone: str, email: str = "") -> Dict[str, Any]:
        """Store contact information"""
        try:
            self.memory["contacts"][name.lower()] = {
                "name": name,
                "phone": phone,
                "email": email,
                "added_at": datetime.now().isoformat()
            }
            self.save_memory()
            logger.info(f"Contact added: {name}")
            return {
                "status": "success",
                "message": f"Contact saved: {name}"
            }
        except Exception as e:
            logger.error(f"Contact error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_contact(self, name: str) -> Dict[str, Any]:
        """Retrieve contact information"""
        return self.memory["contacts"].get(name.lower(), {})
    
    def add_daily_note(self, date: str, note: str) -> Dict[str, Any]:
        """Add daily note"""
        try:
            if date not in self.memory["daily_notes"]:
                self.memory["daily_notes"][date] = []
            
            self.memory["daily_notes"][date].append({
                "note": note,
                "timestamp": datetime.now().isoformat()
            })
            self.save_memory()
            logger.info(f"Daily note added for {date}")
            return {
                "status": "success",
                "message": f"Note saved for {date}"
            }
        except Exception as e:
            logger.error(f"Daily note error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def learn_fact(self, fact: str, value: str) -> Dict[str, Any]:
        """Learn and store a fact about the user or world"""
        try:
            self.memory["learned_facts"][fact.lower()] = value
            self.save_memory()
            logger.info(f"Learned fact: {fact} = {value}")
            return {
                "status": "success",
                "message": f"I've learned: {fact}"
            }
        except Exception as e:
            logger.error(f"Learn fact error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract tags from text"""
        # Simple tag extraction (can be enhanced)
        words = text.lower().split()
        return [word for word in words if len(word) > 3]
    
    def get_all_memories(self) -> Dict[str, Any]:
        """Get all stored memories"""
        return self.memory
    
    def clear_memories(self) -> Dict[str, Any]:
        """Clear all memories (for privacy/reset)"""
        try:
            self.memory = {
                "user_name": self.memory.get("user_name", "avnish"),
                "preferences": {},
                "important_conversations": [],
                "reminders": [],
                "contacts": {},
                "learned_facts": {},
                "daily_notes": {}
            }
            self.save_memory()
            logger.info("All memories cleared")
            return {
                "status": "success",
                "message": "All memories have been cleared"
            }
        except Exception as e:
            logger.error(f"Clear memory error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
