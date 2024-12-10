import torch
import time
import numpy as np
import cv2
from ultralytics import YOLO

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

file = r"C:\Users\guest_l5dyhea\Desktop\transmob\videos\1x1min\2165-155327596_tiny.mp4"

cpu_slice_times = []
gpu_slice_times = []
gpu_bitand_times = []


def create_mask(x1:int, y1:int, x2:int, y2:int):
    height, width = 640, 360
    mask = np.zeros((height, width), dtype=np.uint8)

    cv2.rectangle(mask, (x1, y1), (x2, y2), color=255, thickness=cv2.FILLED)

    cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return mask

for i in range(100):
    print(f"{i}/100", end = "\r")
    width, height = np.random.random(size=2)
    # 640, 360
    x1 = np.randint(0,640*width)
    x2 = x1 + int(640*width)
    y1 = np.randint(0,360*height)
    y2 = x1 + int(360*height)

    cap = cv2.VideoCapture(file)
    model = YOLO(r"C:\Users\guest_l5dyhea\Desktop\transmob\weights\yolo11x.pt")
    model.to(device)
    mask = create_mask(x1,y1,x2,y2)

    t0 = time.time()
    while cap.isOpened():
        succ, frame = cap.read()
        if not succ:
            continue
        gpu_frame = torch.from_numpy(frame).cuda()
        gpu_mask = torch.from_numpy(mask).cuda()

        # Perform bitwise_and operation on GPU
        gpu_result = gpu_frame & gpu_mask

        # Transfer back to CPU
        frame = gpu_result.cpu().numpy()
        res = model.predict(frame)
    gpu_bitand_times.append(time.time()-t0)

    cap = cv2.VideoCapture(file)
    model = YOLO(r"C:\Users\guest_l5dyhea\Desktop\transmob\weights\yolo11x.pt")
    model.to(device)

    t0 = time.time()
    while cap.isOpened():
        succ, frame = cap.read()
        if not succ:
            continue
        gpu_frame = torch.from_numpy(frame).cuda()

        # Slice directly on GPU
        sliced_gpu_frame = gpu_frame[y1:y2, x1:x2]

        # Transfer back to CPU
        frame = sliced_gpu_frame.cpu().numpy()
        res = model.predict(frame)
    gpu_slice_times.append(time.time()-t0)

    cap = cv2.VideoCapture(file)
    model = YOLO(r"C:\Users\guest_l5dyhea\Desktop\transmob\weights\yolo11x.pt")
    model.to(device)

    t0 = time.time()
    while cap.isOpened():
        succ, frame = cap.read()
        if not succ:
            continue

        sliced_frame = frame[y1:y2, x1:x2]

        res = model.predict(sliced_frame)
    cpu_slice_times.append(time.time()-t0)