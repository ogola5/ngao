import argparse
import torch
import flwr as fl
import yaml
from torch.utils.data import DataLoader, TensorDataset
from src.core.model import CyberDefenseNet
from src.core.trainer import train_model, test_model
from src.utils.data_gen import generate_synthetic_traffic
from src.utils.logger import setup_logger

logger = setup_logger("NGAO_CLIENT")

with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

class NgaoClient(fl.client.NumPyClient):
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.net = CyberDefenseNet()
        logger.info(f"🔒 Initializing Secure Node {node_id}")
        
        # Generate local data (Simulation)
        X, y = generate_synthetic_traffic(seed=node_id) # Different seed per client
        
        # Convert to PyTorch
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
        loss = train_model(self.net, self.trainloader, epochs=1)
        logger.info(f"✅ Training Complete on Node {self.node_id}")
        return self.get_parameters(config={}), len(self.trainloader.dataset), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy = test_model(self.net, self.testloader)
        logger.info(f"📊 Node {self.node_id} Accuracy: {accuracy:.4f}")
        return float(loss), len(self.testloader.dataset), {"accuracy": float(accuracy)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-id", type=int, required=True, help="Unique ID for the ministry/bank")
    args = parser.parse_args()
    
    client = NgaoClient(args.node_id)
    fl.client.start_client(
        server_address=config['federated']['server_address'], 
        client=client.to_client()
    )