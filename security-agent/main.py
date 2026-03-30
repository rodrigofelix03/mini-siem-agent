from collectors.auth_log_collector import monitor_auth_log
from utils.db import init_db

if __name__ == "__main__":
    init_db()
    monitor_auth_log()