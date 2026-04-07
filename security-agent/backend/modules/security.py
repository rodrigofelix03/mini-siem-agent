# modules/security.py
import sqlite3
import pandas as pd
from datetime import date

def get_security_data(filter_date=None):
    """
    Retorna os eventos de segurança em JSON, pronto para consumo pelo React.
    """
    if filter_date is None:
        filter_date = date.today().isoformat()  # formato YYYY-MM-DD

    conn = sqlite3.connect("events.db", check_same_thread=False)

    # --- Eventos por hora ---
    query_hour = """
    SELECT strftime('%H', datetime(timestamp, 'unixepoch')) as hour,
           COUNT(*) as attempts
    FROM events
    WHERE date(timestamp, 'unixepoch') = ?
    GROUP BY hour
    ORDER BY hour
    """
    df_hour = pd.read_sql_query(query_hour, conn, params=(filter_date,))
    hourly_attempts = df_hour.to_dict(orient="records")  # lista de dicionários

    # --- Eventos por dia ---
    query_day = """
    SELECT date(timestamp, 'unixepoch') as day,
           COUNT(*) as attempts
    FROM events
    GROUP BY day
    ORDER BY day
    """
    df_day = pd.read_sql_query(query_day, conn)
    daily_attempts = df_day.to_dict(orient="records")

    # --- Top IPs ---
    query_ips = """
    SELECT ip, COUNT(*) as attempts
    FROM events
    WHERE date(timestamp, 'unixepoch') = ?
    GROUP BY ip
    ORDER BY attempts DESC
    LIMIT 5
    """
    df_ips = pd.read_sql_query(query_ips, conn, params=(filter_date,))
    top_ips = df_ips.to_dict(orient="records")

    # --- Alertas ---
    query_alerts = """
    SELECT ip, message, datetime(timestamp, 'unixepoch') as time
    FROM alerts
    WHERE date(timestamp, 'unixepoch') = ?
    ORDER BY timestamp DESC
    """
    df_alerts = pd.read_sql_query(query_alerts, conn, params=(filter_date,))
    alerts = df_alerts.to_dict(orient="records")

    conn.close()

    return {
        "filter_date": filter_date,
        "hourly_attempts": hourly_attempts,
        "daily_attempts": daily_attempts,
        "top_ips": top_ips,
        "alerts": alerts
    }