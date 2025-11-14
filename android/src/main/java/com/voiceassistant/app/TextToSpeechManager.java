package com.voiceassistant.app;

import android.content.Context;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import java.util.Locale;

/**
 * TextToSpeech Manager with Fast Speech Rate
 * Mimics Alexa/Google speed (1.2 - 1.5x faster than default)
 */
public class TextToSpeechManager implements TextToSpeech.OnInitListener {

    private static final String TAG = "TextToSpeech";
    private TextToSpeech tts;
    private Context context;
    private boolean isReady = false;
    private float speechRate = 1.3f; // Faster than normal (1.0)

    public TextToSpeechManager(Context context) {
        this.context = context;
        initTTS();
    }

    /**
     * Initialize TextToSpeech
     */
    private void initTTS() {
        tts = new TextToSpeech(context, this);
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            // Set language
            int result = tts.setLanguage(Locale.getDefault());

            if (result == TextToSpeech.LANG_MISSING_DATA ||
                    result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.e(TAG, "Language not supported");
            } else {
                // Set faster speech rate (1.3x normal speed like Alexa)
                tts.setSpeechRate(speechRate);
                // Set pitch slightly higher (sounds more energetic)
                tts.setPitch(1.1f);
                isReady = true;
                Log.i(TAG, "TTS initialized with speech rate: " + speechRate);
            }
        } else {
            Log.e(TAG, "TTS initialization failed");
        }
    }

    /**
     * Speak text quickly
     */
    public void speak(String text) {
        if (isReady && tts != null) {
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null);
        }
    }

    /**
     * Set custom speech rate (1.0 = normal, 1.5 = 1.5x faster)
     */
    public void setSpeechRate(float rate) {
        speechRate = rate;
        if (tts != null) {
            tts.setSpeechRate(rate);
        }
    }

    /**
     * Stop speaking
     */
    public void stop() {
        if (tts != null) {
            tts.stop();
        }
    }

    /**
     * Release resources
     */
    public void shutdown() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
    }

    public boolean isReady() {
        return isReady;
    }
}
