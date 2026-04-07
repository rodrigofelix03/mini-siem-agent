# modules/network.py
import psutil
import socket
import sqlite3
from backend.detectors.network_detector import analyze_connection
from backend.utils.ip_geo import get_ip_info

def get_network_data(filter_date=None):
    """
    Retorna os dados de rede em JSON, pronto para consumo pelo React.
    """
    # --- IP Local ---
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # --- Estatísticas de rede ---
    net_io = psutil.net_io_counters()
    net_stats = {
        "bytes_sent_mb": round(net_io.bytes_sent / (1024**2), 2),
        "bytes_recv_mb": round(net_io.bytes_recv / (1024**2), 2)
    }

    # --- Conexões ativas ---
    connections = psutil.net_connections(kind='inet')
    active_connections = []
    connections_map = []
    LOCAL_LAT, LOCAL_LON = 38.72, -9.13

    for conn in connections:
        if conn.status == "ESTABLISHED" and conn.raddr:
            ip = conn.raddr.ip
            geo = get_ip_info(ip)
            active_connections.append({
                "remote_ip": ip,
                "port": conn.raddr.port,
                "country": geo["country"],
                "city": geo["city"]
            })

            risk = analyze_connection(conn)
            if risk >= 3:
                color = [255,0,0]
                width = 4
            elif risk > 0:
                color = [255,165,0]
                width = 3
            else:
                color = [0,255,0]
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

    # --- Alertas de rede ---
    conn_db = sqlite3.connect("events.db")
    cursor = conn_db.cursor()
    cursor.execute("""
        SELECT ip, message, datetime(timestamp, 'unixepoch')
        FROM alerts
        ORDER BY timestamp DESC
        LIMIT 5
    """)
    alerts = [{"ip": ip, "message": msg, "timestamp": ts} for ip, msg, ts in cursor.fetchall()]
    conn_db.close()

    # --- Portas em escuta ---
    listening_ports = []
    for conn in connections:
        if conn.status == "LISTEN":
            listening_ports.append({
                "ip": conn.laddr.ip,
                "port": conn.laddr.port
            })

    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "network_stats": net_stats,
        "active_connections": active_connections,
        "connections_map": connections_map,
        "alerts": alerts,
        "listening_ports": listening_ports[:10]
    }