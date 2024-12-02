from ultralytics import YOLO
import os

if __name__ == "__main__":
    model = YOLO(r"../weights/yolo11m.pt")
    os.chdir(os.getcwd())
    model.train(data=r"data.yaml", epochs=50, imgsz=640, device=0, batch=0.8)