import flwr as fl
import yaml
import os
import csv
import numpy as np  # <--- ADDED for Math
from typing import List, Tuple, Dict, Optional, Union
from flwr.server.client_proxy import ClientProxy
from flwr.common import FitRes, Parameters, Scalar, parameters_to_ndarrays, ndarrays_to_parameters
from src.utils.logger import setup_logger

logger = setup_logger("NGAO_SERVER")

# Load Config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

LOG_PATH = config['paths']['log_file']

class AuditStrategy(fl.server.strategy.FedAvg):
    """
    Custom Strategy that implements:
    1. ROBUST AGGREGATION (Median) -> Prevents Poisoning
    2. AUDIT LOGGING -> For Dashboard & Compliance
    """
    
    # --- NEW: ANTI-POISONING LOGIC ---
    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:

        if not results:
            return None, {}

        # 1. Convert binary parameters back to NumPy arrays
        weights_results = [
            (parameters_to_ndarrays(fit_res.parameters), fit_res.num_examples)
            for _, fit_res in results
        ]

        # 2. ROBUST AGGREGATION (The "Krum/Median" Logic)
        # Instead of calculating the Average, we calculate the MEDIAN.
        # If a hacker sends weight = 1,000,000, the Median ignores it.
        logger.info(f"🛡️ Aggregating {len(results)} updates using ROBUST MEDIAN logic.")
        
        # Extract just the weights
        weights_only = [w for w, _ in weights_results]
        
        # Calculate Median for each layer
        new_weights = [
            np.median(np.stack(layer_updates), axis=0) 
            for layer_updates in zip(*weights_only)
        ]

        return ndarrays_to_parameters(new_weights), {}

    # --- EXISTING: DASHBOARD LOGGING ---
    def aggregate_evaluate(
        self, server_round: int, results: List, failures: List
    ) -> Tuple[Optional[float], Dict]:
        
        if failures:
            logger.warning(f"⚠️ Round {server_round}: {len(failures)} failures detected.")

        aggregated_loss, aggregated_metrics = super().aggregate_evaluate(server_round, results, failures)

        if results:
            accuracies = [r.metrics["accuracy"] for _, r in results]
            avg_acc = sum(accuracies) / len(accuracies)
            logger.info(f"📈 Round {server_round} | Global Immunity: {avg_acc:.4f}")
            
            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
            file_exists = os.path.isfile(LOG_PATH)
            with open(LOG_PATH, mode='a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Round", "Accuracy"])
                writer.writerow([server_round, avg_acc])
        
        return aggregated_loss, aggregated_metrics

def start_server():
    logger.info("🛡️ Starting Ngao-Shield Central Core [ROBUST MODE]...")
    
    strategy = AuditStrategy(
        min_fit_clients=config['federated']['min_clients'],
        min_evaluate_clients=config['federated']['min_clients'],
        min_available_clients=config['federated']['min_clients'],
    )

    fl.server.start_server(
        server_address="0.0.0.0:8080", 
        config=fl.server.ServerConfig(num_rounds=config['federated']['rounds']),
        strategy=strategy,
    )

if __name__ == "__main__":
    start_server()