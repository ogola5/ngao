import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="NGAO-SHIELD | COMMAND",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. STATE MANAGEMENT ---
class StateManager:
    @staticmethod
    def init():
        if 'attack_mode' not in st.session_state:
            st.session_state.attack_mode = False
        if 'counter' not in st.session_state:
            st.session_state.counter = 0
        if 'log_data' not in st.session_state:
            st.session_state.log_data = pd.DataFrame({
                "Time": range(20),
                "Integrity": [0.95 + np.random.uniform(-0.01, 0.01) for _ in range(20)]
            })
        if 'attack_progress' not in st.session_state:
            st.session_state.attack_progress = 0.0
        if 'logs' not in st.session_state:
            st.session_state.logs = []

StateManager.init()

# --- 3. UI & THEME ENGINE (HIGH CONTRAST) ---
class ThemeManager:
    @staticmethod
    def apply_custom_css():
        # NEON RED vs NEON CYAN
        main_color = "#FF0000" if st.session_state.attack_mode else "#00FFC8"
        bg_color = "#000000" # Pitch black for contrast
        
        st.markdown(f"""
            <style>
            .stApp {{ font-family: 'Courier New', monospace; background-color: {bg_color}; }}
            
            /* High Contrast Headers */
            h1, h2, h3 {{ 
                color: {main_color} !important; 
                text-shadow: 0 0 15px {main_color};
            }}
            
            /* Cards */
            div[data-testid="stMetric"] {{
                background-color: #111;
                border: 1px solid {main_color};
                box-shadow: 0 0 10px {main_color}40;
            }}
            div[data-testid="stMetricValue"] {{ 
                color: {main_color} !important; 
                font-weight: 900;
                font-size: 28px;
            }}
            
            /* Buttons */
            .stButton>button {{
                border: 2px solid {main_color};
                color: {main_color};
                background: #000;
                font-weight: 900;
            }}
            .stButton>button:hover {{
                background: {main_color};
                color: #000;
                box-shadow: 0 0 25px {main_color};
            }}
            </style>
        """, unsafe_allow_html=True)

# --- 4. BACKEND LOGIC ---
class NetworkSimulation:
    @staticmethod
    def update_metrics():
        st.session_state.counter += 1
        
        # Missile Animation Speed
        if st.session_state.attack_mode:
            st.session_state.attack_progress += 0.04 # Slower, more dramatic
            if st.session_state.attack_progress > 1.0:
                st.session_state.attack_progress = 0.0
        else:
            st.session_state.attack_progress = 0.0

        # Graph Logic
        new_time = st.session_state.log_data.iloc[-1]["Time"] + 1
        current_val = st.session_state.log_data.iloc[-1]["Integrity"]
        
        if st.session_state.attack_mode:
            change = np.random.uniform(-0.15, -0.05)
            new_val = max(0.2, current_val + change)
        else:
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

# --- 5. THE NEON MAP ENGINE (This fixes your issue) ---
class MapEngine:
    @staticmethod
    def render_map():
        # --- DEFINITIONS ---
        NAIROBI = [-1.2921, 36.8219]
        MOMBASA = [-4.0435, 39.6682]
        KISUMU = [-0.0917, 34.7680]
        ELDORET = [0.5143, 35.2698]
        ATTACKER = [15.5007, 32.5599]

        # --- COLORS (NEON) ---
        # Safe: Neon Cyan | Attack: Hot Red
        SAFE_COLOR = [0, 255, 200, 255]      # Bright Cyan
        SAFE_GLOW = [0, 255, 200, 100]       # Transparent Cyan Halo
        
        ATTACK_COLOR = [255, 0, 0, 255]      # Bright Red
        ATTACK_GLOW = [255, 0, 0, 100]       # Transparent Red Halo

        # --- MISSILE LOGIC ---
        if st.session_state.attack_mode:
            t = st.session_state.attack_progress
            missile_lat = ATTACKER[0] + (NAIROBI[0] - ATTACKER[0]) * t
            missile_lon = ATTACKER[1] + (NAIROBI[1] - ATTACKER[1]) * t
            missile_pos = [missile_lon, missile_lat]
            
            # Missile is WHITE hot core with RED glow
            missile_core_color = [255, 255, 255, 255] 
            missile_radius = 60000
        else:
            missile_pos = [0, 0]
            missile_core_color = [0,0,0,0]
            missile_radius = 0

        # --- NODE SETUP ---
        # Base Nodes
        nodes = [
            {"name": "HQ (Nairobi)", "coords": NAIROBI},
            {"name": "Mombasa Port", "coords": MOMBASA},
            {"name": "Kisumu Hub", "coords": KISUMU},
            {"name": "Eldoret Node", "coords": ELDORET},
        ]
        
        # Determine Status Colors
        for node in nodes:
            if st.session_state.attack_mode and node["name"] == "HQ (Nairobi)":
                node["color"] = [255, 150, 0, 255] # Orange impact
                node["glow"] = [255, 100, 0, 150]
            else:
                node["color"] = SAFE_COLOR
                node["glow"] = SAFE_GLOW

        # Arcs
        arcs = [
            {"source": NAIROBI, "target": MOMBASA},
            {"source": NAIROBI, "target": KISUMU},
            {"source": NAIROBI, "target": ELDORET},
        ]
        
        if st.session_state.attack_mode:
            # Add Red Attack Line
            arcs.append({"source": ATTACKER, "target": NAIROBI})
            nodes.append({"name": "THREAT ACTOR", "coords": ATTACKER, "color": ATTACK_COLOR, "glow": ATTACK_GLOW})
            arc_src_col = ATTACK_COLOR
            arc_tgt_col = ATTACK_COLOR
        else:
            arc_src_col = SAFE_COLOR
            arc_tgt_col = SAFE_COLOR

        # --- LAYERS (The Layer Cake) ---
        
        # Layer 1: The Halo (Big transparent circle behind)
        layer_glow = pdk.Layer(
            "ScatterplotLayer",
            data=nodes,
            get_position="coords",
            get_color="glow",
            get_radius=80000, # HUGE Radius for visibility
            pickable=False,
            filled=True,
            stroked=False,
        )

        # Layer 2: The Core Node (Bright solid circle)
        layer_core = pdk.Layer(
            "ScatterplotLayer",
            data=nodes,
            get_position="coords",
            get_color="color",
            get_radius=35000, # Large visible core
            pickable=True,
            filled=True,
            stroked=True,
            get_line_color=[255, 255, 255], # White border for pop
            get_line_width=2000,
        )

        # Layer 3: The Missile
        layer_missile = pdk.Layer(
            "ScatterplotLayer",
            data=[{"pos": missile_pos}],
            get_position="pos",
            get_color=missile_core_color,
            get_radius=missile_radius,
            pickable=False,
            stroked=True,
            get_line_color=[255, 0, 0],
            get_line_width=4000
        )

        # Layer 4: The Arcs (Thick lines)
        layer_arcs = pdk.Layer(
            "ArcLayer",
            data=arcs,
            get_source_position="source",
            get_target_position="target",
            get_width=8, # THICK lines
            get_source_color=arc_src_col,
            get_target_color=arc_tgt_col,
            get_tilt=15,
        )

        return pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(latitude=1.0, longitude=37.0, zoom=5.2, pitch=30),
            layers=[layer_glow, layer_core, layer_arcs, layer_missile],
            tooltip={"text": "{name}"}
        )

# --- 6. MAIN EXECUTION ---
def main():
    ThemeManager.apply_custom_css()
    NetworkSimulation.update_metrics()
    NetworkSimulation.generate_log_entry()

    # Layout
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("🛡️ NGAO-SHIELD // OVERWATCH")
        st.caption("FEDERATED CYBER-DEFENSE GRID | v3.0.1-BETA")
    with c2:
        status = "CRITICAL" if st.session_state.attack_mode else "SECURE"
        st.markdown(f"# [{status}]")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("GRID NODES", "4", "NRB/MBA/KSM/ELD")
    m2.metric("AVG LATENCY", f"{np.random.randint(12, 28)}ms", "+2ms")
    m3.metric("PRIVACY BUDGET", "ε=0.8", "DP-SGD")
    
    with m4:
        if st.session_state.attack_mode:
            if st.button("💠 DEPLOY VACCINE"):
                st.session_state.attack_mode = False
                st.session_state.log_data = st.session_state.log_data.tail(20)
                st.rerun()
        else:
            if st.button("☢️ SIMULATE ATTACK"):
                st.session_state.attack_mode = True
                st.rerun()

    col_map, col_data = st.columns([1.5, 1])
    
    with col_map:
        st.markdown("### 📡 LIVE THREAT GEOMETRY")
        st.pydeck_chart(MapEngine.render_map())

    with col_data:
        st.markdown("### 🧬 MODEL INTEGRITY")
        
        # High Contrast Gradient Chart
        color_hex = "#ff0000" if st.session_state.attack_mode else "#00ffc8"
        chart = alt.Chart(st.session_state.log_data).mark_area(
            line={'color': color_hex},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color=color_hex, offset=0),
                       alt.GradientStop(color=color_hex, offset=1)],
                x1=1, x2=1, y1=1, y2=0
            ),
            opacity=0.6 # Higher opacity for visibility
        ).encode(
            x=alt.X('Time', axis=None),
            y=alt.Y('Integrity', scale=alt.Scale(domain=[0, 1.1]))
        ).properties(height=250)
        
        st.altair_chart(chart, use_container_width=True)

        st.markdown("### 📝 KERNEL LOGS")
        log_text = "\n".join(st.session_state.logs)
        st.code(log_text, language="bash")

    time.sleep(0.8) 
    st.rerun()

if __name__ == "__main__":
    main()