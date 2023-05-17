import torch
import torch.nn.functional as f
import numpy as np
import os

class LenetClassifier:
    # fpath is name of model
    def __init__(self, fpath):
        self.model = torch.load(os.path.join('pytorch/models/', fpath))

    # img: 2d numpy array or regular list
    def predict(self, img):
        img_tensor = torch.Tensor(np.asarray([[img]]))

        out = self.model(img_tensor)
        probs = f.softmax(out, dim=-1).detach().numpy()
        return np.argmax(probs)
    

