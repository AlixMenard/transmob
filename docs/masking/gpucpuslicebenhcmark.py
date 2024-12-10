import torch
import time
import numpy as np
import cv2
from ultralytics import YOLO

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

file = r"C:\Users\Utilisateur\Desktop\transmob\videos\Fait_Aix 1_15' _piétons.mp4"

cpu_slice_times = []
gpu_slice_times = []
gpu_bitand_times = []


def create_mask(x1:int, y1:int, x2:int, y2:int):
    height, width = 720, 1280
    mask = np.zeros((height, width), dtype=np.uint8)

    cv2.rectangle(mask, (x1, y1), (x2, y2), color=255, thickness=cv2.FILLED)

    mask = np.stack([mask]*3, axis = -1)
    return mask

for i in range(50):
    print(f"{i}/50 : ", end ="", flush=True)
    width, height = np.random.random(size=2)
    # 1280, 720
    x1 = np.random.randint(0,1280*width)
    x2 = x1 + int(1280*width)
    y1 = np.random.randint(0,720*height)
    y2 = x1 + int(720*height)

    cap = cv2.VideoCapture(file)
    model = YOLO(r"C:\Users\Utilisateur\Desktop\transmob\weights\yolo11x.pt")
    model.to(device)
    mask = create_mask(x1,y1,x2,y2)


    print(f"GPU &", end =" | ", flush=True)
    t0 = time.time()
    count = 0
    while cap.isOpened() and count <200:
        succ, frame = cap.read()
        if not succ:
            continue
        count += 1
        #print(frame.shape, mask.shape)
        gpu_frame = torch.from_numpy(frame).cuda()
        gpu_mask = torch.from_numpy(mask).cuda()

        # Perform bitwise_and operation on GPU
        gpu_result = gpu_frame & gpu_mask

        # Transfer back to CPU
        frame = gpu_result.cpu().numpy()
        res = model.predict(frame, verbose = False)
        cv2.waitKey(0)
    gpu_bitand_times.append(time.time()-t0)

    del cap
    cap = cv2.VideoCapture(file)

    print(f"GPU slice", end=" | ", flush=True)
    t0 = time.time()
    count = 0
    while cap.isOpened() and count <100:
        succ, frame = cap.read()
        if not succ:
            continue
        count += 1
        gpu_frame = torch.from_numpy(frame).cuda()

        # Slice directly on GPU
        sliced_gpu_frame = gpu_frame[y1:y2, x1:x2]

        # Transfer back to CPU
        frame = sliced_gpu_frame.cpu().numpy()
        res = model.predict(frame, verbose = False)
        cv2.waitKey(0)
    gpu_slice_times.append(time.time()-t0)

    del cap
    cap = cv2.VideoCapture(file)

    print("CPU slice", flush=True)
    t0 = time.time()
    count = 0
    while cap.isOpened() and count <100:
        succ, frame = cap.read()
        if not succ:
            continue
        count += 1

        sliced_frame = frame[y1:y2, x1:x2]

        res = model.predict(sliced_frame, verbose = False)
        cv2.waitKey(0)
    cpu_slice_times.append(time.time()-t0)

    del cap

print(f"GPU & : {np.mean(gpu_bitand_times)}, {np.std(gpu_bitand_times)}")
print(f"GPU slice : {np.mean(gpu_slice_times)}, {np.std(gpu_slice_times)}")
print(f"CPU slice : {np.mean(cpu_slice_times)}, {np.std(cpu_slice_times)}")