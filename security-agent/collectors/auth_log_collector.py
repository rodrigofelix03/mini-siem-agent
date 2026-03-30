import time

LOG_FILE = r"C:\Users\rodri\Desktop\WD\projetos\mini-siem-agent\security-agent\fake_auth.log"
last_size = 0

def monitor_auth_log():
    global last_size
    print("🔍 A monitorizar logs...")

    while True:
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as file:
            file.seek(last_size)
            lines = file.readlines()
            last_size = file.tell()  # guarda onde paramos

        for line in lines:
            if "Failed password" in line:
                print("⚠️ DETETADO:", line.strip())

        time.sleep(2)  # espera 2s antes de abrir o ficheiro novamente