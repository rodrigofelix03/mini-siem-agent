import sqlite3

def get_recent_alerts(filter_date=None, limit=5):
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    
    if filter_date:
        cursor.execute("""
            SELECT ip, message, datetime(timestamp, 'unixepoch')
            FROM alerts
            WHERE date(datetime(timestamp, 'unixepoch')) = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (filter_date, limit))
    else:
        cursor.execute("""
            SELECT ip, message, datetime(timestamp, 'unixepoch')
            FROM alerts
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
    
    alerts = cursor.fetchall()
    conn.close()
    return alerts