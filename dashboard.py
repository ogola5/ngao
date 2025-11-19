import streamlit as st
import pandas as pd
import time
import os

# Page Config
st.set_page_config(
    page_title="Ngao-Sync | Cyber Command",
    page_icon="🛡️",
    layout="wide"
)

# CSS for "Hacker" look
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #00FF41;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.title("🛡️")
with col2:
    st.title("Ngao-Sync: National Cyber Grid")
    st.markdown("**Status:** 🟢 ONLINE | **Encryption:** FEDERATED | **Nodes:** 3 Active")

st.divider()

# Layout: Metrics & Graphs
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📡 Connected Nodes")
    st.info("🏛️ Ministry of Health (Client 1)")
    st.info("🏦 KCB Group (Client 2)")
    st.info("🛂 eCitizen Portal (Client 3)")

with col2:
    st.markdown("### 📊 Global Immunity Level")
    placeholder = st.empty()

with col3:
    st.markdown("### ⚠️ Live Threat Stream")
    st.warning("🛑 SQL Injection blocked at Node 1")
    st.warning("🛑 DDoS Attempt blocked at Node 2")
    st.success("✅ Cross-Node Patterns Updated")

st.divider()

# The Live Graph
st.subheader("📈 Real-Time Federated Learning Accuracy")
chart_holder = st.empty()

# LOGIC: Read the CSV file in a loop to update the graph
LOG_FILE = "training_log.csv"

while True:
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            
            # Update Metric
            if not df.empty:
                latest_acc = df.iloc[-1]["Accuracy"]
                placeholder.metric(label="Current Defense Accuracy", value=f"{latest_acc*100:.2f}%")
            
            # Update Chart
            chart_holder.line_chart(df.set_index("Round"))
            
        except Exception as e:
            pass
    
    time.sleep(1) # Refresh every second