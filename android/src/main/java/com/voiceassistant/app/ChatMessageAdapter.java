package com.voiceassistant.app;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import java.util.ArrayList;

/**
 * Adapter for displaying chat messages in Siri-like format
 */
public class ChatMessageAdapter extends ArrayAdapter<ChatMessage> {
    
    public ChatMessageAdapter(Context context, ArrayList<ChatMessage> messages) {
        super(context, 0, messages);
    }
    
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        ChatMessage message = getItem(position);
        
        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.chat_message_item, parent, false);
        }
        
        TextView messageText = convertView.findViewById(R.id.message_text);
        View messageBubble = convertView.findViewById(R.id.message_bubble);
        
        messageText.setText(message.getMessage());
        
        // Style based on sender
        if ("user".equals(message.getSender())) {
            messageBubble.setBackgroundResource(R.drawable.user_message_bg);
            messageText.setTextColor(0xFFFFFFFF);
        } else if ("assistant".equals(message.getSender())) {
            messageBubble.setBackgroundResource(R.drawable.assistant_message_bg);
            messageText.setTextColor(0xFFFFFFFF);
        } else {
            messageBubble.setBackgroundResource(R.drawable.error_message_bg);
            messageText.setTextColor(0xFFFFFFFF);
        }
        
        return convertView;
    }
}
