# 🛡️ Ngao-Shield: Sovereign Federated Cyber-Defense Grid

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Security](https://img.shields.io/badge/security-differential__privacy-blue)
![Architecture](https://img.shields.io/badge/architecture-federated__learning-purple)
![Platform](https://img.shields.io/badge/platform-docker-2496ED)

> **"An attack on one is an attack on none."**

---

## 🚨 The Bleeding Wound (The Problem)
**Kenya’s critical infrastructure is fighting a lonely war.** 

When hackers attack a government service (like **eCitizen**), the **Ministry of Energy** and **KCB Bank** remain blind to the threat until it is their turn to be hit. 

Currently, our cyber defense is **Siloed and Reactive**.
1.  **The Silo Effect:** Ministries cannot share logs due to the Data Protection Act (ODPC) and national security compartmentalization.
2.  **The Domino Effect:** Attackers use the same key to open 50 doors because the doors don't talk to each other.
3.  **The Lag:** By the time a signature is identified and a patch issued, the damage is done.

**We are waiting for 'Patient Zero' to become a pandemic.**

---

## 🛡️ The Solution: Ngao-Shield
**Ngao-Shield** is Kenya’s first **Federated Learning Defense Grid**. It functions like a biological immune system for the nation's digital infrastructure.

It allows different organizations (Government, Banks, Telcos) to **collaboratively train** a Cyber-Defense AI **without ever sharing a single byte of private data.**

### 💡 How It Works (The "Vaccine" Protocol)
1.  **Infection:** A hacker attacks **Node A (Ministry of Health)**.
2.  **Local Learning:** The Ngao-Shield Agent at Node A detects the anomaly and learns the *mathematical pattern* (gradient) of the attack locally.
3.  **Sovereign Aggregation:** Only the mathematical update (the "knowledge") is sent to the **Central Hub (NIRU)**. No IPs, no logs, no PII.
4.  **Global Immunity:** The Hub aggregates the knowledge and pushes a "Vaccine Update" to **Node B (KCB Bank)**.
5.  **Result:** KCB Bank blocks the attack *before* it even hits their firewall.

---

## 🏗️ Technical Architecture (Google-Class Engineering)

We have built this system using **Enterprise Microservices** standards, ready for Ubuntu/Canonical review.

| Component | Tech Stack | Responsibility |
| :--- | :--- | :--- |
| **The Brain (Server)** | `Python`, `Flower (flwr)`, `PyTorch` | Fault-tolerant aggregation of defense models. |
| **The Agents (Clients)** | `Docker`, `NumPy` | Runs on-premise at Ministries. Trains locally. |
| **The Dashboard** | `Streamlit`, `Pandas` | Real-time visualization of national threat levels. |
| **Security** | `Differential Privacy` | Ensures mathematical updates cannot be reverse-engineered. |

### 📂 Project Structure
The codebase follows strict **Canonical/Ubuntu** repository standards:

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
