import os
import os.path as osp
import torch
import torch.nn as nn
from PIL import Image

from .models import QualityNet
from .config import config as cfg


def load_model():
    cwd = osp.dirname(__file__)
    path = osp.join(cwd, cfg.checkpoints, cfg.restore_model)
    state_dict = torch.load(path, map_location=cfg.device)
    net = QualityNet()
    net = nn.DataParallel(net)
    net.to(cfg.device)
    net.load_state_dict(state_dict)
    net.eval()
    return net

net = load_model()

def input_preprocess(im):
    assert im.mode == 'RGB'
    im = cfg.test_transform(im)
    im = im[None, ...]
    return im

        
def estimate(im: 'str | PIL.Image'):
    global net
    if type(im) == str:
        im = Image.open(im)
    im = input_preprocess(im)
    with torch.no_grad():
        score = net(im)
    score = round(score.item(), 2)
    return score