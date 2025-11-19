import numpy as np
import pandas as pd
from typing import Tuple

def generate_synthetic_traffic(samples: int = 2000, malicious_ratio: float = 0.3, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates synthetic network traffic.
    Features: [Packet Size, Latency, Protocol ID, Request Count]
    """
    np.random.seed(seed)
    
    # Benign Traffic (Normal)
    n_benign = int(samples * (1 - malicious_ratio))
    # Normal: Medium packets, low latency
    benign = np.random.normal(loc=[500, 50, 1, 5], scale=[100, 10, 0.5, 2], size=(n_benign, 4))
    
    # Malicious Traffic (Attack)
    n_mal = samples - n_benign
    # Attack: Huge packets (DDoS) or tiny packets (Probe), High Latency
    malicious = np.random.normal(loc=[1500, 200, 1, 50], scale=[500, 50, 0.5, 10], size=(n_mal, 4))
    
    X = np.vstack((benign, malicious)).astype(np.float32)
    y = np.hstack((np.zeros(n_benign), np.ones(n_mal))).astype(np.int64)
    
    # Shuffle
    indices = np.random.permutation(len(X))
    return X[indices], y[indices]