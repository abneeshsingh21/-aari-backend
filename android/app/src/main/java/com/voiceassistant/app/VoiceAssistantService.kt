package com.voiceassistant.app

import android.app.Service
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.media.AudioManager
import android.speech.SpeechRecognizer
import android.speech.RecognitionListener
import android.util.Log
import androidx.core.app.NotificationCompat
import java.util.Locale

class VoiceAssistantService : Service(), RecognitionListener {

    private lateinit var speechRecognizer: SpeechRecognizer
    private lateinit var config: ConfigManager
    private lateinit var api: BackendAPI
    private lateinit var tts: TextToSpeechManager
    private var isListening = false
    private var isProcessing = false

    companion object {
        private const val TAG = "VoiceAssistantService"
        private const val NOTIFICATION_ID = 1
        private const val CHANNEL_ID = "VoiceAssistantChannel"
    }

    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "Service Created")
        try {
            createNotificationChannel()
            startForegroundNotification()
            
            try {
                config = ConfigManager(this)
                Log.d(TAG, "ConfigManager initialized")
            } catch (e: Exception) {
                Log.e(TAG, "Error initializing ConfigManager", e)
                config = ConfigManager(this) // retry once
            }
            
            try {
                api = BackendAPI(this)
                Log.d(TAG, "BackendAPI initialized")
            } catch (e: Exception) {
                Log.e(TAG, "Error initializing BackendAPI", e)
            }
            
            try {
                tts = TextToSpeechManager(this)
                Log.d(TAG, "TextToSpeechManager initialized")
            } catch (e: Exception) {
                Log.e(TAG, "Error initializing TextToSpeechManager", e)
            }
            
            try {
                initializeSpeechRecognizer()
                Log.d(TAG, "SpeechRecognizer initialized")
            } catch (e: Exception) {
                Log.e(TAG, "Error initializing SpeechRecognizer", e)
            }
        } catch (e: Exception) {
            Log.e(TAG, "Critical error in onCreate", e)
        }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d(TAG, "Service Started")
        startListening()
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Voice Assistant",
                NotificationManager.IMPORTANCE_LOW
            )
            channel.description = "Running voice assistant in background"
            val manager = getSystemService(NotificationManager::class.java)
            manager?.createNotificationChannel(channel)
        }
    }

    private fun startForegroundNotification() {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("🎤 AARI Voice Assistant")
            .setContentText("Listening... Say '${config.getWakeWord()}' to activate")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()

        startForeground(NOTIFICATION_ID, notification)
    }

    private fun initializeSpeechRecognizer() {
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
        speechRecognizer.setRecognitionListener(this)
    }

    private fun startListening() {
        if (!isListening) {
            val intent = Intent(android.speech.RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(
                android.speech.RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                android.speech.RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            intent.putExtra(android.speech.RecognizerIntent.EXTRA_LANGUAGE, Locale.ENGLISH)
            intent.putExtra(android.speech.RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
            
            speechRecognizer.startListening(intent)
            isListening = true
            Log.d(TAG, "Listening started")
        }
    }

    override fun onReadyForSpeech(params: android.os.Bundle?) {
        Log.d(TAG, "Ready for speech")
    }

    override fun onBeginningOfSpeech() {
        Log.d(TAG, "Speech detected")
    }

    override fun onRmsChanged(rmsdB: Float) {
        // Audio level changed
    }

    override fun onBufferReceived(buffer: ByteArray?) {
        // Buffer received
    }

    override fun onEndOfSpeech() {
        Log.d(TAG, "Speech ended")
    }

    override fun onError(error: Int) {
        Log.e(TAG, "Recognition error: $error")
        isListening = false
        
        // Restart listening after a short delay
        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
            startListening()
        }, 1000)
    }

    override fun onResults(results: android.os.Bundle?) {
        val matches = results?.getStringArrayList(android.speech.SpeechRecognizer.RESULTS_RECOGNITION)
        if (matches != null && matches.isNotEmpty()) {
            val spokenText = matches[0].lowercase()
            Log.d(TAG, "Recognized: $spokenText")

            // Check for wake word or commands
            if (spokenText.contains(config.getWakeWord()) || spokenText.contains("hello")) {
                processCommand(spokenText)
            }
        }

        isListening = false
        // Restart listening for continuous operation
        startListening()
    }

    override fun onPartialResults(partialResults: android.os.Bundle?) {
        val partial = partialResults?.getStringArrayList(android.speech.SpeechRecognizer.RESULTS_RECOGNITION)
        if (partial != null && partial.isNotEmpty()) {
            Log.d(TAG, "Partial: ${partial[0]}")
        }
    }

    override fun onEvent(eventType: Int, params: android.os.Bundle?) {
        // Event received
    }

    private fun processCommand(command: String) {
        Log.d(TAG, "Processing command: $command")
        isProcessing = true

        try {
            // Remove wake word from command
            val cleanCommand = command
                .replace(config.getWakeWord(), "", ignoreCase = true)
                .replace("hello", "", ignoreCase = true)
                .trim()

            if (cleanCommand.isNotEmpty()) {
                sendCommandToBackend(cleanCommand)
            } else {
                isProcessing = false
                if (::tts.isInitialized) {
                    tts.speak("I'm ready. What would you like me to do?")
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error in processCommand", e)
            isProcessing = false
        }
    }

    private fun sendCommandToBackend(command: String) {
        Log.d(TAG, "Sending command to backend: $command")

        if (!::api.isInitialized) {
            Log.e(TAG, "API not initialized")
            isProcessing = false
            return
        }

        api.processCommand(
            command,
            onSuccess = { response ->
                try {
                    Log.d(TAG, "Backend response: $response")
                    config.addToConversationHistory("User: $command")
                    config.addToConversationHistory("Assistant: $response")
                    if (::tts.isInitialized) {
                        tts.speak(response)
                    }
                    isProcessing = false
                } catch (e: Exception) {
                    Log.e(TAG, "Error handling response", e)
                    isProcessing = false
                }
            },
            onError = { error ->
                Log.e(TAG, "Backend error: $error")
                if (::tts.isInitialized) {
                    tts.speak("I couldn't reach the backend. Please try again.")
                }
                isProcessing = false
            }
        )
    }

    private fun speakReply(text: String) {
        tts.speak(text)
    }

    override fun onDestroy() {
        super.onDestroy()
        try {
            if (::speechRecognizer.isInitialized) {
                speechRecognizer.destroy()
            }
            if (::tts.isInitialized) {
                tts.shutdown()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error in onDestroy", e)
        }
        Log.d(TAG, "Service Destroyed")
    }
}
