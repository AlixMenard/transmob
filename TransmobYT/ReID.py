from fastreid.config import get_cfg
from fastreid.engine import DefaultPredictor
import cv2
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os
import matplotlib.pyplot as plt
import seaborn as sns

class ReId:
    def __init__(self, model = r"../FastReId_config/veriwild_bot_R50-ibn.pth", config = r"../FastReId_config/bagtricks_R50-ibn.yml"):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(config)
        self.cfg.MODEL.WEIGHTS = model
        self.cfg.MODEL.DEVICE = "cpu"
        self.predictor = DefaultPredictor(self.cfg)

    def __call__(self, image):
        image = image[:, :, ::-1]
        image = cv2.resize(image, tuple(self.cfg.INPUT.SIZE_TEST[::-1]), interpolation=cv2.INTER_CUBIC)
        image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))[None]
        predictions = self.predictor(image)
        return predictions

    def proxi_matrix(self, folder):
        files = os.listdir(folder)
        images = [cv2.imread(f) for f in files]
        features = [self(img) for img in images]
        feature_matrix = np.vstack(features)
        feature_matrix = cosine_similarity(feature_matrix)
        return feature_matrix

    def heatmap(self, feature_matrix):
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            feature_matrix,
            annot=True,  # Show values
            fmt=".2f",  # Format float values
            cmap='coolwarm',
            cbar=True
        )
        plt.title("Proximity Matrix with Annotations")
        plt.show()