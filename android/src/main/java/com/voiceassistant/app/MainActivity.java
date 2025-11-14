package com.voiceassistant.app;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.LinearLayout;
import android.view.View;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends AppCompatActivity {

    private static final int PERMISSION_REQUEST_CODE = 100;
    private VoiceAssistantService voiceAssistantService;
    private ImageButton micButton;
    private TextView statusText;
    private AdvancedFeaturesHandler advancedFeatures;
    private LearningSystem learningSystem;
    private ApiClient apiClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        micButton = findViewById(R.id.mic_button);
        statusText = findViewById(R.id.status_text);

        // Initialize handlers
        advancedFeatures = new AdvancedFeaturesHandler(this);
        learningSystem = new LearningSystem(this);
        apiClient = ApiClient.getInstance(this);

        // Request necessary permissions
        requestPermissions();

        // Start voice assistant service
        startVoiceAssistantService();

        // Set up mic button listener
        micButton.setOnClickListener(v -> toggleVoiceRecognition());

        // Setup advanced feature buttons
        setupAdvancedFeatures();

        // Check backend health
        checkBackendStatus();
    }

    /**
     * Setup advanced feature buttons in UI
     */
    private void setupAdvancedFeatures() {
        // Web Search Button
        ImageButton webSearchBtn = findViewById(R.id.web_search_btn);
        if (webSearchBtn != null) {
            webSearchBtn.setOnClickListener(v -> openWebSearchDialog());
        }

        // Updates Button
        ImageButton updatesBtn = findViewById(R.id.updates_btn);
        if (updatesBtn != null) {
            updatesBtn.setOnClickListener(v -> checkUpdates());
        }

        // Learning Status Button
        ImageButton learningBtn = findViewById(R.id.learning_btn);
        if (learningBtn != null) {
            learningBtn.setOnClickListener(v -> showLearningStatus());
        }

        // Settings Button
        ImageButton settingsBtn = findViewById(R.id.settings_btn);
        if (settingsBtn != null) {
            settingsBtn.setOnClickListener(v -> openSettings());
        }
    }

    /**
     * Open web search dialog
     */
    private void openWebSearchDialog() {
        // Create a simple search input dialog
        android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(this);
        builder.setTitle("Web Search");

        final android.widget.EditText input = new android.widget.EditText(this);
        input.setHint("Enter search query");
        builder.setView(input);

        builder.setPositiveButton("Search", (dialog, which) -> {
            String query = input.getText().toString();
            if (!query.isEmpty()) {
                advancedFeatures.webSearch(query, new AdvancedFeaturesHandler.ApiCallback() {
                    @Override
                    public void onSuccess(org.json.JSONObject response) {
                        showSearchResults(response);
                    }

                    @Override
                    public void onError(String error) {
                        statusText.setText("Search failed: " + error);
                    }
                });
            }
        });

        builder.setNegativeButton("Cancel", (dialog, which) -> dialog.cancel());
        builder.show();
    }

    /**
     * Show search results
     */
    private void showSearchResults(org.json.JSONObject results) {
        try {
            String resultText = results.toString(2);
            android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(this);
            builder.setTitle("Search Results");

            android.widget.TextView textView = new android.widget.TextView(this);
            textView.setText(resultText);
            textView.setPadding(10, 10, 10, 10);
            builder.setView(textView);
            builder.setPositiveButton("OK", null);
            builder.show();
        } catch (Exception e) {
            statusText.setText("Error displaying results");
        }
    }

    /**
     * Check for available updates
     */
    private void checkUpdates() {
        statusText.setText("Checking for updates...");
        advancedFeatures.checkUpdates(new AdvancedFeaturesHandler.ApiCallback() {
            @Override
            public void onSuccess(org.json.JSONObject response) {
                try {
                    android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(MainActivity.this);
                    builder.setTitle("Available Updates");
                    builder.setMessage(response.toString(2));
                    builder.setPositiveButton("Install", (dialog, which) -> installUpdates());
                    builder.setNegativeButton("Later", null);
                    builder.show();
                    statusText.setText("Updates available");
                } catch (Exception e) {
                    statusText.setText("Error: " + e.getMessage());
                }
            }

            @Override
            public void onError(String error) {
                statusText.setText("Update check failed: " + error);
            }
        });
    }

    /**
     * Install available updates
     */
    private void installUpdates() {
        statusText.setText("Installing updates...");
        String[] features = { "web_search", "web_automation", "sentiment_analysis" };
        apiClient.installUpdates(features, new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(org.json.JSONObject response) {
                statusText.setText("Updates installed successfully");
            }

            @Override
            public void onError(String error) {
                statusText.setText("Installation failed: " + error);
            }
        });
    }

    /**
     * Show learning statistics
     */
    private void showLearningStatus() {
        try {
            org.json.JSONObject status = learningSystem.getStatus();
            android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(this);
            builder.setTitle("Learning Statistics");

            String message = "Total Interactions: " + status.getInt("total_interactions") + "\n" +
                    "Successful: " + status.getInt("success_count") + "\n" +
                    "Success Rate: " + status.getString("success_rate") + "\n" +
                    "Last Interaction: " + status.getString("last_interaction");

            builder.setMessage(message);
            builder.setPositiveButton("OK", null);
            builder.show();

            statusText.setText("Statistics: " + status.getString("success_rate"));
        } catch (Exception e) {
            statusText.setText("Error: " + e.getMessage());
        }
    }

    /**
     * Open settings screen with background mode control
     */
    private void openSettings() {
        android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(this);
        builder.setTitle("AARI Settings");

        android.widget.LinearLayout layout = new android.widget.LinearLayout(this);
        layout.setOrientation(android.widget.LinearLayout.VERTICAL);
        layout.setPadding(20, 20, 20, 20);

        // Background Mode Switch
        android.widget.Switch backgroundSwitch = new android.widget.Switch(this);
        backgroundSwitch.setText("Background Mode (Always Listening)");

        android.content.SharedPreferences prefs = getSharedPreferences("aari_prefs", MODE_PRIVATE);
        backgroundSwitch.setChecked(prefs.getBoolean("background_mode_enabled", false));

        backgroundSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> {
            prefs.edit().putBoolean("background_mode_enabled", isChecked).apply();

            if (isChecked) {
                statusText.setText("Background mode enabled - AARI will listen continuously");
                startBackgroundMode();
            } else {
                statusText.setText("Background mode disabled");
            }
        });

        layout.addView(backgroundSwitch);

        // Divider
        android.widget.View divider = new android.widget.View(this);
        divider.setLayoutParams(new android.widget.LinearLayout.LayoutParams(
                android.widget.LinearLayout.LayoutParams.MATCH_PARENT, 2));
        divider.setBackgroundColor(android.graphics.Color.GRAY);
        layout.addView(divider);

        // Wake Word Setting
        android.widget.LinearLayout wakeWordLayout = new android.widget.LinearLayout(this);
        wakeWordLayout.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        wakeWordLayout.setPadding(0, 20, 0, 0);

        android.widget.TextView wakeWordLabel = new android.widget.TextView(this);
        wakeWordLabel.setText("Wake Word: ");
        wakeWordLabel.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,
                android.widget.LinearLayout.LayoutParams.WRAP_CONTENT, 0.4f));

        android.widget.EditText wakeWordInput = new android.widget.EditText(this);
        wakeWordInput.setText(prefs.getString("wake_word", "hey aari"));
        wakeWordInput.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,
                android.widget.LinearLayout.LayoutParams.WRAP_CONTENT, 0.6f));

        wakeWordLayout.addView(wakeWordLabel);
        wakeWordLayout.addView(wakeWordInput);
        layout.addView(wakeWordLayout);

        // Speech Speed Setting
        android.widget.LinearLayout speedLayout = new android.widget.LinearLayout(this);
        speedLayout.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        speedLayout.setPadding(0, 20, 0, 0);

        android.widget.TextView speedLabel = new android.widget.TextView(this);
        speedLabel.setText("Speech Speed: ");
        speedLabel.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,
                android.widget.LinearLayout.LayoutParams.WRAP_CONTENT, 0.4f));

        android.widget.SeekBar speedBar = new android.widget.SeekBar(this);
        speedBar.setMax(20); // 0.8 to 1.8x
        speedBar.setProgress(10); // Default 1.3x
        speedBar.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,
                android.widget.LinearLayout.LayoutParams.WRAP_CONTENT, 0.6f));

        speedLayout.addView(speedLabel);
        speedLayout.addView(speedBar);
        layout.addView(speedLayout);

        builder.setView(layout);
        builder.setPositiveButton("Save", (dialog, which) -> {
            String newWakeWord = wakeWordInput.getText().toString().toLowerCase();
            if (!newWakeWord.isEmpty()) {
                prefs.edit().putString("wake_word", newWakeWord).apply();
                float speed = 0.8f + (speedBar.getProgress() * 0.05f);
                prefs.edit().putFloat("speech_speed", speed).apply();
                statusText.setText(
                        "Settings saved! Wake word: " + newWakeWord + ", Speed: " + String.format("%.1fx", speed));
            }
        });

        builder.setNegativeButton("Cancel", null);
        builder.show();
    }

    /**
     * Start background listening mode
     */
    private void startBackgroundMode() {
        Intent serviceIntent = new Intent(this, VoiceAssistantService.class);
        startService(serviceIntent);
    }

    /**
     * Check backend API health
     */
    private void checkBackendStatus() {
        apiClient.getHealth(new ApiClient.ApiCallback() {
            @Override
            public void onSuccess(org.json.JSONObject response) {
                statusText.setText("Backend Connected ✓");
            }

            @Override
            public void onError(String error) {
                statusText.setText("Backend Offline - Local Mode Only");
            }
        });
    }

    private void requestPermissions() {
        String[] permissions = {
                Manifest.permission.RECORD_AUDIO,
                Manifest.permission.INTERNET,
                Manifest.permission.CALL_PHONE,
                Manifest.permission.SEND_SMS,
                Manifest.permission.READ_CONTACTS
        };

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            for (String permission : permissions) {
                if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(this, new String[] { permission },
                            PERMISSION_REQUEST_CODE);
                }
            }
        }
    }

    private void startVoiceAssistantService() {
        Intent serviceIntent = new Intent(this, VoiceAssistantService.class);
        startService(serviceIntent);
        statusText.setText("Voice Assistant Ready");
    }

    private void toggleVoiceRecognition() {
        Intent voiceIntent = new Intent(this, VoiceRecognitionService.class);
        startService(voiceIntent);
        statusText.setText("Listening...");
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions,
            int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {
            for (int result : grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    statusText.setText("Permissions denied. Some features won't work.");
                }
            }
        }
    }
}
