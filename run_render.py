import subprocess
import time
import os
import sys

# 1. SETUP LOGGING DIRECTORY
if not os.path.exists('logs'):
    os.makedirs('logs')

print("🚀 STARTING NGAO-SHIELD CLOUD DEPLOYMENT...")

# 2. START THE CENTRAL SERVER (Background)
# We use sys.executable to ensure we use the same python environment
print("🛡️ Launching Central Hub...")
server = subprocess.Popen([sys.executable, "-m", "src.nodes.server"])

# Wait a moment for server to initialize
time.sleep(5)

# 3. START THE CLIENTS (Background)
print("🏥 Launching Ministry Node...")
client1 = subprocess.Popen([sys.executable, "-m", "src.nodes.client", "--node-id", "1"])

print("🏦 Launching Bank Node...")
client2 = subprocess.Popen([sys.executable, "-m", "src.nodes.client", "--node-id", "2"])

# 4. START THE DASHBOARD (Foreground - This keeps the container alive)
# Render provides the port in the environment variable 'PORT'
port = os.environ.get("PORT", "8501")
print(f"📊 Launching War Room on Port {port}...")

# We run Streamlit as the main blocking process
try:
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "dashboard/app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ], check=True)
except KeyboardInterrupt:
    # Cleanup if stopped
    server.kill()
    client1.kill()
    client2.kill()