package com.voiceassistant.app;

import android.content.Context;
import android.content.SharedPreferences;
import org.json.JSONException;
import org.json.JSONObject;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Learning System for AARI
 * Tracks interactions, success rates, and patterns
 */
public class LearningSystem {

    private static final String PREFS_NAME = "aari_learning";
    private static final String KEY_TOTAL_INTERACTIONS = "total_interactions";
    private static final String KEY_SUCCESS_COUNT = "success_count";
    private static final String KEY_PATTERNS = "patterns";
    private static final String KEY_LAST_INTERACTION = "last_interaction";

    private SharedPreferences prefs;
    private Context context;

    public LearningSystem(Context context) {
        this.context = context;
        this.prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
    }

    /**
     * Log an interaction result
     */
    public void logInteraction(String command, String response, boolean success) {
        int totalInteractions = getTotalInteractions();
        int successCount = getSuccessCount();

        totalInteractions++;
        if (success) {
            successCount++;
        }

        SharedPreferences.Editor editor = prefs.edit();
        editor.putInt(KEY_TOTAL_INTERACTIONS, totalInteractions);
        editor.putInt(KEY_SUCCESS_COUNT, successCount);
        editor.putString(KEY_LAST_INTERACTION, getCurrentTimestamp());
        editor.apply();

        // Store pattern
        storePattern(command, response, success);
    }

    /**
     * Store interaction pattern
     */
    private void storePattern(String command, String response, boolean success) {
        try {
            JSONObject pattern = new JSONObject();
            pattern.put("command", command);
            pattern.put("response", response);
            pattern.put("success", success);
            pattern.put("timestamp", getCurrentTimestamp());

            // In real implementation, save to file or database
            // For now, just log
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    /**
     * Get success rate percentage
     */
    public double getSuccessRate() {
        int total = getTotalInteractions();
        if (total == 0)
            return 0.0;
        return (double) getSuccessCount() / total * 100;
    }

    /**
     * Get total interactions
     */
    public int getTotalInteractions() {
        return prefs.getInt(KEY_TOTAL_INTERACTIONS, 0);
    }

    /**
     * Get success count
     */
    public int getSuccessCount() {
        return prefs.getInt(KEY_SUCCESS_COUNT, 0);
    }

    /**
     * Get learning status as JSON
     */
    public JSONObject getStatus() {
        try {
            JSONObject status = new JSONObject();
            status.put("total_interactions", getTotalInteractions());
            status.put("success_count", getSuccessCount());
            status.put("success_rate", String.format("%.2f%%", getSuccessRate()));
            status.put("last_interaction", prefs.getString(KEY_LAST_INTERACTION, "Never"));
            return status;
        } catch (JSONException e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Clear learning data
     */
    public void clearData() {
        SharedPreferences.Editor editor = prefs.edit();
        editor.clear();
        editor.apply();
    }

    private String getCurrentTimestamp() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
        return sdf.format(new Date());
    }
}
