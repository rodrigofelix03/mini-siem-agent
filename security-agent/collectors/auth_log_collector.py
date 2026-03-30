import time
import re
from utils.db import save_event
from detectors.brute_force_detector import detect_brute_force

LOG_FILE = r"C:\Users\rodri\Desktop\WD\projetos\mini-siem-agent\security-agent\fake_auth.log"
last_size = 0

def monitor_auth_log():
    global last_size
    print("🔍 A monitorizar logs...")

    while True:
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as file:
            file.seek(last_size)
            lines = file.readlines()
            last_size = file.tell()

        for line in lines:
            process_log_line(line)

        time.sleep(2)


def process_log_line(line):
    if "Failed password" in line:
        ip = extract_ip(line)
        print(f"⚠️ DETETADO: {ip}")

        save_event("failed_login", ip, time.time())

        detect_brute_force(ip)


def extract_ip(log_line):
    match = re.search(r"\d+\.\d+\.\d+\.\d+", log_line)
    return match.group(0) if match else "unknown"