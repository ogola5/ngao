import streamlit as st
import pandas as pd
import time
import os
import yaml

# Load Config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

LOG_FILE = config['paths']['log_file']

st.set_page_config(page_title="Ngao-Shield Command", page_icon="🛡️", layout="wide")

# UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff41; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Ngao-Shield: National Cyber Defense Grid")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("Status", "ACTIVE", "Federated")
col2.metric("Encryption", "AES-256", "Quantum-Safe")
col3.metric("Active Nodes", str(config['federated']['min_clients']), "Online")

st.markdown("### 📈 Live Federation Accuracy")
chart_holder = st.empty()

while True:
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            if not df.empty:
                chart_holder.line_chart(df.set_index("Round"))
        except Exception:
            pass
    time.sleep(1)