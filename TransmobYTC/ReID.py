from fastreid.config import get_cfg
from fastreid.engine import DefaultPredictor
import cv2
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os
import matplotlib.pyplot as plt
import seaborn as sns
from copy import deepcopy

class ReId:
    def __init__(self, model = r"../FastReId_config/veriwild_bot_R50-ibn.pth", config = r"../FastReId_config/bagtricks_R50-ibn.yml"):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(config)
        self.cfg.MODEL.WEIGHTS = model
        self.predictor = DefaultPredictor(self.cfg)

    def __call__(self, image):
        image = image[:, :, ::-1]
        image = cv2.resize(image, tuple(self.cfg.INPUT.SIZE_TEST[::-1]), interpolation=cv2.INTER_CUBIC)
        image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))[None]
        predictions = self.predictor(image)
        return predictions

    def proxi_matrix(self, folder, feat2 = None):
        if type(folder) == str:
            cwd = os.getcwd()
            os.chdir(folder)
            files = os.listdir()
            images = [cv2.imread(f) for f in files]
        else:
            images = folder[:]
        features = [self(img) for img in images]
        feature_matrix = np.vstack(features)
        if feat2 is None:
            feature_matrix = cosine_similarity(feature_matrix)
        else:
            feature_matrix = cosine_similarity(feature_matrix, feat2)
        os.chdir(cwd)
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

if __name__ == '__main__':
    from ultralytics import YOLO
    model = YOLO(r"C:\Users\Utilisateur\Desktop\transmob\weights\yolo11x.pt")
    model.to("cuda")

    reid = ReId()
    t_features = []

    cap = cv2.VideoCapture(r"C:\Users\Utilisateur\Desktop\transmob\videos\media\Fait_Aix 1_15' _piétons.mp4")

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            continue

        results = model.track(frame, tracker="botsort.yaml", persist=True, verbose=False,
                             device=0, conf=0.1)
        try:
            ids = results[0].boxes.id.int().cpu().tolist()
        except:
            continue
        classes = results[0].boxes.cls.int().cpu().tolist()
        confs = results[0].boxes.conf.float().cpu().tolist()
        boxes = results[0].boxes.xyxy.cpu().tolist()

        features = []
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            features.append(reid(frame[y1:y2, x1:x2]))
        if t_features:
            prox = reid.proxi_matrix(features, t_features[:, 1:])
            reid_ranks = []
            for i,id in enumerate(ids):
                if not id in t_features[:, 0]:
                    continue
                temp = prox[i]
                ind = np.where(t_features[:, 0] == id)[0][0]
                value = temp[ind]
                temp = np.sort(temp)
                rank = np.where(temp == value)[0][0]
                reid_ranks.append(rank)
        else:
            reid_ranks = [-1]*len(ids)

        for id, classe, conf, box, rank in zip(ids, classes, confs, boxes, reid_ranks):
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            v = self.fleet.get(id)
            cv2.putText(frame, f'{id} ({rank})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ids = ids.reshape(-1,1)
        t_features = deepcopy(features)
        t_features = np.hstack((ids, t_features))