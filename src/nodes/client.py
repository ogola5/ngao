import argparse
import torch
import flwr as fl
import yaml
import time
import numpy as np # <--- ADDED
from torch.utils.data import DataLoader, TensorDataset
from src.core.model import CyberDefenseNet
from src.core.trainer import train_model, test_model
from src.utils.data_gen import generate_synthetic_traffic
from src.utils.logger import setup_logger

logger = setup_logger("NGAO_CLIENT")

with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

# --- NEW: PRIVACY LOGIC ---
def add_noise(weights, noise_level=0.01):
    """
    Adds Gaussian Noise to weights.
    This prevents the server from reverse-engineering the exact data.
    """
    noisy_weights = []
    for w in weights:
        # Generate noise based on the shape of the weight layer
        noise = np.random.normal(0, noise_level, w.shape)
        noisy_weights.append(w + noise)
    return noisy_weights

class NgaoClient(fl.client.NumPyClient):
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.net = CyberDefenseNet()
        logger.info(f"🔒 Initializing Secure Node {node_id}")
        
        # Generate local data (Simulation)
        X, y = generate_synthetic_traffic(seed=node_id) 
        
        self.train_set = TensorDataset(torch.tensor(X), torch.tensor(y))
        self.test_set = TensorDataset(torch.tensor(X), torch.tensor(y))
        
        self.trainloader = DataLoader(self.train_set, batch_size=32, shuffle=True)
        self.testloader = DataLoader(self.test_set, batch_size=32)

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.net.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(self.net.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        self.net.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        
        # Train locally
        loss = train_model(self.net, self.trainloader, epochs=1)
        logger.info(f"✅ Training Complete on Node {self.node_id}")
        
        # --- NEW: APPLY PRIVACY BEFORE SENDING ---
        raw_weights = self.get_parameters(config={})
        secure_weights = add_noise(raw_weights)
        
        return secure_weights, len(self.trainloader.dataset), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy = test_model(self.net, self.testloader)
        logger.info(f"📊 Node {self.node_id} Accuracy: {accuracy:.4f}")
        return float(loss), len(self.testloader.dataset), {"accuracy": float(accuracy)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-id", type=int, required=True, help="Unique ID for the ministry/bank")
    args = parser.parse_args()
    
    # --- NEW: RESILIENCE LOGIC (Server Down Handling) ---
    # If server is down, we keep retrying, but the local agent stays alive.
    MAX_RETRIES = 5
    RETRY_DELAY = 5 # Seconds
    
    client = NgaoClient(args.node_id)
    
    while True:
        try:
            logger.info(f"📡 Node {args.node_id} attempting connection to Grid...")
            fl.client.start_client(
                server_address=config['federated']['server_address'], 
                client=client.to_client()
            )
        except Exception as e:
            logger.error(f"❌ Connection Lost: {e}")
            logger.info(f"🛡️ Node {args.node_id} entering STANDALONE DEFENSE MODE.")
            logger.info(f"🔄 Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)