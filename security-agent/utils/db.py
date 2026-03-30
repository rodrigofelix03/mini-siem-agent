import sqlite3

conn = sqlite3.connect("events.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        ip TEXT,
        timestamp REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        ip TEXT,
        message TEXT,
        timestamp REAL
    )
    """)

    conn.commit()


def save_alert(alert_type, ip, message, timestamp):
    cursor.execute(
        "INSERT INTO alerts (type, ip, message, timestamp) VALUES (?, ?, ?, ?)",
        (alert_type, ip, message, timestamp)
    )
    conn.commit()

def save_event(event_type, ip, timestamp):
    cursor.execute(
        "INSERT INTO events (type, ip, timestamp) VALUES (?, ?, ?)",
        (event_type, ip, timestamp)
    )
    conn.commit()