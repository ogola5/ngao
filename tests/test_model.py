import unittest
import torch
from src.core.model import CyberDefenseNet

class TestCyberDefenseNet(unittest.TestCase):
    def test_model_structure(self):
        net = CyberDefenseNet()
        self.assertIsInstance(net, torch.nn.Module)
        
    def test_forward_pass(self):
        net = CyberDefenseNet()
        # Mock input: batch of 1, 4 features
        input_tensor = torch.randn(1, 4)
        output = net(input_tensor)
        # Output should be batch of 1, 2 classes
        self.assertEqual(output.shape, (1, 2))

if __name__ == '__main__':
    unittest.main()