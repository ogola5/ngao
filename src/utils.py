import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(client_id: int):
    """
    Loads the CSV for a specific client, normalizes it, 
    and returns PyTorch DataLoaders.
    """
    # 1. Load CSV
    path = f"data/client_{client_id}.csv"
    print(f"📥 Loading data from {path}...")
    df = pd.read_csv(path)
    
    # 2. Split Features (X) and Target (y)
    X = df.drop("is_attack", axis=1).values
    y = df["is_attack"].values
    
    # 3. Normalize (CRITICAL for Neural Networks)
    # This scales packet sizes so 2000 bytes doesn't overpower 50ms duration
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # 4. Split Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Convert to PyTorch Tensors
    train_dataset = TensorDataset(torch.tensor(X_train).float(), torch.tensor(y_train).long())
    test_dataset = TensorDataset(torch.tensor(X_test).float(), torch.tensor(y_test).long())
    
    # 6. Create Loaders
    trainloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    testloader = DataLoader(test_dataset, batch_size=32)
    
    return trainloader, testloader