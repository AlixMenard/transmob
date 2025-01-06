#region Imports
from ultralytics import YOLO
import torch
import numpy as np
import cv2

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

import os

#endRegion

def get_cars(coco_path):
    labels = os.listdir(rf"{coco_path}/labels/train2017")
    np.random.shuffle(labels)
    cars = []
    for label in labels:
        with open(os.path.join(rf"{coco_path}/labels/train2017", label), 'r') as f:
            txt = f.read()
        txt = txt.split(" ")[0]
        if txt == "2":
            cars.append(os.path.join(rf"{coco_path}/images/train2017", label))
        if len(cars) > 50:
            break
    return cars

def get_vans(vans_path):
    images = os.listdir(rf"{vans_path}/train/images")
    np.random.shuffle(images)
    vans = []
    for label in images:
        vans.append(os.path.join(rf"{vans_path}/train/images", label))
        if len(vans) > 50:
            break
    return vans

def fight(coco_path, vans_path, onlyvans, yolo11):
    cars = get_cars(coco_path)
    vans = get_vans(vans_path)

    model = YOLO(yolo11).to(device)

    cars_confs_yolo = []
    vans_confs_yolo = []
    for car in cars:
        frame = cv2.imread(car)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        conf = model.detect(frame, classes = [2])[0].boxes.conf[0]
        cars_confs_yolo.append(conf)
    for van in vans:
        frame = cv2.imread(van)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        conf = model.detect(frame)[0].boxes.conf[0]
        vans_confs_yolo.append(conf)