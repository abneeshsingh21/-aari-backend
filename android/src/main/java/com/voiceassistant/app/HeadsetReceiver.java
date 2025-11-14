package com.voiceassistant.app;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class HeadsetReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (Intent.ACTION_HEADSET_PLUG.equals(intent.getAction())) {
            int state = intent.getIntExtra("state", -1);
            if (state == 1) {
                // Headset connected - can start voice recognition
                Intent voiceIntent = new Intent(context, VoiceRecognitionService.class);
                context.startService(voiceIntent);
            }
        }
    }
}
