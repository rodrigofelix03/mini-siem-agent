import streamlit as st
import psutil
from streamlit_autorefresh import st_autorefresh

def show_infrastructure_dashboard():
    st_autorefresh(interval=5000, key="infra_refresh")

    st.header("💻 Monitorização de Infraestrutura")

    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    col1, col2 = st.columns(2)

    with col1:
        st.metric("CPU Usage", f"{cpu_percent:.1f}%")
        st.progress(min(int(cpu_percent), 100))

    with col2:
        st.metric(
            "RAM Usage",
            f"{memory.percent:.1f}%",
            f"{memory.used / (1024**3):.2f}GB / {memory.total / (1024**3):.2f}GB"
        )
        st.progress(int(memory.percent))

    st.subheader("💾 Disco")
    st.metric(
        "Disk Usage",
        f"{disk.percent:.1f}%",
        f"{disk.used / (1024**3):.2f}GB / {disk.total / (1024**3):.2f}GB"
    )
    st.progress(int(disk.percent))

    st.subheader("🔥 Top Processos por CPU")

    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(p.info)
        except:
            continue

    top_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

    for proc in top_cpu:
        st.write(f"{proc['name']} (PID {proc['pid']}): {proc['cpu_percent']}% CPU")