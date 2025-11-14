package com.voiceassistant.app;

import android.app.Service;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.RecognitionListener;
import android.telecom.TelecomManager;
import android.widget.Toast;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONException;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.Locale;

public class VoiceRecognitionService extends Service implements RecognitionListener {

    private SpeechRecognizer speechRecognizer;
    private RequestQueue requestQueue;
    private Handler handler;
    private static final String API_URL = "http://192.168.x.x:5000/api/process-command";
    private AdvancedFeaturesHandler advancedFeatures;
    private LearningSystem learningSystem;
    private LocalBroadcastManager broadcastManager;
    private TextToSpeechManager ttsManager;
    private SharedPreferences prefs;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        handler = new Handler(Looper.getMainLooper());
        requestQueue = Volley.newRequestQueue(this);
        advancedFeatures = new AdvancedFeaturesHandler(this);
        learningSystem = new LearningSystem(this);
        broadcastManager = LocalBroadcastManager.getInstance(this);
        ttsManager = new TextToSpeechManager(this);
        prefs = getSharedPreferences("aari_prefs", MODE_PRIVATE);

        // Apply stored speech speed
        float speechSpeed = prefs.getFloat("speech_speed", 1.3f);
        ttsManager.setSpeechRate(speechSpeed);

        startListening();
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private void startListening() {
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        speechRecognizer.setRecognitionListener(this);

        Intent recognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE,
                getApplicationContext().getPackageName());

        speechRecognizer.startListening(recognizerIntent);
    }

    @Override
    public void onReadyForSpeech(Bundle params) {
        showToast("Listening...");
    }

    @Override
    public void onBeginningOfSpeech() {
    }

    @Override
    public void onRmsChanged(float rmsdB) {
    }

    @Override
    public void onBufferReceived(byte[] buffer) {
    }

    @Override
    public void onEndOfSpeech() {
    }

    @Override
    public void onError(int error) {
        showToast("Error: " + error);
        startListening();
    }

    @Override
    public void onResults(Bundle results) {
        ArrayList<String> matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
        if (matches != null && !matches.isEmpty()) {
            String command = matches.get(0);
            processCommand(command);
        }
        startListening();
    }

    @Override
    public void onPartialResults(Bundle partialResults) {
    }

    @Override
    public void onEvent(int eventType, Bundle params) {
    }

    private void processCommand(String command) {
        String lowerCommand = command.toLowerCase();
        learningSystem.logInteraction(command, "Processing...", true);

        // Route to specific handlers based on command type
        if (lowerCommand.contains("whatsapp") || lowerCommand.contains("wa")) {
            handleWhatsAppCommand(command);
        } else if (lowerCommand.contains("call") || lowerCommand.contains("phone")) {
            handleCallCommand(command);
        } else if (lowerCommand.contains("sms") || lowerCommand.contains("text message")) {
            handleSMSCommand(command);
        } else if (lowerCommand.contains("search") || lowerCommand.contains("find")) {
            handleWebSearchCommand(command);
        } else if (lowerCommand.contains("weather")) {
            handleWeatherCommand(command);
        } else if (lowerCommand.contains("news")) {
            handleNewsCommand(command);
        } else if (lowerCommand.contains("play") || lowerCommand.contains("music")) {
            handlePlayAudioCommand(command);
        } else if (lowerCommand.contains("open")) {
            handleOpenAppCommand(command);
        } else if (lowerCommand.contains("update")) {
            handleUpdateCommand(command);
        } else {
            // Default: send to backend
            sendToBackend(command);
        }
    }

    private void handleWhatsAppCommand(String command) {
        try {
            JSONObject jsonBody = new JSONObject();
            jsonBody.put("command", command);

            JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, API_URL,
                    jsonBody,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                String contactNumber = response.optString("contact_number", "");
                                String message = response.optString("message", "Hi");

                                if (!contactNumber.isEmpty()) {
                                    advancedFeatures.sendWhatsAppMessage(contactNumber, message);
                                    speakResponse(
                                            "WhatsApp message sent to " + response.optString("contact", "contact"));
                                    learningSystem.logInteraction(command, "WhatsApp sent", true);
                                }
                            } catch (Exception e) {
                                speakResponse("Error sending WhatsApp");
                                learningSystem.logInteraction(command, "WhatsApp failed: " + e.getMessage(), false);
                            }
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            speakResponse("Error: " + error.getMessage());
                            learningSystem.logInteraction(command, "Error: " + error.getMessage(), false);
                        }
                    });

            requestQueue.add(request);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void handleCallCommand(String command) {
        try {
            JSONObject jsonBody = new JSONObject();
            jsonBody.put("command", command);

            JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, API_URL,
                    jsonBody,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                String contactNumber = response.optString("contact_number", "");
                                if (!contactNumber.isEmpty()) {
                                    advancedFeatures.makeCall(contactNumber);
                                    speakResponse("Calling " + response.optString("contact", "contact"));
                                    learningSystem.logInteraction(command, "Call made", true);
                                }
                            } catch (Exception e) {
                                speakResponse("Error making call");
                                learningSystem.logInteraction(command, "Call failed", false);
                            }
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            speakResponse("Error: " + error.getMessage());
                            learningSystem.logInteraction(command, "Call error", false);
                        }
                    });

            requestQueue.add(request);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void handleSMSCommand(String command) {
        try {
            JSONObject jsonBody = new JSONObject();
            jsonBody.put("command", command);

            JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, API_URL,
                    jsonBody,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                String contactNumber = response.optString("contact_number", "");
                                String message = response.optString("message", "Hi");

                                if (!contactNumber.isEmpty()) {
                                    advancedFeatures.sendSMS(contactNumber, message);
                                    speakResponse("SMS sent successfully");
                                    learningSystem.logInteraction(command, "SMS sent", true);
                                }
                            } catch (Exception e) {
                                speakResponse("Error sending SMS");
                                learningSystem.logInteraction(command, "SMS failed", false);
                            }
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            speakResponse("Error: " + error.getMessage());
                            learningSystem.logInteraction(command, "SMS error", false);
                        }
                    });

            requestQueue.add(request);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void handleWebSearchCommand(String command) {
        String query = command.replaceAll("(?i)search|find", "").trim();
        advancedFeatures.webSearch(query, new AdvancedFeaturesHandler.ApiCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                speakResponse("Search completed for " + query);
                learningSystem.logInteraction(command, "Search successful", true);
            }

            @Override
            public void onError(String error) {
                speakResponse("Search failed: " + error);
                learningSystem.logInteraction(command, "Search failed", false);
            }
        });
    }

    private void handleWeatherCommand(String command) {
        String location = command.replaceAll("(?i)weather", "").trim();
        advancedFeatures.getWeather(location, new AdvancedFeaturesHandler.ApiCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                speakResponse("Weather information loaded");
                learningSystem.logInteraction(command, "Weather fetched", true);
            }

            @Override
            public void onError(String error) {
                speakResponse("Weather fetch failed");
                learningSystem.logInteraction(command, "Weather failed", false);
            }
        });
    }

    private void handleNewsCommand(String command) {
        String topic = command.replaceAll("(?i)news", "").trim();
        advancedFeatures.getNews(topic, new AdvancedFeaturesHandler.ApiCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                speakResponse("News loaded for " + topic);
                learningSystem.logInteraction(command, "News fetched", true);
            }

            @Override
            public void onError(String error) {
                speakResponse("News fetch failed");
                learningSystem.logInteraction(command, "News failed", false);
            }
        });
    }

    private void handlePlayAudioCommand(String command) {
        String query = command.replaceAll("(?i)play|music", "").trim();
        if (advancedFeatures.playAudio(query)) {
            speakResponse("Playing " + query);
            learningSystem.logInteraction(command, "Audio playing", true);
        } else {
            speakResponse("Failed to play audio");
            learningSystem.logInteraction(command, "Audio play failed", false);
        }
    }

    private void handleOpenAppCommand(String command) {
        String url = command.replaceAll("(?i)open", "").trim();
        if (advancedFeatures.openURL(url)) {
            speakResponse("Opening " + url);
            learningSystem.logInteraction(command, "URL opened", true);
        } else {
            speakResponse("Failed to open URL");
            learningSystem.logInteraction(command, "URL open failed", false);
        }
    }

    private void handleUpdateCommand(String command) {
        advancedFeatures.checkUpdates(new AdvancedFeaturesHandler.ApiCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                speakResponse("Update check completed");
                learningSystem.logInteraction(command, "Updates checked", true);
            }

            @Override
            public void onError(String error) {
                speakResponse("Update check failed");
                learningSystem.logInteraction(command, "Update check failed", false);
            }
        });
    }

    private void sendToBackend(String command) {
        try {
            JSONObject jsonBody = new JSONObject();
            jsonBody.put("command", command);

            JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, API_URL,
                    jsonBody,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                String assistantResponse = response.getString("response");
                                speakResponse(assistantResponse);
                                learningSystem.logInteraction(command, assistantResponse, true);
                            } catch (JSONException e) {
                                speakResponse("Error processing response");
                                learningSystem.logInteraction(command, "Processing error", false);
                                e.printStackTrace();
                            }
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            speakResponse("Error: " + error.getMessage());
                            learningSystem.logInteraction(command, "API error", false);
                        }
                    });

            requestQueue.add(request);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void speakResponse(String text) {
        showToast("Assistant: " + text);
        // Speak using fast TTS (Alexa-like speed)
        if (ttsManager != null && ttsManager.isReady()) {
            ttsManager.speak(text);
        }
    }

    private void showToast(String message) {
        handler.post(() -> Toast.makeText(VoiceRecognitionService.this,
                message, Toast.LENGTH_SHORT).show());
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (speechRecognizer != null) {
            speechRecognizer.destroy();
        }
        if (ttsManager != null) {
            ttsManager.shutdown();
        }
    }
}
