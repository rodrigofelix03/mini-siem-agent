import streamlit as st
from modules.security import show_security_dashboard
from modules.infrastructure import show_infrastructure_dashboard
from modules.network import show_network_dashboard

st.set_page_config(page_title="Mini SIEM", layout="wide")

st.title("🛡 Mini SIEM Dashboard")

# Sidebar navegação
module = st.sidebar.selectbox(
    "Selecionar módulo",
    ["Eventos de Segurança", "Infraestrutura", "Rede"]
)

if module == "Eventos de Segurança":
    show_security_dashboard()

elif module == "Infraestrutura":
    show_infrastructure_dashboard()

elif module == "Rede":
    show_network_dashboard()