package com.voiceassistant.app;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.util.Log;

/**
 * Boot Receiver - Starts AARI automatically on device boot
 * Auto-starts AARI service even if app is not opened
 */
public class BootReceiver extends BroadcastReceiver {

    private static final String TAG = "BootReceiver";

    @Override
    public void onReceive(Context context, Intent intent) {
        if (Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())) {
            Log.i(TAG, "Device booted - starting AARI Voice Assistant");

            // Start VoiceAssistantService on boot (always, for background listening)
            Intent serviceIntent = new Intent(context, VoiceAssistantService.class);

            // Start as foreground service for continuous operation
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                context.startForegroundService(serviceIntent);
                Log.i(TAG, "Started as foreground service");
            } else {
                context.startService(serviceIntent);
                Log.i(TAG, "Started as regular service");
            }

            // Log successful start
            SharedPreferences prefs = context.getSharedPreferences("aari_prefs", Context.MODE_PRIVATE);
            prefs.edit().putBoolean("service_started_on_boot", true)
                    .putLong("boot_start_time", System.currentTimeMillis())
                    .apply();
        }
    }
}
