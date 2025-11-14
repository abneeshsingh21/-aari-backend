import android.content.Context;
import android.content.SharedPreferences;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.Cursor;
import android.content.ContentValues;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.List;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Local Database Manager for AARI
 * Handles offline data storage and sync with backend
 */
public class LocalDatabaseManager extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "aari_local.db";
    private static final int DATABASE_VERSION = 2;

    // Table names
    private static final String TABLE_MESSAGES = "messages";
    private static final String TABLE_COMMANDS = "commands";
    private static final String TABLE_RESPONSES = "responses";
    private static final String TABLE_CONTACTS = "contacts";
    private static final String TABLE_REMINDERS = "reminders";
    private static final String TABLE_SYNC_LOG = "sync_log";

    private SharedPreferences prefs;

    public LocalDatabaseManager(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        this.prefs = context.getSharedPreferences("aari_prefs", Context.MODE_PRIVATE);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // Messages table - for queued WhatsApp/SMS/Email
        db.execSQL("CREATE TABLE IF NOT EXISTS " + TABLE_MESSAGES + " (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "contact_name TEXT," +
                "contact_number TEXT," +
                "message_text TEXT," +
                "message_type TEXT," + // whatsapp, sms, email, call
                "status TEXT," + // pending, sent, failed
                "created_at TIMESTAMP," +
                "sent_at TIMESTAMP" +
                ");");

        // Commands table - for conversation history
        db.execSQL("CREATE TABLE IF NOT EXISTS " + TABLE_COMMANDS + " (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "user_command TEXT," +
                "command_type TEXT," +
                "intent TEXT," +
                "status TEXT," +
                "created_at TIMESTAMP" +
                ");");

        // Responses table - for cached responses
        db.execSQL("CREATE TABLE IF NOT EXISTS " + TABLE_RESPONSES + " (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "command_id INTEGER," +
                "response_text TEXT," +
                "response_audio BLOB," +
                "created_at TIMESTAMP" +
                ");");

        // Contacts table - local contact cache
        db.execSQL("CREATE TABLE IF NOT EXISTS " + TABLE_CONTACTS + " (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "contact_name TEXT UNIQUE," +
                "contact_number TEXT," +
                "contact_email TEXT," +
                "contact_type TEXT," + // personal, work, etc
                "last_updated TIMESTAMP" +
                ");");

        // Reminders table
        db.execSQL("CREATE TABLE IF NOT EXISTS " + TABLE_REMINDERS + " (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "reminder_text TEXT," +
                "reminder_time TIMESTAMP," +
                "is_triggered INTEGER DEFAULT 0," +
                "created_at TIMESTAMP" +
                ");");

        // Sync log - track what needs to be synced
        db.execSQL("CREATE TABLE IF NOT EXISTS " + TABLE_SYNC_LOG + " (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "table_name TEXT," +
                "record_id INTEGER," +
                "operation TEXT," + // insert, update, delete
                "synced INTEGER DEFAULT 0," +
                "created_at TIMESTAMP" +
                ");");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        if (oldVersion < 2) {
            db.execSQL("ALTER TABLE " + TABLE_COMMANDS + " ADD COLUMN intent TEXT");
        }
    }

    // ====================
    // MESSAGE OPERATIONS
    // ====================

    /**
     * Queue a message for sending when backend is available
     */
    public long queueMessage(String contactName, String contactNumber,
            String message, String type) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();

        values.put("contact_name", contactName);
        values.put("contact_number", contactNumber);
        values.put("message_text", message);
        values.put("message_type", type); // whatsapp, sms, email
        values.put("status", "pending");
        values.put("created_at", getCurrentTimestamp());

        long id = db.insert(TABLE_MESSAGES, null, values);

        // Log for sync
        logSync(TABLE_MESSAGES, (int) id, "insert");

        return id;
    }

    /**
     * Get all pending messages
     */
    public List<JSONObject> getPendingMessages() {
        SQLiteDatabase db = getReadableDatabase();
        List<JSONObject> messages = new ArrayList<>();

        Cursor cursor = db.query(TABLE_MESSAGES,
                null,
                "status = ?",
                new String[] { "pending" },
                null, null, "created_at ASC");

        while (cursor.moveToNext()) {
            try {
                JSONObject msg = new JSONObject();
                msg.put("id", cursor.getInt(0));
                msg.put("contact_name", cursor.getString(1));
                msg.put("contact_number", cursor.getString(2));
                msg.put("message_text", cursor.getString(3));
                msg.put("message_type", cursor.getString(4));
                messages.add(msg);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        cursor.close();

        return messages;
    }

    /**
     * Mark message as sent
     */
    public void markMessageSent(int messageId) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();

        values.put("status", "sent");
        values.put("sent_at", getCurrentTimestamp());

        db.update(TABLE_MESSAGES, values, "id = ?", new String[] { String.valueOf(messageId) });

        // Log for sync
        logSync(TABLE_MESSAGES, messageId, "update");
    }

    // ====================
    // COMMAND OPERATIONS
    // ====================

    /**
     * Save user command to history
     */
    public long saveCommand(String userCommand, String commandType, String intent) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();

        values.put("user_command", userCommand);
        values.put("command_type", commandType);
        values.put("intent", intent);
        values.put("status", "completed");
        values.put("created_at", getCurrentTimestamp());

        long id = db.insert(TABLE_COMMANDS, null, values);
        logSync(TABLE_COMMANDS, (int) id, "insert");

        return id;
    }

    /**
     * Get conversation history
     */
    public List<JSONObject> getConversationHistory(int limit) {
        SQLiteDatabase db = getReadableDatabase();
        List<JSONObject> history = new ArrayList<>();

        Cursor cursor = db.query(TABLE_COMMANDS,
                null, null, null, null, null,
                "created_at DESC", limit + "");

        while (cursor.moveToNext()) {
            try {
                JSONObject cmd = new JSONObject();
                cmd.put("id", cursor.getInt(0));
                cmd.put("command", cursor.getString(1));
                cmd.put("type", cursor.getString(2));
                cmd.put("timestamp", cursor.getString(5));
                history.add(cmd);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        cursor.close();

        return history;
    }

    // ====================
    // CONTACT OPERATIONS
    // ====================

    /**
     * Save contact locally
     */
    public long saveContact(String name, String number, String email, String type) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();

        values.put("contact_name", name);
        values.put("contact_number", number);
        values.put("contact_email", email);
        values.put("contact_type", type);
        values.put("last_updated", getCurrentTimestamp());

        long id = db.insertWithOnConflict(TABLE_CONTACTS, null, values,
                SQLiteDatabase.CONFLICT_REPLACE);
        logSync(TABLE_CONTACTS, (int) id, "insert");

        return id;
    }

    /**
     * Find contact by name (supports partial matching)
     */
    public JSONObject findContact(String name) {
        SQLiteDatabase db = getReadableDatabase();

        Cursor cursor = db.query(TABLE_CONTACTS,
                null,
                "contact_name LIKE ?",
                new String[] { "%" + name + "%" },
                null, null, null, "1");

        JSONObject contact = null;
        if (cursor.moveToNext()) {
            try {
                contact = new JSONObject();
                contact.put("name", cursor.getString(1));
                contact.put("number", cursor.getString(2));
                contact.put("email", cursor.getString(3));
                contact.put("type", cursor.getString(4));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        cursor.close();

        return contact;
    }

    /**
     * Get all contacts
     */
    public List<JSONObject> getAllContacts() {
        SQLiteDatabase db = getReadableDatabase();
        List<JSONObject> contacts = new ArrayList<>();

        Cursor cursor = db.query(TABLE_CONTACTS, null, null, null,
                null, null, "contact_name ASC");

        while (cursor.moveToNext()) {
            try {
                JSONObject contact = new JSONObject();
                contact.put("name", cursor.getString(1));
                contact.put("number", cursor.getString(2));
                contact.put("email", cursor.getString(3));
                contacts.add(contact);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        cursor.close();

        return contacts;
    }

    // ====================
    // REMINDER OPERATIONS
    // ====================

    /**
     * Save reminder
     */
    public long saveReminder(String reminderText, long reminderTime) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();

        values.put("reminder_text", reminderText);
        values.put("reminder_time", reminderTime);
        values.put("is_triggered", 0);
        values.put("created_at", getCurrentTimestamp());

        long id = db.insert(TABLE_REMINDERS, null, values);
        logSync(TABLE_REMINDERS, (int) id, "insert");

        return id;
    }

    /**
     * Get active reminders
     */
    public List<JSONObject> getActiveReminders() {
        SQLiteDatabase db = getReadableDatabase();
        List<JSONObject> reminders = new ArrayList<>();

        long currentTime = System.currentTimeMillis();

        Cursor cursor = db.query(TABLE_REMINDERS,
                null,
                "is_triggered = 0 AND reminder_time <= ?",
                new String[] { String.valueOf(currentTime) },
                null, null, "reminder_time ASC");

        while (cursor.moveToNext()) {
            try {
                JSONObject reminder = new JSONObject();
                reminder.put("id", cursor.getInt(0));
                reminder.put("text", cursor.getString(1));
                reminder.put("time", cursor.getLong(2));
                reminders.add(reminder);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        cursor.close();

        return reminders;
    }

    // ====================
    // SYNC OPERATIONS
    // ====================

    /**
     * Log changes for sync
     */
    private void logSync(String tableName, int recordId, String operation) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();

        values.put("table_name", tableName);
        values.put("record_id", recordId);
        values.put("operation", operation);
        values.put("synced", 0);
        values.put("created_at", getCurrentTimestamp());

        db.insert(TABLE_SYNC_LOG, null, values);
    }

    /**
     * Get all unsynced changes
     */
    public JSONArray getUnsyncedChanges() {
        SQLiteDatabase db = getReadableDatabase();
        JSONArray changes = new JSONArray();

        Cursor cursor = db.query(TABLE_SYNC_LOG,
                null,
                "synced = 0",
                null, null, null, "created_at ASC");

        while (cursor.moveToNext()) {
            try {
                JSONObject change = new JSONObject();
                change.put("id", cursor.getInt(0));
                change.put("table", cursor.getString(1));
                change.put("record_id", cursor.getInt(2));
                change.put("operation", cursor.getString(3));
                changes.put(change);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        cursor.close();

        return changes;
    }

    /**
     * Mark changes as synced
     */
    public void markSynced(int syncLogId) {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put("synced", 1);

        db.update(TABLE_SYNC_LOG, values, "id = ?",
                new String[] { String.valueOf(syncLogId) });
    }

    /**
     * Get database statistics
     */
    public JSONObject getDatabaseStats() {
        SQLiteDatabase db = getReadableDatabase();
        JSONObject stats = new JSONObject();

        try {
            stats.put("pending_messages", getCount(db, TABLE_MESSAGES, "status = 'pending'"));
            stats.put("total_commands", getCount(db, TABLE_COMMANDS, null));
            stats.put("total_contacts", getCount(db, TABLE_CONTACTS, null));
            stats.put("active_reminders", getCount(db, TABLE_REMINDERS, "is_triggered = 0"));
            stats.put("unsynced_changes", getCount(db, TABLE_SYNC_LOG, "synced = 0"));
        } catch (Exception e) {
            e.printStackTrace();
        }

        return stats;
    }

    /**
     * Clear old data (keep only last 30 days)
     */
    public void cleanOldData() {
        SQLiteDatabase db = getWritableDatabase();
        long thirtyDaysAgo = System.currentTimeMillis() - (30 * 24 * 60 * 60 * 1000);

        // Delete old commands
        db.delete(TABLE_COMMANDS, "created_at < ?",
                new String[] { String.valueOf(thirtyDaysAgo) });

        // Delete old synced changes
        db.delete(TABLE_SYNC_LOG, "synced = 1 AND created_at < ?",
                new String[] { String.valueOf(thirtyDaysAgo) });
    }

    // ====================
    // HELPER METHODS
    // ====================

    private int getCount(SQLiteDatabase db, String table, String where) {
        Cursor cursor;
        if (where != null) {
            cursor = db.rawQuery("SELECT COUNT(*) FROM " + table + " WHERE " + where, null);
        } else {
            cursor = db.rawQuery("SELECT COUNT(*) FROM " + table, null);
        }

        cursor.moveToFirst();
        int count = cursor.getInt(0);
        cursor.close();

        return count;
    }

    private String getCurrentTimestamp() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US);
        return sdf.format(new Date());
    }
}
