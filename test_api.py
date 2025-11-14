"""
Test the Voice Assistant API
Run this script to test all endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_status():
    """Test status endpoint"""
    print("\n=== Testing Status ===")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_process_command():
    """Test command processing"""
    print("\n=== Testing Command Processing ===")
    try:
        response = requests.post(
            f"{BASE_URL}/process-command",
            json={"command": "hello what time is it"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_send_message():
    """Test message sending"""
    print("\n=== Testing Send Message ===")
    try:
        response = requests.post(
            f"{BASE_URL}/send-message",
            json={"contact": "john", "message": "Hello there!"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_make_call():
    """Test call making"""
    print("\n=== Testing Make Call ===")
    try:
        response = requests.post(
            f"{BASE_URL}/make-call",
            json={"contact": "mom"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_download_file():
    """Test file download"""
    print("\n=== Testing Download File ===")
    try:
        response = requests.post(
            f"{BASE_URL}/download-file",
            json={"file_name": "tutorial", "file_type": "pdf"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_open_app():
    """Test opening app"""
    print("\n=== Testing Open App ===")
    try:
        response = requests.post(
            f"{BASE_URL}/open-app",
            json={"app_name": "chrome"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_play_media():
    """Test media playback"""
    print("\n=== Testing Play Media ===")
    try:
        response = requests.post(
            f"{BASE_URL}/play-media",
            json={"media_name": "Billie Eilish"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_set_reminder():
    """Test reminder setting"""
    print("\n=== Testing Set Reminder ===")
    try:
        response = requests.post(
            f"{BASE_URL}/set-reminder",
            json={"reminder_text": "meeting", "time": "tomorrow"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_search_web():
    """Test web search"""
    print("\n=== Testing Search Web ===")
    try:
        response = requests.post(
            f"{BASE_URL}/search-web",
            json={"query": "machine learning"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_conversation_history():
    """Test getting conversation history"""
    print("\n=== Testing Conversation History ===")
    try:
        response = requests.get(f"{BASE_URL}/get-conversation-history")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("=" * 60)
    print("VOICE ASSISTANT API TEST SUITE")
    print("=" * 60)
    
    # Test all endpoints
    test_health()
    test_status()
    test_process_command()
    test_send_message()
    test_make_call()
    test_download_file()
    test_open_app()
    test_play_media()
    test_set_reminder()
    test_search_web()
    test_conversation_history()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
