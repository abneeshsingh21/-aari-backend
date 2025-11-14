package com.voiceassistant.app

import android.content.Context
import android.content.SharedPreferences
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

class ConfigManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences(
        "aari_config",
        Context.MODE_PRIVATE
    )
    private val gson = Gson()

    companion object {
        const val BACKEND_URL = "https://aari-backend-2.onrender.com"
        const val WAKE_WORD = "aari"
        const val ASSISTANT_NAME = "aari"
        const val USER_NAME = "user"
    }

    fun getBackendUrl(): String = prefs.getString("backend_url", BACKEND_URL) ?: BACKEND_URL
    fun setBackendUrl(url: String) = prefs.edit().putString("backend_url", url).apply()

    fun getWakeWord(): String = prefs.getString("wake_word", WAKE_WORD) ?: WAKE_WORD
    fun setWakeWord(word: String) = prefs.edit().putString("wake_word", word).apply()

    fun isServiceEnabled(): Boolean = prefs.getBoolean("service_enabled", true)
    fun setServiceEnabled(enabled: Boolean) = prefs.edit().putBoolean("service_enabled", enabled).apply()

    fun isAutoStartEnabled(): Boolean = prefs.getBoolean("auto_start", true)
    fun setAutoStartEnabled(enabled: Boolean) = prefs.edit().putBoolean("auto_start", enabled).apply()

    fun getContacts(): Map<String, String> {
        val json = prefs.getString("contacts", "{}") ?: "{}"
        return gson.fromJson(json, object : TypeToken<Map<String, String>>() {}.type)
    }

    fun saveContacts(contacts: Map<String, String>) {
        prefs.edit().putString("contacts", gson.toJson(contacts)).apply()
    }

    fun getConversationHistory(): List<String> {
        val json = prefs.getString("conversation_history", "[]") ?: "[]"
        return gson.fromJson(json, object : TypeToken<List<String>>() {}.type)
    }

    fun addToConversationHistory(message: String) {
        val history = getConversationHistory().toMutableList()
        history.add(message)
        if (history.size > 100) {
            history.removeAt(0)
        }
        prefs.edit().putString("conversation_history", gson.toJson(history)).apply()
    }

    fun clearConversationHistory() {
        prefs.edit().putString("conversation_history", "[]").apply()
    }
}
