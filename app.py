"""
Flask API Server for Voice Assistant
Enables REST API for Android and desktop integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy initialization
assistant = None
task_executor = None

def get_assistant():
    """Lazy load assistant"""
    global assistant
    if assistant is None:
        try:
            from voice_assistant import VoiceAssistant
            assistant = VoiceAssistant()
        except Exception as e:
            logger.error(f"Failed to initialize VoiceAssistant: {e}")
            return None
    return assistant

def get_task_executor():
    """Lazy load task executor"""
    global task_executor
    if task_executor is None:
        try:
            from task_executor import TaskExecutor
            task_executor = TaskExecutor()
        except Exception as e:
            logger.error(f"Failed to initialize TaskExecutor: {e}")
            return None
    return task_executor


@app.route('/api/process-command', methods=['POST'])
def process_command():
    """Process voice command via API"""
    try:
        data = request.get_json()
        command = data.get('command', '').lower()
        
        if not command:
            return jsonify({"status": "error", "message": "No command provided"}), 400
        
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        # Process command and extract intent/entities
        response = asst.process_command(command)
        
        # Also extract intent and entities for mobile apps
        intent, entities, confidence = asst.nlp_processor.extract_intent(command)
        
        # Build response with metadata
        result = {
            "status": "success",
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "timestamp": json.dumps(__import__('datetime').datetime.now(), default=str)
        }
        
        # Add contact and message info if available
        if entities:
            if entities.get("contact"):
                result["contact"] = entities.get("contact")
                # Get contact number
                contact_number = asst._get_contact_number(entities.get("contact"))
                if contact_number:
                    result["contact_number"] = contact_number
            
            if entities.get("message"):
                result["message"] = entities.get("message")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/send-message', methods=['POST'])
def send_message():
    """Send message via WhatsApp"""
    try:
        data = request.get_json()
        contact = data.get('contact', '')
        message = data.get('message', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.send_whatsapp_message(contact, message)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/make-call', methods=['POST'])
def make_call():
    """Make phone call"""
    try:
        data = request.get_json()
        contact = data.get('contact', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.make_call(contact)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error making call: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/download-file', methods=['POST'])
def download_file():
    """Download file"""
    try:
        data = request.get_json()
        file_name = data.get('file_name', '')
        file_type = data.get('file_type', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.download_file(file_name, file_type)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/open-app', methods=['POST'])
def open_app():
    """Open application"""
    try:
        data = request.get_json()
        app_name = data.get('app_name', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.open_application(app_name)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error opening app: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/search-web', methods=['POST'])
def search_web():
    """Search web"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.search_web(query)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error searching web: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/send-email', methods=['POST'])
def send_email():
    """Send email"""
    try:
        data = request.get_json()
        recipient = data.get('recipient', '')
        subject = data.get('subject', '')
        body = data.get('body', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.send_email(recipient, subject, body)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/set-reminder', methods=['POST'])
def set_reminder():
    """Set reminder"""
    try:
        data = request.get_json()
        reminder_text = data.get('reminder_text', '')
        time_str = data.get('time', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.set_reminder(reminder_text, time_str)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error setting reminder: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/play-media', methods=['POST'])
def play_media():
    """Play media"""
    try:
        data = request.get_json()
        media_name = data.get('media_name', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.play_media(media_name)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error playing media: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/execute-system-command', methods=['POST'])
def execute_system_command():
    """Execute system command"""
    try:
        data = request.get_json()
        action = data.get('action', '')
        
        executor = get_task_executor()
        if executor is None:
            return jsonify({"status": "error", "message": "Executor not available"}), 500
        
        result = executor.execute_system_command(action)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/get-conversation-history', methods=['GET'])
def get_conversation_history():
    """Get conversation history"""
    try:
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        history = asst.get_conversation_history()
        return jsonify({"status": "success", "history": history})
    
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Get assistant status"""
    return jsonify({
        "status": "running",
        "assistant": "AI Voice Assistant",
        "version": "1.0.0",
        "timestamp": json.dumps(__import__('datetime').datetime.now(), default=str)
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/api/remember', methods=['POST'])
def remember():
    """Remember/store important information"""
    try:
        data = request.get_json()
        title = data.get('title', '')
        content = data.get('content', '')
        category = data.get('category', 'general')
        
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        result = asst.memory_manager.remember(title, content, category)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in remember: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/recall', methods=['POST'])
def recall():
    """Recall stored memories"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        memories = asst.memory_manager.recall(query)
        return jsonify({
            "status": "success",
            "memories": memories,
            "count": len(memories)
        })
    
    except Exception as e:
        logger.error(f"Error in recall: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/learn', methods=['POST'])
def learn():
    """Learn a new fact"""
    try:
        data = request.get_json()
        fact = data.get('fact', '')
        value = data.get('value', '')
        
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        result = asst.memory_manager.learn_fact(fact, value)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in learn: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/get-memory', methods=['GET'])
def get_memory():
    """Get all stored memories"""
    try:
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        memories = asst.memory_manager.get_all_memories()
        return jsonify({
            "status": "success",
            "memories": memories
        })
    
    except Exception as e:
        logger.error(f"Error in get_memory: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/clear-memory', methods=['POST'])
def clear_memory():
    """Clear all memories"""
    try:
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        result = asst.memory_manager.clear_memories()
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in clear_memory: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/check-updates', methods=['GET'])
def check_updates():
    """Check for available updates"""
    try:
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        result = asst.auto_updater.check_for_updates()
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error checking updates: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/install-updates', methods=['POST'])
def install_updates():
    """Install available updates"""
    try:
        data = request.get_json()
        features = data.get('features', None)  # Optional specific features list
        
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        result = asst.auto_updater.auto_install_updates(features)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error installing updates: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/update-status', methods=['GET'])
def update_status():
    """Get update system status"""
    try:
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        config = asst.auto_updater._load_config()
        return jsonify({
            "status": "success",
            "auto_update_enabled": config.get("auto_update_enabled"),
            "last_update_check": config.get("last_update_check"),
            "last_feature_update": config.get("last_feature_update"),
            "installed_features": config.get("installed_features", []),
            "update_history": config.get("update_history", [])
        })
    
    except Exception as e:
        logger.error(f"Error getting update status: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/learning-status', methods=['GET'])
def learning_status():
    """Get self-learning system status"""
    try:
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        patterns = asst.self_learning.pattern_db.get("patterns", [])
        success_patterns = [p for p in patterns if p.get("success")]
        
        return jsonify({
            "status": "success",
            "total_interactions": len(patterns),
            "successful_interactions": len(success_patterns),
            "success_rate": len(success_patterns) / len(patterns) if patterns else 0,
            "learning_enabled": True
        })
    
    except Exception as e:
        logger.error(f"Error getting learning status: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/web-search', methods=['POST'])
def web_search():
    """Perform web search"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        num_results = data.get('num_results', 5)
        
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        results = asst.web_search.search(query, num_results)
        return jsonify({
            "status": "success",
            "query": query,
            "results": results,
            "count": len(results)
        })
    
    except Exception as e:
        logger.error(f"Error in web search: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/get-page-content', methods=['POST'])
def get_page_content():
    """Get content from webpage"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        asst = get_assistant()
        if asst is None:
            return jsonify({"status": "error", "message": "Assistant not available"}), 500
        
        content = asst.web_search.get_page_content(url)
        return jsonify({
            "status": "success",
            "url": url,
            "content": content
        })
    
    except Exception as e:
        logger.error(f"Error getting page content: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting Voice Assistant API Server on http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
