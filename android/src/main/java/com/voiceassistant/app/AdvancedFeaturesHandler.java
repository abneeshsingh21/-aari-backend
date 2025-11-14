package com.voiceassistant.app;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.telephony.SmsManager;
import androidx.core.content.ContextCompat;

/**
 * Advanced Features Handler for AARI Android
 * Handles WhatsApp, calling, SMS, web search, and more
 */
public class AdvancedFeaturesHandler {

    private Context context;
    private ApiClient apiClient;
    private LearningSystem learningSystem;

    public AdvancedFeaturesHandler(Context context) {
        this.context = context;
        this.apiClient = ApiClient.getInstance(context);
        this.learningSystem = new LearningSystem(context);
    }

    /**
     * Send WhatsApp message
     */
    public boolean sendWhatsAppMessage(String phoneNumber, String message) {
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW);
            String url = "https://wa.me/" + phoneNumber + "?text=" + Uri.encode(message);
            intent.setData(Uri.parse(url));
            intent.setPackage("com.whatsapp");
            context.startActivity(intent);
            logSuccess("send_whatsapp", "Message sent via WhatsApp");
            return true;
        } catch (Exception e) {
            logFailure("send_whatsapp", e.getMessage());
            return false;
        }
    }

    /**
     * Make phone call
     */
    public boolean makeCall(String phoneNumber) {
        try {
            Intent intent = new Intent(Intent.ACTION_CALL);
            intent.setData(Uri.parse("tel:" + phoneNumber));
            context.startActivity(intent);
            logSuccess("make_call", "Call initiated to " + phoneNumber);
            return true;
        } catch (SecurityException e) {
            logFailure("make_call", "Permission denied");
            return false;
        }
    }

    /**
     * Send SMS
     */
    public boolean sendSMS(String phoneNumber, String message) {
        try {
            SmsManager smsManager = SmsManager.getDefault();
            smsManager.sendTextMessage(phoneNumber, null, message, null, null);
            logSuccess("send_sms", "SMS sent successfully");
            return true;
        } catch (Exception e) {
            logFailure("send_sms", e.getMessage());
            return false;
        }
    }

    /**
     * Web search
     */
    public void webSearch(String query, ApiCallback callback) {
        apiClient.webSearch(query, new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(org.json.JSONObject response) {
                logSuccess("web_search", "Search completed for: " + query);
                callback.onSuccess(response);
            }

            @Override
            public void onError(String error) {
                logFailure("web_search", error);
                callback.onError(error);
            }
        });
    }

    /**
     * Open URL in browser
     */
    public boolean openURL(String url) {
        try {
            if (!url.startsWith("http://") && !url.startsWith("https://")) {
                url = "https://" + url;
            }
            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            context.startActivity(intent);
            logSuccess("open_url", "Opened URL: " + url);
            return true;
        } catch (Exception e) {
            logFailure("open_url", e.getMessage());
            return false;
        }
    }

    /**
     * Play music/audio
     */
    public boolean playAudio(String query) {
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW);
            String youtubeUrl = "https://www.youtube.com/results?search_query=" + Uri.encode(query);
            intent.setData(Uri.parse(youtubeUrl));
            context.startActivity(intent);
            logSuccess("play_audio", "Playing: " + query);
            return true;
        } catch (Exception e) {
            logFailure("play_audio", e.getMessage());
            return false;
        }
    }

    /**
     * Set reminder/alarm
     */
    public boolean setReminder(String title, long timeInMillis) {
        try {
            Intent intent = new Intent(Intent.ACTION_INSERT);
            intent.setType("vnd.android.cursor.item/event");
            intent.putExtra("title", title);
            intent.putExtra("beginTime", timeInMillis);
            context.startActivity(intent);
            logSuccess("set_reminder", "Reminder set: " + title);
            return true;
        } catch (Exception e) {
            logFailure("set_reminder", e.getMessage());
            return false;
        }
    }

    /**
     * Check for updates
     */
    public void checkUpdates(ApiCallback callback) {
        apiClient.checkUpdates(new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(org.json.JSONObject response) {
                logSuccess("check_updates", "Updates checked");
                callback.onSuccess(response);
            }

            @Override
            public void onError(String error) {
                logFailure("check_updates", error);
                callback.onError(error);
            }
        });
    }

    /**
     * Get learning statistics
     */
    public void getLearningStats(ApiCallback callback) {
        try {
            org.json.JSONObject stats = learningSystem.getStatus();
            callback.onSuccess(stats);
        } catch (Exception e) {
            callback.onError(e.getMessage());
        }
    }

    /**
     * Process command with learning
     */
    public void processCommand(String command, ApiCallback callback) {
        apiClient.processCommand(command, new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(org.json.JSONObject response) {
                try {
                    String result = response.optString("response", "");
                    learningSystem.logInteraction(command, result, true);
                    callback.onSuccess(response);
                } catch (Exception e) {
                    callback.onError(e.getMessage());
                }
            }

            @Override
            public void onError(String error) {
                learningSystem.logInteraction(command, error, false);
                callback.onError(error);
            }
        });
    }

    /**
     * Translate text
     */
    public boolean translateText(String text, String targetLanguage) {
        try {
            String translatorUrl = "https://translate.google.com/?sl=auto&tl=" + targetLanguage +
                    "&text=" + Uri.encode(text) + "&op=translate";
            openURL(translatorUrl);
            logSuccess("translate", "Translation opened for: " + text);
            return true;
        } catch (Exception e) {
            logFailure("translate", e.getMessage());
            return false;
        }
    }

    /**
     * Get weather information
     */
    public void getWeather(String location, ApiCallback callback) {
        String query = "weather in " + location;
        webSearch(query, callback);
    }

    /**
     * Get news information
     */
    public void getNews(String topic, ApiCallback callback) {
        String query = "latest news about " + topic;
        webSearch(query, callback);
    }

    /**
     * Get AI recommendations for user queries
     */
    public void getRecommendation(String query, ApiCallback callback) {
        String prompt = "Based on this query: " + query +
                "\n\nProvide a helpful recommendation or suggestion. Be concise and practical.";

        apiClient.processCommand(prompt, new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(org.json.JSONObject response) {
                try {
                    String recommendation = response.optString("response", "I can help with that");
                    callback.onSuccess(response);
                    learningSystem.logInteraction(query, recommendation, true);
                } catch (Exception e) {
                    callback.onError(e.getMessage());
                }
            }

            @Override
            public void onError(String error) {
                callback.onError(error);
                learningSystem.logInteraction(query, "Recommendation failed", false);
            }
        });
    }

    /**
     * Download/Install app from Play Store
     */
    public boolean downloadApp(String appName) {
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setData(Uri.parse("market://search?q=" + appName));
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(intent);

            logSuccess("download_app", "App download initiated: " + appName);
            return true;
        } catch (Exception e) {
            logFailure("download_app", "Cannot access Play Store");
            return false;
        }
    }

    /**
     * Unlock phone for specific commands (with permission)
     */
    public boolean unlockForCommand() {
        try {
            android.app.KeyguardManager km = (android.app.KeyguardManager) context
                    .getSystemService(android.content.Context.KEYGUARD_SERVICE);

            if (km != null && km.isKeyguardLocked()) {
                // Wake up device
                android.os.PowerManager pm = (android.os.PowerManager) context
                        .getSystemService(android.content.Context.POWER_SERVICE);

                if (pm != null) {
                    android.os.PowerManager.WakeLock wakeLock = pm
                            .newWakeLock(android.os.PowerManager.PARTIAL_WAKE_LOCK, "aari:wake");
                    wakeLock.acquire(10000); // Hold for 10 seconds
                    logSuccess("unlock_device", "Device woken for command");
                    return true;
                }
            }
            return true;
        } catch (Exception e) {
            logFailure("unlock_device", e.getMessage());
            return false;
        }
    }

    private void logSuccess(String action, String details) {
        learningSystem.logInteraction(action, details, true);
    }

    private void logFailure(String action, String error) {
        learningSystem.logInteraction(action, error, false);
    }

    /**
     * Callback interface for advanced features
     */
    public interface ApiCallback {
        void onSuccess(org.json.JSONObject response);

        void onError(String error);
    }
}
