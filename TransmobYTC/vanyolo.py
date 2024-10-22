from ultralytics import YOLO
import os

model = YOLO(r"../weights/yolo11n.pt")
os.chdir(os.getcwd())
model.train(data="coco.yaml", epochs=100, imgsz=736, device=0, batch=0.8)