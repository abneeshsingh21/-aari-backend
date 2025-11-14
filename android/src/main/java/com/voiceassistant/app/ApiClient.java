package com.voiceassistant.app;

import android.content.Context;
import android.content.SharedPreferences;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONException;
import org.json.JSONObject;
import java.util.HashMap;
import java.util.Map;

/**
 * API Client for communicating with AARI backend server
 * Hybrid mode: Uses local PC when available, falls back to cloud
 * 
 * FREE CLOUD OPTIONS:
 * 1. Render.com - Completely free, no credit card
 *    https://render.com
 *    Example: https://aari-backend.onrender.com/api
 * 
 * 2. Railway.app - $5 free credit monthly
 *    https://railway.app
 *    Example: https://aari-backend.railway.app/api
 * 
 * 3. Replit - Free with limitations
 *    https://replit.com
 * 
 * SETUP:
 * 1. Deploy to free cloud using: DEPLOY_FREE.bat
 * 2. Get your cloud URL
 * 3. Update CLOUD_BACKEND below with your URL
 * 4. Rebuild Android APK
 */
public class ApiClient {

    // LOCAL: Works on home WiFi (fast, PC must be on)
    private static final String LOCAL_BACKEND = "http://192.168.1.100:5000/api"; // <-- CHANGE IP TO YOUR PC
    // CLOUD: Works anywhere 24/7 (set after deploying to free cloud)
    private static final String CLOUD_BACKEND = "https://aari-backend-2.onrender.com/api"; // <-- UPDATE WITH YOUR CLOUD URL
    
    // Current backend being used
    private static String currentBaseUrl = CLOUD_BACKEND;
    private static boolean preferLocal = false;
    
    private static RequestQueue requestQueue;
    private static ApiClient instance;
    private Context context;
    private SharedPreferences prefs;

    private ApiClient(Context context) {
        this.context = context.getApplicationContext();
        this.prefs = context.getSharedPreferences("aari_prefs", Context.MODE_PRIVATE);
        requestQueue = Volley.newRequestQueue(this.context);
        
        // Load saved backend preference
        String savedBackend = prefs.getString("current_backend", "cloud");
        if ("local".equals(savedBackend)) {
            currentBaseUrl = LOCAL_BACKEND;
            preferLocal = true;
        } else {
            currentBaseUrl = CLOUD_BACKEND;
            preferLocal = false;
        }
    }

    public static synchronized ApiClient getInstance(Context context) {
        if (instance == null) {
            instance = new ApiClient(context);
        }
        return instance;
    }
    
    /**
     * Switch between local and cloud backend
     */
    public void setBackend(String backendType) {
        if ("local".equals(backendType)) {
            currentBaseUrl = LOCAL_BACKEND;
            preferLocal = true;
            prefs.edit().putString("current_backend", "local").apply();
        } else {
            currentBaseUrl = CLOUD_BACKEND;
            preferLocal = false;
            prefs.edit().putString("current_backend", "cloud").apply();
        }
    }
    
    /**
     * Get current backend URL
     */
    public String getCurrentBackendUrl() {
        return currentBaseUrl;
    }
    
    /**
     * Check which backend is available and use it
     * Tries local first if preferred, then falls back to cloud
     */
    private void makeSmartRequest(String endpoint, JSONObject body, 
                                   ApiCallback callback, int method) {
        if (preferLocal) {
            // Try local first
            makeRequest(LOCAL_BACKEND + endpoint, body, new ApiCallback() {
                @Override
                public void onSuccess(JSONObject response) {
                    currentBaseUrl = LOCAL_BACKEND;
                    callback.onSuccess(response);
                }
                
                @Override
                public void onError(String error) {
                    // Local failed, try cloud
                    makeRequest(CLOUD_BACKEND + endpoint, body, new ApiCallback() {
                        @Override
                        public void onSuccess(JSONObject response) {
                            currentBaseUrl = CLOUD_BACKEND;
                            callback.onSuccess(response);
                        }
                        
                        @Override
                        public void onError(String error2) {
                            callback.onError("Both local and cloud backends unreachable");
                        }
                    }, method);
                }
            }, method);
        } else {
            // Use cloud directly
            makeRequest(CLOUD_BACKEND + endpoint, body, callback, method);
        }
    }

    /**
     * Process voice command on backend
     */
    public void processCommand(String command, ApiCallback callback) {
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("command", command);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        makeSmartRequest("/process-command", jsonBody, callback, Request.Method.POST);
    }

    /**
     * Check for available updates
     */
    public void checkUpdates(ApiCallback callback) {
        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                BASE_URL + "/check-updates",
                null,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    /**
     * Install specific features
     */
    public void installUpdates(String[] features, ApiCallback callback) {
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("features", features);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.POST,
                BASE_URL + "/install-updates",
                jsonBody,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback)) {
            @Override
            public Map<String, String> getHeaders() {
                Map<String, String> headers = new HashMap<>();
                headers.put("Content-Type", "application/json");
                return headers;
            }
        };

        requestQueue.add(request);
    }

    /**
     * Get update status history
     */
    public void getUpdateStatus(ApiCallback callback) {
        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                BASE_URL + "/update-status",
                null,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    /**
     * Get learning metrics and statistics
     */
    public void getLearningStatus(ApiCallback callback) {
        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                BASE_URL + "/learning-status",
                null,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    /**
     * Perform web search
     */
    public void webSearch(String query, ApiCallback callback) {
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("query", query);
            jsonBody.put("num_results", 5);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.POST,
                BASE_URL + "/web-search",
                jsonBody,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    /**
     * Extract content from webpage
     */
    public void getPageContent(String url, ApiCallback callback) {
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("url", url);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.POST,
                BASE_URL + "/get-page-content",
                jsonBody,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    /**
     * Send SMS via assistant
     */
    public void sendSMS(String phoneNumber, String message, ApiCallback callback) {
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("phone_number", phoneNumber);
            jsonBody.put("message", message);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.POST,
                BASE_URL + "/send-sms",
                jsonBody,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    /**
     * Make phone call
     */
    public void makeCall(String phoneNumber, ApiCallback callback) {
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("phone_number", phoneNumber);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.POST,
                BASE_URL + "/make-call",
                jsonBody,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    /**
     * Get health/status of backend
     */
    public void getHealth(ApiCallback callback) {
        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                BASE_URL + "/health",
                null,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    private void handleResponse(JSONObject response, ApiCallback callback) {
        if (callback != null) {
            callback.onSuccess(response);
        }
    }

    private void handleError(VolleyError error, ApiCallback callback) {
        if (callback != null) {
            callback.onError(error.getMessage());
        }
    }
    
    /**
     * Generic request maker for smart backend routing
     */
    private void makeRequest(String fullUrl, JSONObject body, ApiCallback callback, int method) {
        JsonObjectRequest request = new JsonObjectRequest(
                method,
                fullUrl,
                body,
                response -> handleResponse(response, callback),
                error -> handleError(error, callback));

        requestQueue.add(request);
    }

    /**
     * Callback interface for API responses
     */
    public interface ApiCallback {
        void onSuccess(JSONObject response);

        void onError(String error);
    }
}
