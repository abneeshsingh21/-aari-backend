package com.voiceassistant.app;

/**
 * Chat message model
 */
public class ChatMessage {
    private String message;
    private String sender; // "user", "assistant", or "error"
    private long timestamp;
    
    public ChatMessage(String message, String sender) {
        this.message = message;
        this.sender = sender;
        this.timestamp = System.currentTimeMillis();
    }
    
    public String getMessage() {
        return message;
    }
    
    public String getSender() {
        return sender;
    }
    
    public long getTimestamp() {
        return timestamp;
    }
}
