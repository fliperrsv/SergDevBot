import sqlite3
from datetime import datetime

DB_NAME = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language TEXT DEFAULT 'ru',
            is_premium INTEGER DEFAULT 0,
            joined_at TIMESTAMP,
            last_active TIMESTAMP
        )
    ''')
    # Таблица напоминаний
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            remind_at TIMESTAMP,
            status TEXT DEFAULT 'active'
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name, last_name, language='ru'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, language, joined_at, last_active)
        VALUES (?, ?, ?, ?, ?, COALESCE((SELECT joined_at FROM users WHERE user_id = ?), ?), ?)
    ''', (user_id, username, first_name, last_name, language, user_id, datetime.now(), datetime.now()))
    conn.commit()
    conn.close()

def update_last_active(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET last_active = ? WHERE user_id = ?', (datetime.now(), user_id))
    conn.commit()
    conn.close()

def update_language(user_id, language):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
    conn.commit()
    conn.close()

def set_premium(user_id, is_premium):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_premium = ? WHERE user_id = ?', (is_premium, user_id))
    conn.commit()
    conn.close()

def get_user_language(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'ru'

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username, first_name, language, is_premium FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_users_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Напоминания
def add_reminder(user_id, text, remind_at):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reminders (user_id, text, remind_at) VALUES (?, ?, ?)', (user_id, text, remind_at))
    conn.commit()
    conn.close()

def get_active_reminders():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, user_id, text, remind_at FROM reminders WHERE status = "active" AND remind_at <= ?', (datetime.now(),))
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def mark_reminder_done(reminder_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE reminders SET status = "done" WHERE id = ?', (reminder_id,))
    conn.commit()
    conn.close()

def get_user_reminders(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, text, remind_at, status FROM reminders WHERE user_id = ? ORDER BY remind_at DESC', (user_id,))
    reminders = cursor.fetchall()
    conn.close()
    return reminders
