import streamlit as st
import sqlite3
from datetime import datetime
import psutil

# Conectar à DB
conn = sqlite3.connect("events.db", check_same_thread=False)
cursor = conn.cursor()

st.title("🛡 Mini SIEM Dashboard")

# --- Sidebar com navegação ---
module = st.sidebar.selectbox("Selecionar módulo", ["Eventos de Segurança", "Infraestrutura"])

if module == "Eventos de Segurança":
    st.header("📅 Eventos de Segurança")

    # Seleção de data
    date_input = st.sidebar.date_input("Escolher data", datetime.today())
    date_str = date_input.strftime("%Y-%m-%d")

    # --- Eventos por IP ---
    cursor.execute("""
        SELECT ip, COUNT(*) as attempts
        FROM events
        WHERE date(timestamp, 'unixepoch') = ?
        GROUP BY ip
        ORDER BY attempts DESC
        LIMIT 10
    """, (date_str,))
    events = cursor.fetchall()

    st.subheader("Top IPs por tentativas de login")
    if events:
        for ip, attempts in events:
            st.write(f"- {ip}: {attempts} tentativas")
    else:
        st.write("Nenhum evento registado neste dia.")

    # --- Alertas do dia ---
    cursor.execute("""
        SELECT ip, message, datetime(timestamp, 'unixepoch') 
        FROM alerts
        WHERE date(timestamp, 'unixepoch') = ?
        ORDER BY timestamp DESC
    """, (date_str,))
    alerts = cursor.fetchall()

    st.subheader("Alertas do dia")
    if alerts:
        for ip, message, ts in alerts:
            st.write(f"- [{ts}] {ip}: {message}")
    else:
        st.write("Nenhum alerta registado neste dia.")

elif module == "Infraestrutura":
    st.header("💻 Monitorização de Infraestrutura")

    # --- CPU ---
    cpu_percent = psutil.cpu_percent(interval=1)
    st.subheader("CPU")
    st.progress(min(int(cpu_percent), 100))

    # --- Memória ---
    memory = psutil.virtual_memory()
    st.subheader("Memória RAM")
    st.write(f"Usada: {memory.percent}% ({memory.used / (1024**3):.2f} GB / {memory.total / (1024**3):.2f} GB)")

    # --- Disco ---
    disk = psutil.disk_usage('/')
    st.subheader("Disco")
    st.write(f"Usado: {disk.percent}% ({disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB)")

    # --- Top processos CPU ---
    st.subheader("Top processos por CPU")
    processes = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) 
                 for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    top_cpu = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
    for pid, name, cpu in top_cpu:
        st.write(f"- {name} (PID {pid}): {cpu}% CPU")