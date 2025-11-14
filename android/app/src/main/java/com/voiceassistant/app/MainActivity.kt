package com.voiceassistant.app

import android.Manifest
import android.app.AlertDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.floatingactionbutton.FloatingActionButton

class MainActivity : AppCompatActivity() {

    private val PERMISSION_REQUEST_CODE = 200
    private var statusTextView: TextView? = null
    private var startButton: Button? = null
    private var stopButton: Button? = null
    private var voiceButton: FloatingActionButton? = null
    private lateinit var conversationAdapter: ConversationAdapter
    private var conversationRecyclerView: RecyclerView? = null
    private val TAG = "MainActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(TAG, "MainActivity.onCreate called")
        try {
            setContentView(R.layout.activity_main)

            // Initialize views
            statusTextView = findViewById(R.id.statusTextView)
            startButton = findViewById(R.id.startButton)
            stopButton = findViewById(R.id.stopButton)
            voiceButton = findViewById(R.id.voiceButton)
            conversationRecyclerView = findViewById(R.id.conversationRecyclerView)

            // Setup RecyclerView
            conversationAdapter = ConversationAdapter(mutableListOf())
            conversationRecyclerView?.apply {
                layoutManager = LinearLayoutManager(this@MainActivity)
                adapter = conversationAdapter
            }

            // Check permissions
            checkAndRequestPermissions()

            // Set up button listeners
            startButton?.setOnClickListener { startVoiceAssistantService() }
            stopButton?.setOnClickListener { stopVoiceAssistantService() }
            voiceButton?.setOnClickListener { triggerVoiceInput() }

            // Quick command buttons
            findViewById<Button>(R.id.commandSendMessage)?.setOnClickListener { showSendMessageDialog() }
            findViewById<Button>(R.id.commandMakeCall)?.setOnClickListener { showMakeCallDialog() }
            findViewById<Button>(R.id.commandPlayMedia)?.setOnClickListener { showPlayMediaDialog() }
            findViewById<Button>(R.id.commandSearch)?.setOnClickListener { showSearchDialog() }
            findViewById<Button>(R.id.commandReminder)?.setOnClickListener { showReminderDialog() }
            findViewById<Button>(R.id.commandEmail)?.setOnClickListener { showEmailDialog() }

            // Menu and Settings
            findViewById<ImageView>(R.id.menuIcon)?.setOnClickListener { showMenu() }
            findViewById<ImageView>(R.id.settingsIcon)?.setOnClickListener { showSettings() }

            // Start service automatically
            try {
                startVoiceAssistantService()
            } catch (e: Exception) {
                Log.e(TAG, "Error starting service on onCreate", e)
                updateStatus("⚠️ Service startup error: ${e.message}")
            }
        } catch (e: Exception) {
            Log.e(TAG, "Fatal error in onCreate", e)
            Toast.makeText(this, "Critical Error: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }

    private fun checkAndRequestPermissions() {
        val permissions = arrayOf(
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.INTERNET,
            Manifest.permission.SEND_SMS,
            Manifest.permission.CALL_PHONE,
            Manifest.permission.READ_CONTACTS,
            Manifest.permission.WRITE_CONTACTS,
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.MODIFY_AUDIO_SETTINGS,
            Manifest.permission.WAKE_LOCK,
            Manifest.permission.ACCESS_NETWORK_STATE,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
        )

        val permissionsToRequest = mutableListOf<String>()

        for (permission in permissions) {
            if (ContextCompat.checkSelfPermission(this, permission)
                != PackageManager.PERMISSION_GRANTED
            ) {
                permissionsToRequest.add(permission)
            }
        }

        if (permissionsToRequest.isNotEmpty()) {
            ActivityCompat.requestPermissions(
                this,
                permissionsToRequest.toTypedArray(),
                PERMISSION_REQUEST_CODE
            )
        } else {
            updateStatus("All permissions granted ✓")
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == PERMISSION_REQUEST_CODE) {
            var allGranted = true
            for (result in grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allGranted = false
                    break
                }
            }
            if (allGranted) {
                updateStatus("All permissions granted ✓")
            } else {
                updateStatus("Some permissions denied - app may not work correctly")
            }
        }
    }

    private fun startVoiceAssistantService() {
        try {
            Log.d(TAG, "Starting VoiceAssistantService")
            ServiceManager.startService(this)
            updateStatus("🎤 Listening...")
            conversationAdapter.addMessage(Message("Voice Assistant started!", isUser = false))
            Toast.makeText(this, "Voice Assistant is running", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            Log.e(TAG, "Error starting service", e)
            updateStatus("❌ Failed to start service")
            Toast.makeText(this, "Error starting service: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    private fun stopVoiceAssistantService() {
        try {
            Log.d(TAG, "Stopping VoiceAssistantService")
            ServiceManager.stopService(this)
            updateStatus("⏹️ Stopped")
            Toast.makeText(this, "Voice Assistant stopped", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            Log.e(TAG, "Error stopping service", e)
            Toast.makeText(this, "Error stopping service: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    private fun triggerVoiceInput() {
        updateStatus("🎤 Listening... Speak now!")
        conversationAdapter.addMessage(Message("Voice input activated", isUser = true))
    }

    private fun showSendMessageDialog() {
        val contactInput = EditText(this).apply { hint = "Contact name" }
        val messageInput = EditText(this).apply { hint = "Message" }
        val container = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            addView(contactInput)
            addView(messageInput)
        }

        AlertDialog.Builder(this)
            .setTitle("Send Message")
            .setView(container)
            .setPositiveButton("Send") { _, _ ->
                val contact = contactInput.text.toString()
                val message = messageInput.text.toString()
                if (contact.isNotEmpty() && message.isNotEmpty()) {
                    sendCommand("send message to $contact saying $message")
                }
            }
            .show()
    }

    private fun showMakeCallDialog() {
        val input = EditText(this).apply { hint = "Contact name or number" }
        AlertDialog.Builder(this)
            .setTitle("Make Call")
            .setView(input)
            .setPositiveButton("Call") { _, _ ->
                val contact = input.text.toString()
                if (contact.isNotEmpty()) {
                    sendCommand("call $contact")
                }
            }
            .show()
    }

    private fun showPlayMediaDialog() {
        val input = EditText(this).apply { hint = "Song or artist name" }
        AlertDialog.Builder(this)
            .setTitle("Play Music")
            .setView(input)
            .setPositiveButton("Play") { _, _ ->
                val media = input.text.toString()
                if (media.isNotEmpty()) {
                    sendCommand("play $media")
                }
            }
            .show()
    }

    private fun showSearchDialog() {
        val input = EditText(this).apply { hint = "Search query" }
        AlertDialog.Builder(this)
            .setTitle("Search")
            .setView(input)
            .setPositiveButton("Search") { _, _ ->
                val query = input.text.toString()
                if (query.isNotEmpty()) {
                    sendCommand("search for $query")
                }
            }
            .show()
    }

    private fun showReminderDialog() {
        val input = EditText(this).apply { hint = "Reminder (e.g., buy groceries tomorrow)" }
        AlertDialog.Builder(this)
            .setTitle("Set Reminder")
            .setView(input)
            .setPositiveButton("Set") { _, _ ->
                val reminder = input.text.toString()
                if (reminder.isNotEmpty()) {
                    sendCommand("remind me to $reminder")
                }
            }
            .show()
    }

    private fun showEmailDialog() {
        val input = EditText(this).apply { hint = "Recipient email" }
        AlertDialog.Builder(this)
            .setTitle("Send Email")
            .setView(input)
            .setPositiveButton("Next") { _, _ ->
                val recipient = input.text.toString()
                if (recipient.isNotEmpty()) {
                    sendCommand("send email to $recipient")
                }
            }
            .show()
    }

    private fun showMenu() {
        AlertDialog.Builder(this)
            .setTitle("Menu")
            .setItems(arrayOf("Conversation History", "Clear Chat", "About")) { _, which ->
                when (which) {
                    0 -> Toast.makeText(this, "Conversation history", Toast.LENGTH_SHORT).show()
                    1 -> conversationAdapter = ConversationAdapter(mutableListOf())
                    2 -> showAbout()
                }
            }
            .show()
    }

    private fun showSettings() {
        Toast.makeText(this, "Settings coming soon", Toast.LENGTH_SHORT).show()
    }

    private fun showAbout() {
        AlertDialog.Builder(this)
            .setTitle("About AARI")
            .setMessage("AARI Voice Assistant\nVersion 2.0\n\nYour intelligent voice assistant powered by AI")
            .setPositiveButton("OK") { dialog, _ -> dialog.dismiss() }
            .show()
    }

    private fun sendCommand(command: String) {
        try {
            Log.d(TAG, "Sending command: $command")
            conversationAdapter.addMessage(Message(command, isUser = true))
            updateStatus("Processing: $command")
            
            // Send to backend
            val api = BackendAPI(this)
            api.processCommand(
                command,
                onSuccess = { response ->
                    conversationAdapter.addMessage(Message(response, isUser = false))
                    updateStatus("✓ Done")
                    Toast.makeText(this, "Command executed", Toast.LENGTH_SHORT).show()
                },
                onError = { error ->
                    updateStatus("❌ Error: $error")
                }
            )
        } catch (e: Exception) {
            Log.e(TAG, "Error sending command", e)
        }
    }

    private fun updateStatus(status: String) {
        statusTextView?.text = status
    }

    override fun onDestroy() {
        super.onDestroy()
    }
}

    private fun checkAndRequestPermissions() {
        val permissions = arrayOf(
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.INTERNET,
            Manifest.permission.SEND_SMS,
            Manifest.permission.CALL_PHONE,
            Manifest.permission.READ_CONTACTS,
            Manifest.permission.WRITE_CONTACTS,
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.MODIFY_AUDIO_SETTINGS,
            Manifest.permission.WAKE_LOCK,
            Manifest.permission.ACCESS_NETWORK_STATE,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
        )

        val permissionsToRequest = mutableListOf<String>()

        for (permission in permissions) {
            if (ContextCompat.checkSelfPermission(this, permission)
                != PackageManager.PERMISSION_GRANTED
            ) {
                permissionsToRequest.add(permission)
            }
        }

        if (permissionsToRequest.isNotEmpty()) {
            ActivityCompat.requestPermissions(
                this,
                permissionsToRequest.toTypedArray(),
                PERMISSION_REQUEST_CODE
            )
        } else {
            updateStatus("All permissions granted ✓")
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == PERMISSION_REQUEST_CODE) {
            var allGranted = true
            for (result in grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allGranted = false
                    break
                }
            }
            if (allGranted) {
                updateStatus("All permissions granted ✓")
            } else {
                updateStatus("Some permissions denied - app may not work correctly")
            }
        }
    }

    private fun startVoiceAssistantService() {
        try {
            Log.d(TAG, "Starting VoiceAssistantService")
            ServiceManager.startService(this)
            updateStatus("🎤 Voice Assistant Started (listening...)")
            Toast.makeText(this, "Voice Assistant is running in background", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            Log.e(TAG, "Error starting service", e)
            updateStatus("❌ Failed to start service")
            Toast.makeText(this, "Error starting service: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    private fun stopVoiceAssistantService() {
        try {
            Log.d(TAG, "Stopping VoiceAssistantService")
            ServiceManager.stopService(this)
            updateStatus("⏹️ Voice Assistant Stopped")
            Toast.makeText(this, "Voice Assistant stopped", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            Log.e(TAG, "Error stopping service", e)
            Toast.makeText(this, "Error stopping service: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    private fun updateStatus(status: String) {
        statusTextView?.text = status
    }

    override fun onDestroy() {
        super.onDestroy()
        // Keep service running even if app is closed
    }
}
