import torch
import torch.nn as nn

from siriusbackbone import mobilenet_v2


class QualityNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = mobilenet_v2()
        self.classify = nn.Linear(1280, 1)
    
    def forward(self, x):
        x = self.backbone(x)[0]
        x = torch.mean(x, dim=(2, 3))
        x = self.classify(x)
        return x


if __name__ == '__main__':
    x = torch.randn(1, 3, 128, 128)
    net = QualityNet()
    with torch.no_grad():
        res = net(x)
    print(res.shape)