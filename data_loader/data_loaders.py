import torch
import numpy as np
from torchvision import datasets, transforms
from base import BaseDataLoader


class MnistDataLoader(BaseDataLoader):
    def __init__(self, data_dir, batch_size, shuffle=False):
        """
        :param data_dir: Data directory
        """
        super(MnistDataLoader, self).__init__(batch_size, shuffle)
        self.data_dir = data_dir
        self.data_loader = torch.utils.data.DataLoader(
            datasets.MNIST('../data', train=True, download=True,
                           transform=transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize((0.1307,), (0.3081,))
                           ])), batch_size=256, shuffle=False)
        self.x = []
        self.y = []
        for data, target in self.data_loader:
            self.x += [i for i in data.numpy()]
            self.y += [i for i in target.numpy()]
        self.x = np.array(self.x)
        self.y = np.array(self.y)

    def __next__(self):
        batch = super(MnistDataLoader, self).__next__()
        batch = [np.array(sample) for sample in batch]
        return batch

    def _pack_data(self):
        packed = list(zip(self.x, self.y))
        return packed

    def _unpack_data(self, packed):
        unpacked = list(zip(*packed))
        unpacked = [list(item) for item in unpacked]
        return unpacked

    def _update_data(self, unpacked):
        self.x = unpacked[0]
        self.y = unpacked[1]

    def _n_samples(self):
        return len(self.x)
