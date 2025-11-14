package com.voiceassistant.app

import android.content.Context
import android.content.Intent
import android.os.Build

object ServiceManager {
    fun startService(context: Context) {
        val intent = Intent(context, VoiceAssistantService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            context.startForegroundService(intent)
        } else {
            context.startService(intent)
        }
    }

    fun stopService(context: Context) {
        val intent = Intent(context, VoiceAssistantService::class.java)
        context.stopService(intent)
    }

    fun isServiceRunning(context: Context): Boolean {
        val manager = context.getSystemService(Context.ACTIVITY_SERVICE) as android.app.ActivityManager
        for (service in manager.getRunningServices(Integer.MAX_VALUE)) {
            if (VoiceAssistantService::class.java.name == service.service.className) {
                return true
            }
        }
        return false
    }
}
