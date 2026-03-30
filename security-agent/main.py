from collectors.auth_log_collector import monitor_auth_log
from utils.db import init_db
import subprocess
import threading

# --- Função para correr o Streamlit ---
def run_dashboard():
    subprocess.Popen([
        "streamlit", "run", "dashboard.py", "--server.headless", "false"
    ])

if __name__ == "__main__":
    # Inicializa a base de dados
    init_db()

    # Inicia o dashboard num thread separado
    threading.Thread(target=run_dashboard, daemon=True).start()

    # Inicia a monitorização de logs normalmente
    print("🔍 A monitorizar logs...")
    monitor_auth_log()