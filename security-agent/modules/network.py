import streamlit as st
import psutil
import socket
import sqlite3
from streamlit_autorefresh import st_autorefresh
from detectors.network_detector import analyze_connection
from utils.ip_geo import get_ip_info
import pandas as pd
import pydeck as pdk

def show_network_dashboard():
    st_autorefresh(interval=5000, key="network_refresh")

    st.header("🌐 Monitorização de Rede")

    # --- IP Local ---
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    st.subheader("📍 Informação da Máquina")
    st.write(f"Hostname: {hostname}")
    st.write(f"IP Local: {local_ip}")

    # --- Estatísticas de rede ---
    net_io = psutil.net_io_counters()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📤 Bytes Enviados", f"{net_io.bytes_sent / (1024**2):.2f} MB")

    with col2:
        st.metric("📥 Bytes Recebidos", f"{net_io.bytes_recv / (1024**2):.2f} MB")

    # --- Conexões ativas ---
    st.subheader("🔗 Conexões Ativas")

    connections = psutil.net_connections(kind='inet')

    active_connections = []
    
    map_data = []

    for conn in connections:
        if conn.status == "ESTABLISHED" and conn.raddr:
            ip = conn.raddr.ip

            geo = get_ip_info(ip)

            active_connections.append({
                "Remote IP": ip,
                "Port": conn.raddr.port,
                "Country": geo["country"],
                "City": geo["city"]
            })

            if geo["lat"] and geo["lon"]:
                map_data.append({
                    "lat": geo["lat"],
                    "lon": geo["lon"]
                })

        # --- Mapa com direções ---
    st.subheader("🗺 Ligações de Rede (Origem → Destino)")

    connections_map = []

    LOCAL_LAT = 38.72
    LOCAL_LON = -9.13

    for conn in connections:
        if conn.status == "ESTABLISHED" and conn.raddr:
            ip = conn.raddr.ip
            geo = get_ip_info(ip)

            risk = analyze_connection(conn)  # retorna score

            # cores: vermelho forte para risco alto, verde para normal
            if risk >= 3:
                color = [255, 0, 0]  # vermelho
                width = 4
            elif risk > 0:
                color = [255, 165, 0]  # laranja
                width = 3
            else:
                color = [0, 255, 0]  # verde
                width = 2

            if geo["lat"] and geo["lon"]:
                connections_map.append({
                    "from_lat": LOCAL_LAT,
                    "from_lon": LOCAL_LON,
                    "to_lat": geo["lat"],
                    "to_lon": geo["lon"],
                    "color": color,
                    "width": width
                })

    if connections_map:
        layer = pdk.Layer(
            "LineLayer",
            data=connections_map,
            get_source_position='[from_lon, from_lat]',
            get_target_position='[to_lon, to_lat]',
            get_color='color',
            get_width='width'
        )

        view_state = pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1
        )

        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state
        ))

    # --- Alertas de rede ---
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT ip, message, datetime(timestamp, 'unixepoch')
    FROM alerts
    ORDER BY timestamp DESC
    LIMIT 5
    """)

    alerts = cursor.fetchall()

    st.subheader("🚨 Alertas de Rede")

    for ip, msg, ts in alerts:
        st.warning(f"[{ts}] {ip} - {msg}")

    # --- Portas abertas ---
    st.subheader("🔓 Portas em Escuta")

    listening_ports = []
    for conn in connections:
        if conn.status == "LISTEN":
            listening_ports.append({
                "IP": conn.laddr.ip,
                "Porta": conn.laddr.port
            })

    if listening_ports:
        st.table(listening_ports[:10])
    else:
        st.write("Nenhuma porta em escuta detetada.")