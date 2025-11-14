package com.voiceassistant.app

import android.content.Context
import android.util.Log
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import org.json.JSONObject

class BackendAPI(private val context: Context) {
    private val requestQueue: RequestQueue = Volley.newRequestQueue(context)
    private val config = ConfigManager(context)

    companion object {
        private const val TAG = "BackendAPI"
    }

    fun processCommand(command: String, onSuccess: (String) -> Unit, onError: (String) -> Unit) {
        val url = "${config.getBackendUrl()}/api/process-command"
        val jsonBody = JSONObject()
        jsonBody.put("command", command)

        Log.d(TAG, "Sending command: $command to $url")

        val request = JsonObjectRequest(
            Request.Method.POST, url, jsonBody,
            { response ->
                try {
                    val reply = response.optString("response", "Command executed")
                    Log.d(TAG, "Response: $reply")
                    onSuccess(reply)
                } catch (e: Exception) {
                    Log.e(TAG, "Error parsing response: ${e.message}")
                    onError("Error parsing response")
                }
            },
            { error ->
                Log.e(TAG, "API Error: ${error.message}")
                onError(error.message ?: "Unknown error")
            }
        )

        requestQueue.add(request)
    }

    fun sendMessage(contact: String, message: String, onSuccess: (String) -> Unit, onError: (String) -> Unit) {
        val url = "${config.getBackendUrl()}/api/send-message"
        val jsonBody = JSONObject()
        jsonBody.put("contact", contact)
        jsonBody.put("message", message)

        val request = JsonObjectRequest(
            Request.Method.POST, url, jsonBody,
            { response ->
                onSuccess(response.optString("response", "Message sent"))
            },
            { error ->
                onError(error.message ?: "Unknown error")
            }
        )

        requestQueue.add(request)
    }

    fun makeCall(contact: String, onSuccess: (String) -> Unit, onError: (String) -> Unit) {
        val url = "${config.getBackendUrl()}/api/make-call"
        val jsonBody = JSONObject()
        jsonBody.put("contact", contact)

        val request = JsonObjectRequest(
            Request.Method.POST, url, jsonBody,
            { response ->
                onSuccess(response.optString("response", "Call initiated"))
            },
            { error ->
                onError(error.message ?: "Unknown error")
            }
        )

        requestQueue.add(request)
    }

    fun getHealth(onSuccess: (String) -> Unit, onError: (String) -> Unit) {
        val url = "${config.getBackendUrl()}/api/health"

        val request = JsonObjectRequest(
            Request.Method.GET, url, null,
            { response ->
                onSuccess("Backend is healthy")
            },
            { error ->
                onError("Backend unavailable")
            }
        )

        requestQueue.add(request)
    }
}
