#region Imports
from ultralytics import YOLO
import torch
import numpy as np
import cv2
import json
import os

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

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
            cars.append(os.path.join(rf"{coco_path}/images/train2017", label[:-4]+".jpg"))
        if len(cars) > 50:
            break
    return cars

def get_trucks(coco_path):
    labels = os.listdir(rf"{coco_path}/labels/train2017")
    np.random.shuffle(labels)
    trucks = []
    for label in labels:
        with open(os.path.join(rf"{coco_path}/labels/train2017", label), 'r') as f:
            txt = f.read()
        txt = txt.split(" ")[0]
        if txt == "7":
            trucks.append(os.path.join(rf"{coco_path}/images/train2017", label[:-4]+".jpg"))
        if len(trucks) > 50:
            break
    return trucks

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
    trucks = get_trucks(coco_path)

    model = YOLO(yolo11).to(device)

    cars_confs_yolo = []
    vans_confs_yolo = []
    trucks_confs_yolo = []
    print("cars yolo...")
    for car in cars:
        frame = cv2.imread(car)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        confs = model(frame, classes = [2])[0].boxes.conf
        conf = confs[0] if len(confs) > 0 else 0
        cars_confs_yolo.append(conf)
    print("vans yolo...")
    for van in vans:
        frame = cv2.imread(van)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        confs = model(frame, classes = [2,7])[0].boxes.conf
        conf = confs[0] if len(confs) > 0 else 0
        vans_confs_yolo.append(conf)
    print("trucks yolo...")
    for truck in trucks:
        frame = cv2.imread(truck)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        confs = model(frame, classes = [7])[0].boxes.conf
        conf = confs[0] if len(confs) > 0 else 0
        trucks_confs_yolo.append(conf)

    model = YOLO(onlyvans).to(device)

    cars_confs_vans = []
    vans_confs_vans = []
    trucks_confs_vans = []
    print("cars vans...")
    for car in cars:
        frame = cv2.imread(car)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        confs = model(frame)[0].boxes.conf
        conf = confs[0] if len(confs) > 0 else 0
        cars_confs_vans.append(conf)
    print("vans vans...")
    for van in vans:
        frame = cv2.imread(van)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        confs = model(frame)[0].boxes.conf
        conf = confs[0] if len(confs) > 0 else 0
        vans_confs_vans.append(conf)
    print("trucks vans...")
    for truck in trucks:
        frame = cv2.imread(truck)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        confs = model(frame)[0].boxes.conf
        conf = confs[0] if len(confs) > 0 else 0
        trucks_confs_vans.append(conf)

    dic = {"cars_confs_yolo": cars_confs_yolo,
           "vans_confs_yolo": vans_confs_yolo,
           "trucks_confs_yolo": trucks_confs_yolo,
           "cars_confs_vans": cars_confs_vans,
           "vans_confs_vans": vans_confs_vans,
           "trucks_confs_vans": trucks_confs_vans}
    with open("test.json", "w") as f:
        json.dump(dic, f)

if __name__ == "__main__":
    coco_path = r"C:\Users\Utilisateur\Desktop\transmob\datasets\coco"
    van_path = r"C:\Users\Utilisateur\Desktop\transmob\datasets\vans_dataset"
    yolo = r"C:\Users\Utilisateur\Desktop\transmob\weights\yolo11x.pt"
    onlyvans = r"C:\Users\Utilisateur\Desktop\transmob\weights\vansx.pt"
    fight(coco_path, van_path, onlyvans, yolo)