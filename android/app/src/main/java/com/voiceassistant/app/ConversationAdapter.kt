package com.voiceassistant.app

import android.view.LayoutInflater
import android.view.TextView
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView

data class Message(
    val text: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis()
)

class ConversationAdapter(private val messages: MutableList<Message>) :
    RecyclerView.Adapter<ConversationAdapter.MessageViewHolder>() {

    inner class MessageViewHolder(itemView: android.view.View) : RecyclerView.ViewHolder(itemView) {
        fun bind(message: Message) {
            val textView = itemView.findViewById<TextView>(android.R.id.text1)
            textView.text = message.text

            if (message.isUser) {
                textView.setBackgroundColor(itemView.context.getColor(R.color.primary_light))
                textView.gravity = android.view.Gravity.END
            } else {
                textView.setBackgroundColor(itemView.context.getColor(R.color.info_blue))
                textView.gravity = android.view.Gravity.START
                textView.setTextColor(itemView.context.getColor(R.color.white))
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MessageViewHolder {
        val textView = TextView(parent.context).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
            setPadding(16, 12, 16, 12)
            textSize = 14f
        }
        return MessageViewHolder(textView)
    }

    override fun onBindViewHolder(holder: MessageViewHolder, position: Int) {
        holder.bind(messages[position])
    }

    override fun getItemCount() = messages.size

    fun addMessage(message: Message) {
        messages.add(message)
        notifyItemInserted(messages.size - 1)
    }
}
