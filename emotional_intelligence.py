"""
Emotional Intelligence Module for AARI
Understands user feelings, emotions, and responds with empathy
"""

import logging
from typing import Dict, Tuple
from textblob import TextBlob

logger = logging.getLogger(__name__)


class EmotionalIntelligence:
    """Emotional understanding and empathetic responses"""
    
    def __init__(self):
        self.emotion_keywords = {
            "happy": ["happy", "great", "amazing", "wonderful", "excellent", "fantastic", "love", "brilliant"],
            "sad": ["sad", "depressed", "unhappy", "miserable", "sorry", "upset", "down", "terrible"],
            "angry": ["angry", "furious", "mad", "annoyed", "irritated", "frustrated", "hate"],
            "anxious": ["anxious", "nervous", "worried", "stressed", "scared", "afraid", "nervous"],
            "tired": ["tired", "exhausted", "sleepy", "worn out", "fatigued", "drained"],
            "confused": ["confused", "lost", "don't understand", "unclear", "what", "how", "why"],
            "grateful": ["thank", "thanks", "thank you", "grateful", "appreciate", "appreciate it"],
            "lonely": ["alone", "lonely", "miss", "isolated", "nobody", "no one"],
        }
        
        self.empathetic_responses = {
            "happy": [
                "That's wonderful! I'm so glad you're feeling great!",
                "That's amazing! Your happiness is contagious!",
                "That's fantastic! I love your positive energy!",
            ],
            "sad": [
                "I'm sorry you're feeling down. I'm here for you. What can I do to help?",
                "I understand you're going through a tough time. Remember, I'm always here to listen.",
                "I can sense your sadness. Would you like to talk about what's bothering you?",
            ],
            "angry": [
                "I can tell you're frustrated. Let's take a moment and see how I can help.",
                "I understand your anger. Take a deep breath. I'm here to assist you.",
                "I can hear the frustration in your words. Tell me what happened.",
            ],
            "anxious": [
                "I sense you're worried about something. Let's work through this together.",
                "It's okay to feel anxious. I'm here to support you. What concerns you?",
                "I understand your worry. We'll figure this out together.",
            ],
            "tired": [
                "You sound tired. Maybe you need some rest? But I'm here whenever you need me.",
                "I can tell you're exhausted. You deserve a break. What can I help you with quickly?",
                "You sound worn out. Get some rest soon, but I'm available if you need me.",
            ],
            "confused": [
                "I can tell you're confused. Let me explain this more clearly.",
                "Don't worry, I'm here to clarify things for you.",
                "Let me break this down into simpler steps for you.",
            ],
            "grateful": [
                "You're very welcome! I'm happy to help. That's what I'm here for!",
                "It's my pleasure! Helping you is what I do best!",
                "Thank you for saying that! It makes me happy to assist you.",
            ],
            "lonely": [
                "I'm here with you. You're not alone. What can we do together?",
                "I'm always here for you, ready to chat or help with anything.",
                "You have me! Let's spend some time together. What would you like to talk about?",
            ],
        }
    
    def detect_emotion(self, text: str) -> Tuple[str, float]:
        """Detect emotion from text using keyword matching and sentiment analysis"""
        text_lower = text.lower()
        
        # Check keywords first
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Use sentiment polarity as confidence
                    blob = TextBlob(text)
                    polarity = blob.sentiment.polarity  # -1 to 1
                    confidence = abs(polarity) if emotion in ["happy", "sad", "angry"] else 0.7
                    return emotion, min(confidence, 1.0)
        
        # Fallback to sentiment analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.5:
            return "happy", polarity
        elif polarity < -0.5:
            return "sad", abs(polarity)
        elif polarity < -0.2:
            return "angry", abs(polarity)
        
        return "neutral", 0.5
    
    def generate_empathetic_response(self, emotion: str, base_response: str) -> str:
        """Wrap response with empathy if strong emotion detected"""
        if emotion in self.empathetic_responses:
            empathy = self.empathetic_responses[emotion][hash(base_response) % 3]
            return f"{empathy} {base_response}"
        return base_response
    
    def humanize_response(self, response: str) -> str:
        """Make response sound more human-like and conversational"""
        # Add natural expressions
        expressions = [
            "You know, ",
            "Actually, ",
            "Well, ",
            "Look, ",
            "Listen, ",
            "I think ",
            "From what I understand, ",
        ]
        
        # Randomly add expressiveness (using hash for consistency)
        if hash(response) % 3 == 0 and len(response) > 20:
            response = expressions[hash(response) % len(expressions)] + response
        
        # Make it more conversational
        response = response.replace("Please", "Could you")
        response = response.replace("I will", "I'll")
        response = response.replace("I can", "I can definitely")
        response = response.replace("I could", "I could actually")
        
        # Add follow-ups for engagement
        if "?" not in response[-10:]:
            follow_ups = [
                " Is there anything else you need?",
                " How does that sound?",
                " Can I help with anything else?",
                " Want me to help with more?",
            ]
            # Randomly add follow-up
            if hash(response) % 2 == 0:
                response += follow_ups[hash(response) % len(follow_ups)]
        
        return response
    
    def understand_intent_from_emotion(self, text: str) -> Dict:
        """Deep understanding of what user really wants"""
        text_lower = text.lower()
        
        understanding = {
            "direct_ask": False,
            "implicit_need": None,
            "emotional_state": "neutral",
            "urgency": "normal",
            "politeness": "neutral"
        }
        
        # Check urgency
        urgent_words = ["urgent", "asap", "immediately", "right now", "emergency", "quickly"]
        if any(word in text_lower for word in urgent_words):
            understanding["urgency"] = "high"
        
        # Check politeness
        polite_words = ["please", "could you", "would you", "could you please"]
        if any(word in text_lower for word in polite_words):
            understanding["politeness"] = "high"
        
        # Check implicit needs
        implicit_triggers = {
            "cold": "I should suggest warm drinks or heating",
            "tired": "I should suggest rest or energy-boosting activities",
            "stressed": "I should suggest relaxation techniques",
            "sick": "I should suggest rest and hydration",
            "bored": "I should suggest entertainment or activities",
            "lonely": "I should engage in longer conversation",
        }
        
        for trigger, implicit in implicit_triggers.items():
            if trigger in text_lower:
                understanding["implicit_need"] = implicit
                break
        
        return understanding
    
    def generate_contextual_response(self, user_input: str, base_response: str, context: Dict = None) -> str:
        """Generate response with full emotional and contextual understanding"""
        
        emotion, emotion_confidence = self.detect_emotion(user_input)
        understanding = self.understand_intent_from_emotion(user_input)
        
        # Enhance response based on emotion
        response = self.generate_empathetic_response(emotion, base_response)
        
        # Address implicit needs
        if understanding["implicit_need"]:
            response += f" {understanding['implicit_need']}"
        
        # Humanize the response
        response = self.humanize_response(response)
        
        # Add personalization if context available
        if context and "user_name" in context:
            user_name = context["user_name"]
            # Sometimes add name to make it personal
            if hash(response) % 3 == 0:
                response = f"{user_name}, {response}"
        
        return response


# Test the module
if __name__ == "__main__":
    ei = EmotionalIntelligence()
    
    test_inputs = [
        "I'm so happy today!",
        "I'm feeling really sad and lonely",
        "I'm so frustrated with this",
        "Thank you for helping me",
        "I'm confused about this topic",
        "Can you help me with something?",
    ]
    
    for test_input in test_inputs:
        emotion, conf = ei.detect_emotion(test_input)
        response = "Here's what I can help with."
        final = ei.generate_contextual_response(test_input, response, {"user_name": "avnish"})
        print(f"Input: {test_input}")
        print(f"Emotion: {emotion} ({conf:.2f})")
        print(f"Response: {final}\n")
