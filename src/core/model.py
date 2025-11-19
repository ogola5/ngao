import torch
import torch.nn as nn
import torch.nn.functional as F

class CyberDefenseNet(nn.Module):
    """
    Deep Learning Model for detecting network anomalies.
    """
    def __init__(self, input_size: int = 4):
        super(CyberDefenseNet, self).__init__()
        self.fc1 = nn.Linear(input_size, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 2) # Binary Classification: Safe vs Attack

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)