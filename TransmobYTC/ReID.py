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
            os.chdir(cwd)
            images = [cv2.imread(f) for f in files]
        else:
            images = folder[:]
        features = [self(img) for img in images]
        feature_matrix = np.vstack(features)
        if feat2 is None:
            feature_matrix = cosine_similarity(feature_matrix)
        else:
            feature_matrix = cosine_similarity(feature_matrix, feat2)
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
    from collections import defaultdict
    model = YOLO(r"C:\Users\Utilisateur\Desktop\transmob\weights\yolo11x.pt")
    model.to("cuda")

    reid = ReId()
    t_features = None
    frame_error = [0,0]
    total_error = [0,0]
    vehicle_error = defaultdict(bool)


    cap = cv2.VideoCapture(r"C:\Users\Utilisateur\Desktop\transmob\videos\media\Fait_Aix 1_15' _piétons.mp4")
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0

    print("start video")
    while cap.isOpened() and count < total:

        ret, frame = cap.read()
        count += 1
        if not ret:
            continue

        results = model.track(frame, tracker="botsort.yaml", persist=True, verbose=False, classes = [2],
                             device=0, conf=0.1)
        try:
            ids = results[0].boxes.id.int().cpu().tolist()
        except:
            continue
        classes = results[0].boxes.cls.int().cpu().tolist()
        confs = results[0].boxes.conf.float().cpu().tolist()
        boxes = results[0].boxes.xyxy.cpu().tolist()

        features = []
        images = []
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            features.append(reid(frame[y1:y2, x1:x2])[0])
            images.append(frame[y1:y2, x1:x2])
        features = np.array(features)
        if t_features is not None:
            prox = reid.proxi_matrix(images, t_features[:, 1:])
            reid_ranks = []
            for i,id in enumerate(ids):
                if not id in t_features[:, 0]:
                    reid_ranks.append(-1)
                    continue
                temp = prox[i]
                ind = np.where(t_features[:, 0] == id)[0][0]
                value = temp[ind]
                temp = np.sort(temp)[::-1]
                rank = np.where(temp == value)[0][0]
                reid_ranks.append(rank)
        else:
            reid_ranks = []

        reid_ranks = np.array([0 if i<4 else 1 for i in reid_ranks])
        if len(reid_ranks) == 0:
            ids = np.array(ids)
            ids = ids.reshape(-1,1)
            t_features = deepcopy(features)
            t_features = np.hstack((ids, t_features))
            continue
        else:
            f_error = False
            for i,id in enumerate(ids):
                _ = vehicle_error[id]
                if reid_ranks[i] > 0:
                    f_error = True
                    total_error[0] = total_error[0] + 1
                    vehicle_error[id] = True
                total_error[1] = total_error[1] + 1
            if f_error:
                frame_error[0] = frame_error[0] + 1
            frame_error[1] = frame_error[1] + 1
        #(np.random.randint(0,9), end = "\r", flush = True)

        """for id, classe, conf, box, rank in zip(ids, classes, confs, boxes, reid_ranks):
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f'{id} ({rank})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break"""
        ids = np.array(ids)
        ids = ids.reshape(-1,1)
        t_features = deepcopy(features)
        t_features = np.hstack((ids, t_features))
        cv2.waitKey(1)
        print(f"{count}/{total}", end = "\r", flush = True)

    print(f"Total error: {total_error[0]}/{total_error[1]}")
    print(f"frame error: {frame_error[0]}/{frame_error[1]}")
    print(f"Vehicle error: {len([0 for i in vehicle_error if vehicle_error[i]])}/{len(vehicle_error)}")