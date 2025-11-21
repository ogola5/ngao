import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import time
from datetime import datetime

# --- 1. CONFIGURATION (The Foundation) ---
st.set_page_config(
    page_title="NGAO-SHIELD | COMMAND",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. STATE MANAGEMENT (The Brain) ---
class StateManager:
    @staticmethod
    def init():
        if 'attack_mode' not in st.session_state:
            st.session_state.attack_mode = False
        if 'counter' not in st.session_state:
            st.session_state.counter = 0
        if 'log_data' not in st.session_state:
            # Pre-fill with healthy data for the graph
            st.session_state.log_data = pd.DataFrame({
                "Time": range(20),
                "Integrity": [0.95 + np.random.uniform(-0.01, 0.01) for _ in range(20)]
            })
        if 'attack_progress' not in st.session_state:
            st.session_state.attack_progress = 0.0
        if 'logs' not in st.session_state:
            st.session_state.logs = []

StateManager.init()

# --- 3. UI & THEME ENGINE (The "Hollywood" Look) ---
class ThemeManager:
    @staticmethod
    def apply_custom_css():
        main_color = "#ff2b2b" if st.session_state.attack_mode else "#00ff41"
        
        st.markdown(f"""
            <style>
            /* TERMINAL FONT FOR EVERYTHING */
            .stApp {{ font-family: 'Courier New', monospace; background-color: #0e1117; }}
            
            /* GLOWING HEADERS */
            h1, h2, h3 {{ 
                color: {main_color} !important; 
                text-shadow: 0 0 10px {main_color};
            }}
            
            /* CUSTOM METRIC BOXES */
            div[data-testid="stMetric"] {{
                background-color: #161b22;
                border-left: 4px solid {main_color};
                padding: 15px;
                box-shadow: 0 0 15px rgba(0,0,0,0.5);
                transition: transform 0.2s;
            }}
            div[data-testid="stMetric"]:hover {{
                transform: scale(1.02);
            }}
            div[data-testid="stMetricLabel"] {{ color: #8b949e; font-size: 14px; letter-spacing: 1px; }}
            div[data-testid="stMetricValue"] {{ color: {main_color} !important; font-size: 26px; }}
            
            /* BUTTONS */
            .stButton>button {{
                border: 1px solid {main_color};
                color: {main_color};
                background: transparent;
                width: 100%;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: bold;
                padding: 10px;
            }}
            .stButton>button:hover {{
                background: {main_color};
                color: black;
                box-shadow: 0 0 20px {main_color};
            }}
            </style>
        """, unsafe_allow_html=True)

# --- 4. DATA SIMULATION ENGINE (The Backend) ---
class NetworkSimulation:
    @staticmethod
    def update_metrics():
        # Update Counter
        st.session_state.counter += 1
        
        # Animate Missile (0.0 to 1.0)
        if st.session_state.attack_mode:
            st.session_state.attack_progress += 0.05 # Speed of missile
            if st.session_state.attack_progress > 1.0:
                st.session_state.attack_progress = 0.0 # Reset to loop
        else:
            st.session_state.attack_progress = 0.0

        # Update Graph Data
        new_time = st.session_state.log_data.iloc[-1]["Time"] + 1
        current_val = st.session_state.log_data.iloc[-1]["Integrity"]
        
        if st.session_state.attack_mode:
            # Drastic drop with noise
            change = np.random.uniform(-0.15, -0.05)
            new_val = max(0.2, current_val + change)
        else:
            # Slow recovery
            change = np.random.uniform(0.01, 0.08)
            new_val = min(0.99, current_val + change)
            
        new_row = pd.DataFrame({"Time": [new_time], "Integrity": [new_val]})
        st.session_state.log_data = pd.concat([st.session_state.log_data, new_row]).tail(40)

    @staticmethod
    def generate_log_entry():
        t = datetime.now().strftime('%H:%M:%S')
        if st.session_state.attack_mode:
            log_pool = [
                f"[CRIT] {t} | UDP FLOOD DETECTED ON PORT 443",
                f"[WARN] {t} | NODE_MOMBASA LATENCY > 600ms",
                f"[INFO] {t} | DEPLOYING MEDIAN ROBUSTNESS AGGREGATION...",
                f"[ACTN] {t} | IP 45.12.x.x BLACKLISTED VIA eBPF",
                f"[ALRT] {t} | SIGNATURE MISMATCH IN LAYER 7"
            ]
            entry = np.random.choice(log_pool)
        else:
            log_pool = [
                f"[INFO] {t} | HEARTBEAT RECEIVED FROM MOMBASA_NODE",
                f"[INFO] {t} | HEARTBEAT RECEIVED FROM KISUMU_NODE",
                f"[INFO] {t} | FEDERATED ROUND {st.session_state.counter} COMPLETE",
                f"[OKAY] {t} | MODEL INTEGRITY VERIFIED (SHA-256)",
                f"[INFO] {t} | DIFFERENTIAL PRIVACY NOISE ADDED (Epsilon=1.2)"
            ]
            entry = np.random.choice(log_pool)
        
        st.session_state.logs.append(entry)
        if len(st.session_state.logs) > 8:
            st.session_state.logs.pop(0)

# --- 5. MAP ENGINE (PyDeck with Missile) ---
class MapEngine:
    @staticmethod
    def render_map():
        # Coordinates
        NAIROBI = [-1.2921, 36.8219]
        MOMBASA = [-4.0435, 39.6682]
        KISUMU = [-0.0917, 34.7680]
        ELDORET = [0.5143, 35.2698]
        ATTACKER = [15.5007, 32.5599] # Khartoum/North region

        # Interpolate Missile Position
        if st.session_state.attack_mode:
            t = st.session_state.attack_progress
            # Linear interpolation (Lerp)
            missile_lat = ATTACKER[0] + (NAIROBI[0] - ATTACKER[0]) * t
            missile_lon = ATTACKER[1] + (NAIROBI[1] - ATTACKER[1]) * t
            missile_pos = [missile_lon, missile_lat]
            missile_color = [255, 0, 0, 255]
            missile_radius = 50000
        else:
            missile_pos = [0, 0] # Hidden
            missile_color = [0, 0, 0, 0]
            missile_radius = 0

        # Node Data
        nodes = [
            {"name": "HQ (Nairobi)", "coords": NAIROBI, "color": [0, 255, 0, 255]},
            {"name": "Mombasa Port", "coords": MOMBASA, "color": [0, 255, 0, 200]},
            {"name": "Kisumu Hub", "coords": KISUMU, "color": [0, 255, 0, 200]},
            {"name": "Eldoret Node", "coords": ELDORET, "color": [0, 255, 0, 200]},
        ]
        
        # Connection Arcs
        arcs = [
            {"source": NAIROBI, "target": MOMBASA},
            {"source": NAIROBI, "target": KISUMU},
            {"source": NAIROBI, "target": ELDORET},
        ]
        
        # If Attack: Add Red Arc and Attacker Node
        if st.session_state.attack_mode:
            arcs.append({"source": ATTACKER, "target": NAIROBI})
            nodes[0]["color"] = [255, 100, 0, 255] # Nairobi turns Orange
            nodes.append({"name": "UNKNOWN THREAT", "coords": ATTACKER, "color": [255, 0, 0, 255]})

        # Layers
        layer_nodes = pdk.Layer(
            "ScatterplotLayer",
            data=nodes,
            get_position="coords",
            get_color="color",
            get_radius=20000,
            pickable=True,
        )

        layer_missile = pdk.Layer(
            "ScatterplotLayer",
            data=[{"pos": missile_pos}],
            get_position="pos",
            get_color=missile_color,
            get_radius=missile_radius,
            pickable=False,
        )

        layer_arcs = pdk.Layer(
            "ArcLayer",
            data=arcs,
            get_source_position="source",
            get_target_position="target",
            get_width=5,
            get_source_color=[255, 0, 0] if st.session_state.attack_mode else [0, 255, 100],
            get_target_color=[255, 0, 0] if st.session_state.attack_mode else [0, 255, 100],
            get_tilt=15,
        )

        return pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(latitude=1.5, longitude=37.0, zoom=5.5, pitch=45),
            layers=[layer_nodes, layer_arcs, layer_missile],
            tooltip={"text": "{name}"}
        )

# --- 6. MAIN APP EXECUTION ---
def main():
    ThemeManager.apply_custom_css()
    NetworkSimulation.update_metrics()
    NetworkSimulation.generate_log_entry()

    # -- HEADER --
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("🛡️ NGAO-SHIELD // OVERWATCH")
        st.caption("FEDERATED CYBER-DEFENSE GRID | v3.0.1-BETA")
    with c2:
        status = "CRITICAL" if st.session_state.attack_mode else "SECURE"
        st.markdown(f"# [{status}]")

    # -- METRICS ROW --
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("GRID NODES", "4", "NRB/MBA/KSM/ELD")
    m2.metric("AVG LATENCY", f"{np.random.randint(12, 28)}ms", "+2ms")
    m3.metric("PRIVACY BUDGET", "ε=0.8", "DP-SGD")
    
    with m4:
        if st.session_state.attack_mode:
            if st.button("💠 DEPLOY VACCINE"):
                st.session_state.attack_mode = False
                st.session_state.log_data = st.session_state.log_data.tail(20) # Reset graph view
                st.rerun()
        else:
            if st.button("☢️ SIMULATE ATTACK"):
                st.session_state.attack_mode = True
                st.rerun()

    # -- MAIN VISUALS --
    col_map, col_data = st.columns([1.5, 1])
    
    with col_map:
        st.markdown("### 📡 LIVE THREAT GEOMETRY")
        st.pydeck_chart(MapEngine.render_map())

    with col_data:
        st.markdown("### 🧬 MODEL INTEGRITY")
        
        # Sexy Altair Gradient Chart
        color_hex = "#ff2b2b" if st.session_state.attack_mode else "#00ff41"
        chart = alt.Chart(st.session_state.log_data).mark_area(
            line={'color': color_hex},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color=color_hex, offset=0),
                       alt.GradientStop(color=color_hex, offset=1)],
                x1=1, x2=1, y1=1, y2=0
            ),
            opacity=0.5
        ).encode(
            x=alt.X('Time', axis=None),
            y=alt.Y('Integrity', scale=alt.Scale(domain=[0, 1.1]))
        ).properties(height=250)
        
        st.altair_chart(chart, use_container_width=True)

        # Terminal Logs
        st.markdown("### 📝 KERNEL LOGS")
        
        # Display logs as a code block (looks like a terminal)
        log_text = "\n".join(st.session_state.logs)
        st.code(log_text, language="bash")

    # -- AUTO REFRESH LOOP --
    # Updates every 0.8 seconds for smooth animation
    time.sleep(0.8) 
    st.rerun()

if __name__ == "__main__":
    main()