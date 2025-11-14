package com.voiceassistant.app;

import android.app.Service;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.RecognitionListener;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.core.app.NotificationCompat;
import android.net.Uri;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.Locale;

/**
 * Enhanced Voice Assistant Service with Background Execution
 * Runs continuously, listens for wake word, speaks responses, performs tasks even when locked
 * Auto-starts on boot and runs as foreground service
 */
public class VoiceAssistantService extends Service implements RecognitionListener {

    private static final String TAG = "VoiceAssistantService";
    private static final String CHANNEL_ID = "aari_service_channel";
    private static final int NOTIFICATION_ID = 1001;
    private Handler handler;
    private HeadsetReceiver headsetReceiver;
    private SpeechRecognizer speechRecognizer;
    private TextToSpeech textToSpeech;
    private AdvancedFeaturesHandler advancedFeatures;
    private LearningSystem learningSystem;
    private LocalBroadcastManager broadcastManager;
    private SharedPreferences prefs;
    private ApiClient apiClient;
    private LocalDatabaseManager dbManager;
    private volatile boolean isListening = false;
    private volatile boolean isAwake = false;
    private String wakeWord = "hey aari";
    private static final int INACTIVITY_TIMEOUT = 30000; // 30 seconds
    private static final int RESTART_DELAY = 2000; // 2 seconds

    @Override
    public void onCreate() {
        super.onCreate();
        Log.i(TAG, "VoiceAssistantService created");

        handler = new Handler(Looper.getMainLooper());
        advancedFeatures = new AdvancedFeaturesHandler(this);
        learningSystem = new LearningSystem(this);
        broadcastManager = LocalBroadcastManager.getInstance(this);
        prefs = getSharedPreferences("aari_prefs", MODE_PRIVATE);
        apiClient = ApiClient.getInstance(this);
        dbManager = new LocalDatabaseManager(this);

        // Read wake word from preferences
        wakeWord = prefs.getString("wake_word", "hey aari").toLowerCase();

        // Initialize Text-to-Speech
        initializeTextToSpeech();

        // Create notification channel for foreground service
        createNotificationChannel();

        // Start as foreground service
        startForegroundNotification();
    }

    /**
     * Initialize Text-to-Speech engine
     */
    private void initializeTextToSpeech() {
        textToSpeech = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                textToSpeech.setLanguage(Locale.US);
                textToSpeech.setPitch(1.0f);
                textToSpeech.setSpeechRate(0.9f);
                Log.i(TAG, "Text-to-Speech initialized");
            } else {
                Log.e(TAG, "Text-to-Speech initialization failed");
            }
        });
    }

    /**
     * Speak response using Text-to-Speech
     */
    private void speakResponse(String response) {
        if (textToSpeech != null && !textToSpeech.isSpeaking()) {
            handler.post(() -> {
                textToSpeech.speak(response, TextToSpeech.QUEUE_FLUSH, null);
            });
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.i(TAG, "Service started - entering background mode");

        // Check if background mode is enabled
        boolean backgroundEnabled = prefs.getBoolean("background_mode_enabled", true); // Default to true
        if (backgroundEnabled) {
            startListeningInBackground();
        }

        setupWakeWordDetection();

        // Return START_STICKY to restart service if killed
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    /**
     * Start listening in background (continuously)
     */
    private void startListeningInBackground() {
        Log.i(TAG, "Starting background listening");
        isAwake = false;
        startSpeechRecognizer();
    }

    /**
     * Initialize speech recognizer
     */
    private void startSpeechRecognizer() {
        if (speechRecognizer == null) {
            speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
            speechRecognizer.setRecognitionListener(this);
        }

        Intent recognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, getPackageName());
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1);

        isListening = true;
        speechRecognizer.startListening(recognizerIntent);
    }

    private void setupWakeWordDetection() {
        headsetReceiver = new HeadsetReceiver();
        IntentFilter filter = new IntentFilter(Intent.ACTION_HEADSET_PLUG);
        LocalBroadcastManager.getInstance(this).registerReceiver(headsetReceiver, filter);
    }

    @Override
    public void onReadyForSpeech(Bundle params) {
        Log.d(TAG, "Ready for speech");
    }

    @Override
    public void onBeginningOfSpeech() {
        Log.d(TAG, "Speech beginning");
    }

    @Override
    public void onRmsChanged(float rmsdB) {
    }

    @Override
    public void onBufferReceived(byte[] buffer) {
    }

    @Override
    public void onEndOfSpeech() {
        Log.d(TAG, "Speech ended");
    }

    @Override
    public void onError(int error) {
        Log.e(TAG, "Speech recognition error: " + error);
        isListening = false;
        // Automatically restart listening
        handler.postDelayed(this::startSpeechRecognizer, RESTART_DELAY);
    }

    @Override
    public void onResults(Bundle results) {
        ArrayList<String> matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);

        if (matches != null && !matches.isEmpty()) {
            String command = matches.get(0).toLowerCase();
            Log.i(TAG, "Recognized: " + command);

            // Check for wake word
            if (!isAwake && command.contains(wakeWord)) {
                isAwake = true;
                Log.i(TAG, "Wake word detected - AARI is now awake");
                broadcastMessage("AARI is now awake. Say your command...");

                // Give time for user to speak command
                handler.postDelayed(this::startSpeechRecognizer, 1000);
            } else if (isAwake) {
                // Process command while awake
                processCommand(command);

                // Reset to sleep after inactivity
                handler.postDelayed(() -> {
                    isAwake = false;
                    Log.i(TAG, "Timeout - AARI is now sleeping");
                    startSpeechRecognizer();
                }, INACTIVITY_TIMEOUT);
            } else {
                // Continue listening for wake word
                startSpeechRecognizer();
            }
        } else {
            startSpeechRecognizer();
        }
    }

    @Override
    public void onPartialResults(Bundle partialResults) {
    }

    @Override
    public void onEvent(int eventType, Bundle params) {
    }

    /**
     * Process voice command
     */
    private void processCommand(String command) {
        Log.i(TAG, "Processing: " + command);

        // Route to appropriate handler
        if (command.contains("call")) {
            handleCallCommand(command);
        } else if (command.contains("download") || command.contains("install")) {
            handleAppDownload(command);
        } else if (command.contains("recommend") || command.contains("suggest")) {
            handleRecommendation(command);
        } else if (command.contains("search")) {
            handleSearchCommand(command);
        } else if (command.contains("whatsapp")) {
            handleWhatsAppCommand(command);
        } else {
            handleGenericCommand(command);
        }
    }

    /**
     * Handle call command - works even on locked screen
     */
    private void handleCallCommand(String command) {
        // Extract contact name
        String contact = command.replaceAll("(?i)call", "").trim();

        try {
            // Query contacts and make call
            advancedFeatures.makeCall(contact);
            broadcastMessage("Calling " + contact);
            learningSystem.logInteraction(command, "Call initiated", true);
        } catch (Exception e) {
            broadcastMessage("Could not make call");
            learningSystem.logInteraction(command, "Call failed: " + e.getMessage(), false);
        }
    }

    /**
     * Handle app download/install
     */
    private void handleAppDownload(String command) {
        String appName = command.replaceAll("(?i)download|install", "").trim();

        // Open Google Play Store with app search
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setData(Uri.parse("market://search?q=" + appName));
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);

            broadcastMessage("Opening Play Store for " + appName);
            learningSystem.logInteraction(command, "App download initiated", true);
        } catch (Exception e) {
            broadcastMessage("Cannot access Play Store");
            learningSystem.logInteraction(command, "App download failed", false);
        }
    }

    /**
     * Handle recommendations
     */
    private void handleRecommendation(String command) {
        String query = command.replaceAll("(?i)recommend|suggest|what should", "").trim();

        // Send to backend for AI recommendations
        ApiClient.getInstance(this).processCommand("Recommend " + query, new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                try {
                    String recommendation = response.optString("response", "I can help with that");
                    broadcastMessage(recommendation);
                    learningSystem.logInteraction(command, recommendation, true);
                } catch (Exception e) {
                    broadcastMessage("Could not get recommendation");
                }
            }

            @Override
            public void onError(String error) {
                broadcastMessage("Error getting recommendation");
                learningSystem.logInteraction(command, "Recommendation failed", false);
            }
        });
    }

    /**
     * Handle search command
     */
    private void handleSearchCommand(String command) {
        String query = command.replaceAll("(?i)search|find", "").trim();

        advancedFeatures.webSearch(query, new AdvancedFeaturesHandler.ApiCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                broadcastMessage("Search completed");
                learningSystem.logInteraction(command, "Search successful", true);
            }

            @Override
            public void onError(String error) {
                broadcastMessage("Search failed");
                learningSystem.logInteraction(command, "Search failed", false);
            }
        });
    }

    /**
     * Handle WhatsApp command
     */
    private void handleWhatsAppCommand(String command) {
        // Extract phone number and message
        String[] parts = command.split("(?i)message");
        if (parts.length >= 1) {
            String phoneNumber = extractPhoneNumber(parts[0]);
            String message = parts.length > 1 ? parts[1].trim() : "Hello";

            advancedFeatures.sendWhatsAppMessage(phoneNumber, message);
            broadcastMessage("WhatsApp message sent");
            learningSystem.logInteraction(command, "WhatsApp sent", true);
        }
    }

    /**
     * Handle generic command via backend
     */
    private void handleGenericCommand(String command) {
        ApiClient.getInstance(this).processCommand(command, new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                try {
                    String result = response.optString("response", "Done");
                    broadcastMessage(result);
                    learningSystem.logInteraction(command, result, true);
                } catch (Exception e) {
                    broadcastMessage("Error processing command");
                }
            }

            @Override
            public void onError(String error) {
                broadcastMessage("Error: " + error);
                learningSystem.logInteraction(command, "Command failed", false);
            }
        });
    }

    private String extractPhoneNumber(String text) {
        String cleaned = text.replaceAll("[^0-9+]", "");
        return cleaned.substring(0, Math.min(15, cleaned.length()));
    }

    /**
     * Broadcast message to UI
     */
    private void broadcastMessage(String message) {
        Intent intent = new Intent("com.voiceassistant.MESSAGE");
        intent.putExtra("message", message);
        broadcastManager.sendBroadcast(intent);
    }

    /**
     * Create notification channel for foreground service (Android 8+)
     */
    private void createNotificationChannel() {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID,
                    "AARI Voice Assistant",
                    NotificationManager.IMPORTANCE_LOW);
            channel.setDescription("Background voice listening service");
            channel.enableVibration(false);
            channel.setSound(null, null);

            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) {
                manager.createNotificationChannel(channel);
            }
        }
    }

    /**
     * Start foreground notification to keep service running
     */
    private void startForegroundNotification() {
        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle("AARI Voice Assistant")
                .setContentText("Listening... Say 'Hey AARI'")
                .setSmallIcon(R.drawable.ic_launcher_foreground)
                .setOngoing(true)
                .setPriority(NotificationCompat.PRIORITY_LOW)
                .setCategory(NotificationCompat.CATEGORY_SERVICE);

        Notification notification = builder.build();
        startForeground(NOTIFICATION_ID, notification);
        Log.i(TAG, "Started as foreground service");
    }

    /**
     * Update notification status
     */
    private void updateNotificationStatus(String status) {
        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle("AARI Voice Assistant")
                .setContentText(status)
                .setSmallIcon(R.drawable.ic_launcher_foreground)
                .setOngoing(true)
                .setPriority(NotificationCompat.PRIORITY_LOW);

        NotificationManager manager = getSystemService(NotificationManager.class);
        if (manager != null) {
            manager.notify(NOTIFICATION_ID, builder.build());
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.i(TAG, "Service destroyed - restarting...");

        if (speechRecognizer != null) {
            try {
                speechRecognizer.destroy();
            } catch (Exception e) {
                Log.e(TAG, "Error destroying speech recognizer", e);
            }
        }

        if (headsetReceiver != null) {
            try {
                LocalBroadcastManager.getInstance(this).unregisterReceiver(headsetReceiver);
            } catch (Exception e) {
                Log.e(TAG, "Error unregistering receiver", e);
            }
        }

        // Restart service if it's destroyed
        handler.postDelayed(() -> {
            Log.i(TAG, "Restarting service after destruction");
            Intent restartIntent = new Intent(this, VoiceAssistantService.class);
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                startForegroundService(restartIntent);
            } else {
                startService(restartIntent);
            }
        }, RESTART_DELAY);
    }
}
