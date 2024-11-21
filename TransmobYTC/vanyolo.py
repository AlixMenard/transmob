from ultralytics import YOLO
import os

if __name__ == "__main__":
    model = YOLO(r"../weights/yolo11x.pt")
    os.chdir(os.getcwd())
    model.train(data=r"coco.yaml", epochs=50, imgsz=640, device=0, batch=0.8)