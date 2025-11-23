

# 🛡️ Ngao-Shield: Sovereign Federated Cyber-Defense Grid

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge&logo=github)](https://github.com/yourusername/ngao-shield)
[![Security](https://img.shields.io/badge/security-differential__privacy-blue?style=for-the-badge&logo=lock)](https://github.com/yourusername/ngao-shield)
[![Architecture](https://www.mermaidchart.com/app/projects/944e50c1-1ed4-4582-964c-ab852a859f9f/diagrams/77030829-11e3-4a46-b36c-d3d1f15fc54e/version/v0.1/edit](https://www.mermaidchart.com/app/projects/944e50c1-1ed4-4582-964c-ab852a859f9f/diagrams/77030829-11e3-4a46-b36c-d3d1f15fc54e/version/v0.1/edit)
[![Platform](https://img.shields.io/badge/deploy-docker__containers-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)](LICENSE)

> **"An attack on one is an attack on none."** — The Ngao-Shield Protocol

</div>

---

## 🚨 The Bleeding Wound: Why Kenya Needs This
**July 27th, 2023.** A massive DDoS attack hit Kenya. *eCitizen* went down. *M-Pesa* services flickered. *Kenya Power* token systems stalled. Millions of shillings were lost in hours.

The problem was not that we lacked firewalls. The problem is that our defense is **Siloed and Reactive**.

* **The Silo Effect:** When the Ministry of Health is attacked, KCB Bank remains blind to the threat until it is *their* turn to be hit.
* **Capital Flight:** We pay millions of dollars to foreign firms (Cloudflare/Akamai) to protect sovereign data. We rely on imported shields.
* **Data Sovereignty:** Government agencies cannot share logs to coordinate defense because of the **Data Protection Act (ODPC)**.

**We are waiting for 'Patient Zero' to become a pandemic.**

---

## 🛡️ The Solution: Collaborative National Immunity
**Ngao-Shield** is Kenya’s first **Federated Learning Defense Grid**. It functions like a biological immune system for the nation's digital infrastructure.

It allows different organizations (Government, Banks, Telcos) to **collaboratively train** a Cyber-Defense AI **without ever sharing a single byte of private data.**

### 💡 The "Vaccine" Protocol
1.  **Infection:** A hacker attacks **Node A (Ministry of Health)**.
2.  **Local Learning:** The Ngao-Shield Agent at Node A detects the anomaly and learns the *mathematical pattern* (gradient) locally.
3.  **Sovereign Aggregation:** Only the mathematical update is sent to the **Central Hub (NIRU)**. No IPs. No logs. No PII.
4.  **Global Immunity:** The Hub aggregates the knowledge and pushes a **"Vaccine Update"** to **Node B (KCB Bank)**.
5.  **Result:** KCB Bank blocks the attack *before* it even hits their firewall.

---

## 🏗️ System Architecture (The "Google-Class" Build)
We engineered this system using Enterprise Microservices standards, compliant with Ubuntu/Canonical code integrity checks.





## Deployment & Execution Guide
⚠️ Note on Cloud Deployment (Render/Cloud)
While Ngao-Shield is deployed to the cloud, you may experience timeouts or disconnected nodes. This is expected behavior on Free-Tier Cloud environments for the following technical reasons:
Resource Constraints: A full Federated Learning Grid (Server + Dashboard + Multiple AI Clients) requires significant RAM (2GB+). Free cloud tiers often cap at 512MB, causing the OS to kill the AI processes (OOM Kill).
Port Binding Limitations: Our architecture uses gRPC for secure model aggregation on Port 8080 and HTTP for the Dashboard on Port 8501. Most PaaS providers only expose a single port, blocking the internal communication between the Federated Server and the AI Agents.
✅ For the best "War Room" experience (as seen in the Video Demo), we recommend running the grid locally.
🚀 How to Run Locally (The "War Room" Setup)
Follow these steps to simulate the entire National Defense Grid on your laptop.
## . Prerequisites
Python 3.9 or higher installed.
Git installed.
2. Setup Environment
Open your terminal and run the following commands:
code
Bash
# #1. Clone the repository
git clone https://github.com/ogola5/ngao
cd ngao-shield

## 2. Create a Virtual Environment (Recommended)
# Windows:
python -m venv venv
venv\Scripts\activate

## Mac/Linux:
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt
3. Configuration Check
Before running, ensure your config/settings.yaml is set to Local Mode.
Open config/settings.yaml and check these lines:
code
Yaml
federated:
  ## Ensure this is localhost, NOT 'server' or a cloud URL
  server_address: "localhost:8080" 

paths:
  ## Ensure this is a relative path (no /app/ prefix)
  log_file: "logs/training_metrics.csv"
4. Launch the Grid (The 4-Terminal Method)
To visualize the system correctly, you need to open 4 separate Terminal windows/tabs to simulate the different components of the network.
🖥️ Terminal 1: The Central Hub (NIRU Server)
This is the brain. It waits for updates from ministries.
code
Bash
## Make sure venv is activated
python -m src.nodes.server
🖥️ Terminal 2: The War Room Dashboard
This is the visual interface for the judges.
code
Bash
## Make sure venv is activated
python -m streamlit run dashboard/app.py
Expected Output: Your browser will open automatically at http://localhost:8501.
🖥️ Terminal 3: Client A (Ministry of Health)
This simulates the first institution joining the grid.
code
Bash
## Make sure venv is activated
python -m src.nodes.client --node-id 1
🖥️ Terminal 4: Client B (KCB Bank)
This simulates the second institution joining the grid.
code
Bash
## Make sure venv is activated
python -m src.nodes.client --node-id 2
🎮 How to Demo the System
Once all 4 terminals are running:
Go to the Browser (Dashboard): You will see the map and the "Secure" status.
# #Click "🔴 SIMULATE ATTACK":
Watch the Map: A red missile trajectory targets the Nairobi Node.
Watch the Graph: The Model Integrity score drops (simulating a breach).
Watch Terminal 3 & 4: You will see logs showing "Training" (The agents are learning the attack pattern locally).
### Click "💠 DEPLOY VACCINE":
Watch Terminal 1: The server aggregates the math using Median logic.
Watch the Dashboard: The status turns GREEN, and the Integrity graph recovers to 100%.
Narrative: "KCB Bank has just been vaccinated against an attack that hit the Ministry of Health seconds ago."
#🔧 Troubleshooting
Error: Permission denied: logs/training_metrics.csv
Fix: Delete the logs folder manually (rm -rf logs/ or delete in file explorer) and restart Terminal 1.
Error: Address already in use
Fix: You have an old server running. Close all terminals and start fresh.
Use Arrow Up and Arrow Down to select a turn, Enter to jump to it, and Escape to return to the chat.









# Example of logs of normal flow and attack
## Attack mode
ALRT] 12:49:35 | SIGNATURE MISMATCH IN LAYER 7
[INFO] 12:49:37 | DEPLOYING MEDIAN ROBUSTNESS AGGREGATION...
[CRIT] 12:49:38 | UDP FLOOD DETECTED ON PORT 443
[INFO] 12:49:39 | DEPLOYING MEDIAN ROBUSTNESS AGGREGATION...
[CRIT] 12:49:40 | UDP FLOOD DETECTED ON PORT 443
[WARN] 12:49:42 | NODE_MOMBASA LATENCY > 600ms
[ACTN] 12:49:43 | IP 45.12.x.x BLACKLISTED VIA eBPF
[CRIT] 12:49:44 | UDP FLOOD DETECTED ON PORT 443


## Normal mode
[INFO] 12:50:24 | HEARTBEAT RECEIVED FROM MOMBASA_NODE
[INFO] 12:50:25 | FEDERATED ROUND 143 COMPLETE
[OKAY] 12:50:26 | MODEL INTEGRITY VERIFIED (SHA-256)
[INFO] 12:50:26 | DIFFERENTIAL PRIVACY NOISE ADDED (Epsilon=1.2)
[INFO] 12:50:27 | FEDERATED ROUND 146 COMPLETE
[INFO] 12:50:28 | HEARTBEAT RECEIVED FROM KISUMU_NODE
[INFO] 12:50:29 | HEARTBEAT RECEIVED FROM MOMBASA_NODE
[INFO] 12:50:30 | FEDERATED ROUND 149 COMPLETE


# 🧠 Technical Deep Dive:
 Hardened for RealityWe anticipate the criticism of "Academic AI."
 :1. Byzantine Robustness (Anti-Poisoning)Problem: What if a hacker compromises a County Government node and sends "bad math" to corrupt the national model?
 Our Fix: We replaced standard Federated Averaging with Coordinate-wise Median Aggregation.The Math:$$W_{global} = \text{Median}(W_1, W_2, ..., W_n)$$Result: Outliers and lying nodes are mathematically ignored.2. Differential Privacy (Anti-Reverse Engineering)Problem: Can a sophisticated attacker reverse-engineer the gradients to see who the bank's customers are?
 Our Fix: We implement Local Differential Privacy (LDP).Tech: Gaussian Noise is injected into the weights before they leave the client container.Result: It is mathematically impossible to reconstruct the original log data.3. Fail-Open ResilienceProblem: What if the Central Server goes offline?Our Fix: The Client Agents run in Autonomous Mode.
  If the grid disconnects, they continue to protect the local infrastructure using the last known good model.📊 The Threat Matrix: Kenyan ContextThreat TypeFrequencyNgao EffectivenessMechanismDDoS (Volumetric)
  🔴 Critical⭐⭐⭐⭐⭐Detects traffic volume anomalies instantly across the grid.SQL Injection🔴 Critical⭐⭐⭐⭐Detects abnormal character patterns in request strings.Insider Threat🟠 High⭐⭐⭐⭐Spots behavioral deviations (e.g., 3 AM massive downloads).Ransomware🟡 Medium⭐⭐⭐Identifies "Command & Control" beaconing activity.
  🚀 One-Click DeploymentWe have containerized the entire ecosystem. You do not need to install Python, PyTorch, or set up environments. It just works.Prerequisites: Docker & Docker Compose.1. Clone the Repository git clone [https://github.com/ogola5/ngao](https://github.com/ogola5/ngao)
cd ngao-shield
# 2. Launch the National GridBashdocker compose -f deployment/docker-compose.yml up --build
T
```text
ngao-shield/
├── config/                  # Configuration Management (YAML)
├── src/                     # Source Code (Type Hinted & Linted)
│   ├── core/                # The AI Engine (Autoencoders)
│   ├── nodes/               # Server/Client Logic
│   └── utils/               # Enterprise Logging & Data Gen
├── deployment/              # DevOps (Docker & Compose)
├── tests/                   # Unit Testing Suite
└── Makefile                 # Automation# ngao
