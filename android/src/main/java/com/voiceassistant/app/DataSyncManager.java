package com.voiceassistant.app;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Handler;
import android.os.Looper;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.Timer;
import java.util.TimerTask;

/**
 * DataSyncManager - Syncs local data with backend
 * Handles offline mode and automatic sync when backend is available
 */
public class DataSyncManager {
    
    private static final String TAG = "DataSyncManager";
    private Context context;
    private LocalDatabaseManager dbManager;
    private ApiClient apiClient;
    private SharedPreferences prefs;
    private Timer syncTimer;
    private Handler handler;
    
    // Sync interval: 5 minutes
    private static final long SYNC_INTERVAL = 5 * 60 * 1000;
    
    private boolean isSyncing = false;
    private boolean isOnline = true;
    
    public interface SyncListener {
        void onSyncStart();
        void onSyncComplete(int itemsSync);
        void onSyncFailed(String error);
        void onOfflineMode();
        void onOnlineMode();
    }
    
    private SyncListener listener;
    
    public DataSyncManager(Context context) {
        this.context = context;
        this.dbManager = new LocalDatabaseManager(context);
        this.apiClient = ApiClient.getInstance(context);
        this.prefs = context.getSharedPreferences("aari_prefs", Context.MODE_PRIVATE);
        this.handler = new Handler(Looper.getMainLooper());
    }
    
    /**
     * Start automatic sync in background
     */
    public void startAutoSync() {
        if (syncTimer != null) {
            return; // Already running
        }
        
        syncTimer = new Timer();
        syncTimer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                syncWithBackend();
            }
        }, 0, SYNC_INTERVAL);
    }
    
    /**
     * Stop automatic sync
     */
    public void stopAutoSync() {
        if (syncTimer != null) {
            syncTimer.cancel();
            syncTimer = null;
        }
    }
    
    /**
     * Sync with backend
     */
    public void syncWithBackend() {
        if (isSyncing) {
            return; // Already syncing
        }
        
        isSyncing = true;
        
        // Check if backend is available
        apiClient.getHealth(new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                handleOnline();
            }
            
            @Override
            public void onError(String error) {
                handleOffline();
            }
        });
    }
    
    /**
     * Handle online state
     */
    private void handleOnline() {
        if (!isOnline) {
            isOnline = true;
            notifyListener(() -> listener.onOnlineMode());
        }
        
        // Sync pending messages
        syncPendingMessages();
        
        // Sync conversation history
        syncConversationHistory();
        
        // Sync contacts
        syncContacts();
        
        // Sync reminders
        syncReminders();
    }
    
    /**
     * Handle offline state
     */
    private void handleOffline() {
        if (isOnline) {
            isOnline = false;
            notifyListener(() -> {
                if (listener != null) listener.onOfflineMode();
            });
        }
        
        isSyncing = false;
    }
    
    /**
     * Sync pending messages to backend
     */
    private void syncPendingMessages() {
        java.util.List<JSONObject> pendingMessages = dbManager.getPendingMessages();
        
        for (JSONObject msg : pendingMessages) {
            try {
                int messageId = msg.getInt("id");
                String type = msg.getString("message_type");
                
                // Send based on type
                if ("whatsapp".equals(type)) {
                    sendWhatsAppMessage(msg, messageId);
                } else if ("sms".equals(type)) {
                    sendSMSMessage(msg, messageId);
                } else if ("email".equals(type)) {
                    sendEmailMessage(msg, messageId);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    
    /**
     * Send WhatsApp message via backend
     */
    private void sendWhatsAppMessage(JSONObject msg, final int messageId) {
        try {
            JSONObject payload = new JSONObject();
            payload.put("contact", msg.getString("contact_name"));
            payload.put("message", msg.getString("message_text"));
            
            apiClient.sendWhatsApp(payload, new ApiClient.ApiCallback() {
                @Override
                public void onSuccess(JSONObject response) {
                    dbManager.markMessageSent(messageId);
                }
                
                @Override
                public void onError(String error) {
                    // Retry later
                }
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Send SMS message via backend
     */
    private void sendSMSMessage(JSONObject msg, final int messageId) {
        try {
            JSONObject payload = new JSONObject();
            payload.put("phone", msg.getString("contact_number"));
            payload.put("message", msg.getString("message_text"));
            
            apiClient.sendSMS(payload, new ApiClient.ApiCallback() {
                @Override
                public void onSuccess(JSONObject response) {
                    dbManager.markMessageSent(messageId);
                }
                
                @Override
                public void onError(String error) {
                    // Retry later
                }
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Send email via backend
     */
    private void sendEmailMessage(JSONObject msg, final int messageId) {
        try {
            JSONObject payload = new JSONObject();
            payload.put("to", msg.getString("contact_number"));
            payload.put("message", msg.getString("message_text"));
            
            apiClient.sendEmail(payload, new ApiClient.ApiCallback() {
                @Override
                public void onSuccess(JSONObject response) {
                    dbManager.markMessageSent(messageId);
                }
                
                @Override
                public void onError(String error) {
                    // Retry later
                }
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Sync conversation history with backend
     */
    private void syncConversationHistory() {
        try {
            JSONArray history = dbManager.getUnsyncedChanges();
            
            if (history.length() > 0) {
                JSONObject payload = new JSONObject();
                payload.put("changes", history);
                
                apiClient.syncData(payload, new ApiClient.ApiCallback() {
                    @Override
                    public void onSuccess(JSONObject response) {
                        markAllSynced();
                    }
                    
                    @Override
                    public void onError(String error) {
                        // Retry later
                    }
                });
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Sync contacts with backend
     */
    private void syncContacts() {
        try {
            java.util.List<JSONObject> contacts = dbManager.getAllContacts();
            
            if (contacts.size() > 0) {
                JSONObject payload = new JSONObject();
                payload.put("contacts", new JSONArray(contacts));
                
                apiClient.syncContacts(payload, new ApiClient.ApiCallback() {
                    @Override
                    public void onSuccess(JSONObject response) {
                        // Contacts synced
                    }
                    
                    @Override
                    public void onError(String error) {
                        // Retry later
                    }
                });
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Sync reminders with backend
     */
    private void syncReminders() {
        try {
            java.util.List<JSONObject> reminders = dbManager.getActiveReminders();
            
            for (JSONObject reminder : reminders) {
                JSONObject payload = new JSONObject();
                payload.put("reminder", reminder.getString("text"));
                payload.put("time", reminder.getLong("time"));
                
                apiClient.setReminder(payload, new ApiClient.ApiCallback() {
                    @Override
                    public void onSuccess(JSONObject response) {
                        // Reminder synced
                    }
                    
                    @Override
                    public void onError(String error) {
                        // Retry later
                    }
                });
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Mark all changes as synced
     */
    private void markAllSynced() {
        try {
            JSONArray changes = dbManager.getUnsyncedChanges();
            
            for (int i = 0; i < changes.length(); i++) {
                JSONObject change = changes.getJSONObject(i);
                dbManager.markSynced(change.getInt("id"));
            }
            
            notifyListener(() -> {
                if (listener != null) listener.onSyncComplete(changes.length());
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        isSyncing = false;
    }
    
    /**
     * Get sync status
     */
    public JSONObject getSyncStatus() {
        try {
            JSONObject status = new JSONObject();
            status.put("is_online", isOnline);
            status.put("is_syncing", isSyncing);
            status.put("last_sync", prefs.getLong("last_sync_time", 0));
            status.put("db_stats", dbManager.getDatabaseStats());
            
            return status;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
    
    /**
     * Notify listener on main thread
     */
    private void notifyListener(Runnable runnable) {
        if (listener != null) {
            handler.post(runnable);
        }
    }
    
    /**
     * Set sync listener
     */
    public void setSyncListener(SyncListener listener) {
        this.listener = listener;
    }
    
    /**
     * Clean up resources
     */
    public void cleanup() {
        stopAutoSync();
        if (dbManager != null) {
            dbManager.close();
        }
    }
}
