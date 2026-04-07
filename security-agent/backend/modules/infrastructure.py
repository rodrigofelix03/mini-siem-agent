# modules/infrastructure.py
import psutil

def get_infra_data(filter_date=None):
    """
    Retorna os dados de infraestrutura em JSON, pronto para consumo pelo React.
    """
    # Uso de CPU, memória e disco
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # Top 5 processos por CPU
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(p.info)
        except Exception:
            continue

    top_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

    # Estrutura JSON
    data = {
        "cpu": {
            "percent": cpu_percent
        },
        "memory": {
            "percent": memory.percent,
            "used_gb": round(memory.used / (1024**3), 2),
            "total_gb": round(memory.total / (1024**3), 2)
        },
        "disk": {
            "percent": disk.percent,
            "used_gb": round(disk.used / (1024**3), 2),
            "total_gb": round(disk.total / (1024**3), 2)
        },
        "top_cpu_processes": [
            {"pid": proc['pid'], "name": proc['name'], "cpu_percent": proc['cpu_percent']}
            for proc in top_cpu
        ]
    }

    return data