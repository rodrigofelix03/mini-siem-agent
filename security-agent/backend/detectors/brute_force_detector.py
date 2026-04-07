from collections import defaultdict
import time
from utils.db import save_alert

failed_attempts = defaultdict(list)

THRESHOLD = 5
TIME_WINDOW = 60  # segundos

def detect_brute_force(ip):
    now = time.time()

    failed_attempts[ip].append(now)

    # manter só tentativas recentes
    failed_attempts[ip] = [
        t for t in failed_attempts[ip] if now - t < TIME_WINDOW
    ]

    if len(failed_attempts[ip]) >= THRESHOLD:
        message = f"Possível ataque de brute force do IP {ip}"
        print(f"🚨 ALERTA: {message}")

        save_alert("brute_force", ip, message, now)

        # limpar para evitar spam de alertas
        failed_attempts[ip] = []