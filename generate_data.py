import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=5000, client_id=1):
    np.random.seed(42 + client_id) 
    
    # Generate Normal Traffic
    n_normal = int(num_samples * 0.8)
    normal_data = {
        # Packet size varies widely
        "packet_size": np.random.normal(800, 300, n_normal), 
        # Duration is fast
        "duration": np.random.normal(50, 20, n_normal),
        "protocol": np.random.randint(0, 2, n_normal),
        "login_attempts": np.random.poisson(1, n_normal),
        "is_attack": np.zeros(n_normal)
    }
    
    # Generate Attack Traffic (Make it trickier!)
    n_attack = num_samples - n_normal
    attack_data = {
        # Attack packets now look similar to large normal packets
        "packet_size": np.random.normal(1000, 400, n_attack), 
        # Attacks are slightly slower, but overlap with normal
        "duration": np.random.normal(80, 30, n_attack),      
        "protocol": np.random.randint(0, 2, n_attack),
        # Attackers try to hide login attempts
        "login_attempts": np.random.poisson(2, n_attack),     
        "is_attack": np.ones(n_attack)
    }
    
    df_normal = pd.DataFrame(normal_data)
    df_attack = pd.DataFrame(attack_data)
    
    # Shuffle
    df = pd.concat([df_normal, df_attack]).sample(frac=1).reset_index(drop=True)
    
    # Cleanup: No negative numbers
    df[df < 0] = 0
    
    if not os.path.exists("data"):
        os.makedirs("data")
        
    filename = f"data/client_{client_id}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Generated HARDER data for {filename}")

if __name__ == "__main__":
    generate_synthetic_data(client_id=1)
    generate_synthetic_data(client_id=2)
    generate_synthetic_data(client_id=3)