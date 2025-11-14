package com.voiceassistant.app

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import java.util.Locale

class TextToSpeechManager(context: Context) : TextToSpeech.OnInitListener {
    private var tts: TextToSpeech? = null
    private var isReady = false

    companion object {
        private const val TAG = "TextToSpeechManager"
    }

    init {
        tts = TextToSpeech(context, this)
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            tts?.language = Locale.ENGLISH
            tts?.setSpeechRate(1.0f)
            isReady = true
            Log.d(TAG, "TextToSpeech initialized successfully")
        } else {
            Log.e(TAG, "TextToSpeech initialization failed")
        }
    }

    fun speak(text: String) {
        if (isReady && tts != null) {
            tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null)
            Log.d(TAG, "Speaking: $text")
        } else {
            Log.w(TAG, "TextToSpeech not ready")
        }
    }

    fun stop() {
        tts?.stop()
    }

    fun shutdown() {
        tts?.shutdown()
    }
}
