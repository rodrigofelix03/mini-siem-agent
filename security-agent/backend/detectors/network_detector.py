from backend.utils.db import save_alert
import time

# portas suspeitas comuns
SUSPICIOUS_PORTS = {4444, 1337, 6666, 5555}

# tracking de conexões por IP
connection_count = {}

THRESHOLD = 10  # nº de conexões para alertar

def analyze_connection(conn):
    if not conn.raddr:
        return

    ip = conn.raddr.ip
    port = conn.raddr.port
    now = time.time()

    # --- 1. IP externo ---
    if not ip.startswith(("192.168.", "10.", "172.")):
        save_alert(
            "suspicious_ip",
            ip,
            f"Conexão para IP externo: {ip}:{port}",
            now
        )

    # --- 2. Porta suspeita ---
    if port in SUSPICIOUS_PORTS:
        save_alert(
            "suspicious_port",
            ip,
            f"Conexão para porta suspeita {port}",
            now
        )

    # --- 3. Muitas conexões ---
    connection_count[ip] = connection_count.get(ip, 0) + 1

    if connection_count[ip] >= THRESHOLD:
        save_alert(
            "connection_spike",
            ip,
            f"Muitas conexões para {ip}",
            now
        )
        connection_count[ip] = 0

def analyze_connection(conn):
    if not conn.raddr:
        return 0  # risco 0

    ip = conn.raddr.ip
    port = conn.raddr.port
    risk = 0

    # IP externo
    if not ip.startswith(("192.168.", "10.", "172.")):
        risk += 2  # alto

    # Porta suspeita
    if port in {4444, 1337, 6666, 5555}:
        risk += 3

    # Muitas conexões
    connection_count[ip] = connection_count.get(ip, 0) + 1
    if connection_count[ip] >= 10:
        risk += 1
        connection_count[ip] = 0

    return risk