import streamlit as st
import sqlite3
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import pandas as pd

def show_security_dashboard():
    st_autorefresh(interval=5000, key="security_refresh")

    conn = sqlite3.connect("events.db", check_same_thread=False)

    st.header("🔐 Eventos de Segurança")

    date_input = st.sidebar.date_input("Escolher data", datetime.today())
    date_str = date_input.strftime("%Y-%m-%d")

    st.subheader(f"📅 Dados do dia: {date_str}")

    # --- Eventos por hora ---
    query = """
    SELECT strftime('%H', datetime(timestamp, 'unixepoch')) as hour,
           COUNT(*) as attempts
    FROM events
    WHERE date(timestamp, 'unixepoch') = ?
    GROUP BY hour
    ORDER BY hour
    """
    df_hour = pd.read_sql_query(query, conn, params=(date_str,))

    st.subheader("📊 Tentativas por hora")
    if not df_hour.empty:
        st.line_chart(df_hour.set_index("hour"))
    else:
        st.write("Sem dados.")

    # --- Eventos por dia ---
    query = """
    SELECT date(timestamp, 'unixepoch') as day,
           COUNT(*) as attempts
    FROM events
    GROUP BY day
    ORDER BY day
    """
    df_day = pd.read_sql_query(query, conn)

    st.subheader("📊 Eventos por dia")
    if not df_day.empty:
        st.bar_chart(df_day.set_index("day"))

    # --- Top IPs ---
    query = """
    SELECT ip, COUNT(*) as attempts
    FROM events
    WHERE date(timestamp, 'unixepoch') = ?
    GROUP BY ip
    ORDER BY attempts DESC
    LIMIT 5
    """
    df_ips = pd.read_sql_query(query, conn, params=(date_str,))

    st.subheader("🌍 Top IPs")
    if not df_ips.empty:
        st.table(df_ips)

    # --- Alertas ---
    query = """
    SELECT ip, message, datetime(timestamp, 'unixepoch') as time
    FROM alerts
    WHERE date(timestamp, 'unixepoch') = ?
    ORDER BY timestamp DESC
    """
    df_alerts = pd.read_sql_query(query, conn, params=(date_str,))

    st.subheader("🚨 Alertas")
    if not df_alerts.empty:
        for _, row in df_alerts.iterrows():
            st.error(f"[{row['time']}] {row['ip']} - {row['message']}")
    else:
        st.success("Nenhum alerta crítico 🎉")