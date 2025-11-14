package com.voiceassistant.app

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import android.os.Build

class HeadsetReceiver : BroadcastReceiver() {

    companion object {
        private const val TAG = "HeadsetReceiver"
    }

    override fun onReceive(context: Context?, intent: Intent?) {
        if (intent?.action == Intent.ACTION_MEDIA_BUTTON) {
            Log.d(TAG, "Headset button pressed - activating voice assistant")

            // Start voice assistant service
            val serviceIntent = Intent(context, VoiceAssistantService::class.java)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && context != null) {
                context.startForegroundService(serviceIntent)
            } else {
                context?.startService(serviceIntent)
            }

            // Abort broadcast so other apps don't receive it
            abortBroadcast()
        }

        // Handle screen unlock to keep service active
        if (intent?.action == Intent.ACTION_USER_PRESENT) {
            Log.d(TAG, "Screen unlocked - voice assistant active")
            val serviceIntent = Intent(context, VoiceAssistantService::class.java)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && context != null) {
                context.startForegroundService(serviceIntent)
            } else {
                context?.startService(serviceIntent)
            }
        }
    }
}
