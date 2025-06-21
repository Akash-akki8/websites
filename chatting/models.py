import sqlite3

def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_message(sender, message, timestamp):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)',
                   (sender, message, timestamp))
    conn.commit()
    conn.close()

def load_messages():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sender, message, timestamp FROM messages ORDER BY id ASC')
    messages = cursor.fetchall()
    conn.close()
    return messages