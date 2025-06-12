import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('sleep_bot.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_user_id INTEGER PRIMARY KEY,
            morning_time TEXT,
            evening_time TEXT
        )
    ''')
    
    # Create records table without foreign key
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id INTEGER,
            wake_up_time TEXT,
            asleep_time TEXT,
            record_date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(telegram_user_id, morning_time, evening_time):
    conn = sqlite3.connect('sleep_bot.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users (telegram_user_id, morning_time, evening_time) VALUES (?, ?, ?)',
              (telegram_user_id, morning_time, evening_time))
    conn.commit()
    conn.close()

def get_user(telegram_user_id):
    conn = sqlite3.connect('sleep_bot.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE telegram_user_id = ?', (telegram_user_id,))
    user = c.fetchone()
    conn.close()
    return user

def add_record(telegram_user_id, wake_up_time, asleep_time):
    conn = sqlite3.connect('sleep_bot.db')
    c = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')
    c.execute('INSERT INTO records (telegram_user_id, wake_up_time, asleep_time, record_date) VALUES (?, ?, ?, ?)',
              (telegram_user_id, wake_up_time, asleep_time, current_date))
    conn.commit()
    conn.close()

def get_user_records(telegram_user_id):
    conn = sqlite3.connect('sleep_bot.db')
    c = conn.cursor()
    c.execute('SELECT * FROM records WHERE telegram_user_id = ? ORDER BY id DESC', (telegram_user_id,))
    records = c.fetchall()
    conn.close()
    return records

def update_user_times(telegram_user_id, morning_time, evening_time):
    conn = sqlite3.connect('sleep_bot.db')
    c = conn.cursor()
    c.execute('UPDATE users SET morning_time = ?, evening_time = ? WHERE telegram_user_id = ?',
              (morning_time, evening_time, telegram_user_id))
    conn.commit()
    conn.close()

def update_previous_day_sleep_time(telegram_user_id, sleep_time):
    conn = sqlite3.connect('sleep_bot.db')
    c = conn.cursor()
    
    # Get the most recent record for this user
    c.execute('''
        SELECT id FROM records 
        WHERE telegram_user_id = ? 
        ORDER BY record_date DESC, id DESC 
        LIMIT 1 OFFSET 1
    ''', (telegram_user_id,))
    
    result = c.fetchone()
    if result:
        record_id = result[0]
        # Update the sleep time for the previous day's record
        c.execute('''
            UPDATE records 
            SET asleep_time = ? 
            WHERE id = ?
        ''', (sleep_time, record_id))
        
    conn.commit()
    conn.close() 