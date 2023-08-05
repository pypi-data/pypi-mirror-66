import torch
import torchvision.transforms as T

class Config:
    # data preprocess
    input_shape = [3, 128, 128]
    train_transform = T.Compose([
        T.RandomHorizontalFlip(),
        T.ToTensor(),
        T.Normalize(mean=[0.5] * 3, std=[0.5] * 3),
    ])
    test_transform = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=[0.5] * 3, std=[0.5] * 3),
    ])

    # dataset
    train_root = '/data/WIDER_train/quality/'
    
    # training settings
    checkpoints = "checkpoints"
    restore = False
    restore_model = "last.pth"
    test_model = "checkpoints/24.pth"
    
    batch_size = 64

    epoch = 50
    optimizer = 'adam'  # ['sgd', 'adam']
    lr = 5e-4
    lr_step = 10
    lr_decay = 0.95
    weight_decay = 5e-4
 
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    pin_memory = True  # if memory is large, set it True to speed up a bit
    num_workers = 4  # dataloader

config = Config()