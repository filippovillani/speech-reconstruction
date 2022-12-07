import torch
from torch.utils.data import Dataset, DataLoader, random_split
from argparse import Namespace
import numpy as np
import os
from typing import Tuple

import config

def build_dataloaders(data_dir: str,
                      hparams: Namespace)->Tuple[DataLoader, DataLoader]:
    ds = MelSTFTDataset(data_dir)
    train_ds, val_ds = random_split(ds, [0.7, 0.3], generator=torch.Generator().manual_seed(config.SEED))
    train_dl = DataLoader(train_ds, 
                          hparams.batch_size, 
                          shuffle=True, 
                          pin_memory=True)
    val_dl = DataLoader(val_ds, 
                        hparams.batch_size, 
                        shuffle=False,
                        pin_memory=True)
    
    return train_dl, val_dl
    
class MelSTFTDataset(Dataset):
    def __init__(self, 
                 data_dir: str):
        super().__init__()
        self.data_dir = data_dir
        
        self.spectr_dir = data_dir / "spectr" 
        self.melspectr_dir = data_dir / "melspectr" 
        self.wav_dir = data_dir / "wav" 
        
        self.melspectr_list_path = [self.melspectr_dir / path for path in os.listdir(self.melspectr_dir)]
        self.spectr_list_path = [self.spectr_dir / path for path in os.listdir(self.spectr_dir)]
        self.wav_list_path = [self.wav_dir / path for path in os.listdir(self.wav_dir)]
       
    def __getitem__(self, 
                    idx):
        
        wav = torch.from_numpy(np.load(self.wav_list_path[idx]))
        melspectr = torch.from_numpy(np.load(self.melspectr_list_path[idx]))
        spectr = torch.from_numpy(np.load(self.spectr_list_path[idx]))
        
        return {'wav': wav,
                'melspectr': melspectr,
                'spectr': spectr}
        
    def __len__(self):
        return len(os.listdir(self.spectr_dir))

if __name__ == "__main__":
    _, val_dl = build_dataloaders(config.DATA_DIR, config.create_hparams())
    
    for el in val_dl:
        print(el['wav'].shape)
        print(el['spectr'].shape)
        print(el['melspectr'].shape)
        break