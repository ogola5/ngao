import flwr as fl
import yaml
import os
import csv
from typing import List, Tuple, Dict, Optional
from src.utils.logger import setup_logger

logger = setup_logger("NGAO_SERVER")

# Load Config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

LOG_PATH = config['paths']['log_file']

class AuditStrategy(fl.server.strategy.FedAvg):
    """
    Custom Strategy to log Global Accuracy for the Dashboard.
    """
    def aggregate_evaluate(
        self, server_round: int, results: List, failures: List
    ) -> Tuple[Optional[float], Dict]:
        
        if failures:
            logger.warning(f"⚠️ Round {server_round}: {len(failures)} failures detected.")

        # Standard aggregation
        aggregated_loss, aggregated_metrics = super().aggregate_evaluate(server_round, results, failures)

        if results:
            # specific logic to handle custom metrics from clients
            accuracies = [r.metrics["accuracy"] for _, r in results]
            avg_acc = sum(accuracies) / len(accuracies)
            logger.info(f"📈 Round {server_round} | Global Immunity: {avg_acc:.4f}")
            
            # Write to shared CSV for Dashboard
            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
            file_exists = os.path.isfile(LOG_PATH)
            with open(LOG_PATH, mode='a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Round", "Accuracy"])
                writer.writerow([server_round, avg_acc])
        
        return aggregated_loss, aggregated_metrics

def start_server():
    logger.info("🛡️ Starting Ngao-Shield Central Core...")
    
    strategy = AuditStrategy(
        min_fit_clients=config['federated']['min_clients'],
        min_evaluate_clients=config['federated']['min_clients'],
        min_available_clients=config['federated']['min_clients'],
    )

    # FORCE 0.0.0.0 here so the container listens on all interfaces
    fl.server.start_server(
        server_address="0.0.0.0:8080", 
        config=fl.server.ServerConfig(num_rounds=config['federated']['rounds']),
        strategy=strategy,
    )

if __name__ == "__main__":
    start_server()