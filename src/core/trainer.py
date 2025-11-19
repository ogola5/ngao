import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from src.core.model import CyberDefenseNet
from typing import Tuple, Dict

def train_model(net: CyberDefenseNet, trainloader: DataLoader, epochs: int) -> float:
    """Trains the network locally and returns final loss."""
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.01, momentum=0.9)
    net.train()
    final_loss = 0.0
    
    for _ in range(epochs):
        for images, labels in trainloader:
            optimizer.zero_grad()
            loss = criterion(net(images), labels)
            loss.backward()
            optimizer.step()
            final_loss = loss.item()
    return final_loss

def test_model(net: CyberDefenseNet, testloader: DataLoader) -> Tuple[float, float]:
    """Evaluates the network locally."""
    criterion = nn.CrossEntropyLoss()
    correct, total, loss = 0, 0, 0.0
    net.eval()
    with torch.no_grad():
        for data, labels in testloader:
            outputs = net(data)
            loss += criterion(outputs, labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = correct / total if total > 0 else 0.0
    return loss, accuracy