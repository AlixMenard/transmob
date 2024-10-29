import os
import shutil
from copy import deepcopy

os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["OPENCV_FFMPEG_READ_ATTEMPTS"] = "8192"

from .Vehicle import Fleet
from .Box import Box as vBox
from .Line import Line
import cv2

import numpy as np
from .sort import Sort
from ultralytics import YOLO
from typing import List
import time
import tkinter as tk
from datetime import datetime


# ? First try at box connection, either too slow (often) or incorrect and leaving objects unclassed
def dic_search2(dic: dict, tupl: tuple):
    margin = 5
    x1, y1, x2, y2 = tupl
    d = [-margin] * 4
    while d[3] < margin + 1:
        if (x1 + d[0], y1 + d[1], x2 + d[2], y2 + d[3]) in dic.keys():
            return dic[(x1 + d[0], y1 + d[1], x2 + d[2], y2 + d[3])]
        else:
            d[0] += 1
            for i in range(3):
                if d[i] == margin + 1:
                    d[i] = -margin
                    d[i + 1] += 1
    return None, 0


def dic_search(dic: dict, tupl: tuple):
    x1, y1, x2, y2 = tupl

    for box in dic:
        x3, y3, x4, y4 = box

        si = max(0, min(x2, x4) - max(x1, x3)) * max(0, min(y2, y4) - max(y1, y3))
        s1 = (x2 - x1) * (y2 - y1)
        s2 = (x4 - x3) * (y4 - y3)

        su = s1 + s2 - si
        r = si / su
        if r >= 0.8:
            return dic[x3, y3, x4, y4]

    return "", 0


def draw_line(frame, line, color = (255, 255, 0), thickness = 3):
    cv2.line(frame, line.start, line.end, color, thickness=thickness)
    cv2.line(frame, line.center, line.p3, color, thickness=thickness)
    cv2.putText(frame, f'{line.id}', line.end, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)


def time_5(_time):
    return float(int(_time / 300) * 300)

def time_1(_time):
    return float(int(_time / 60) * 60)


def str_time(_time):
    c_time_str = time.ctime(_time)
    c_time_str = time.strptime(c_time_str)
    c_time_str = time.strftime("%Y-%m-%d %Hh%M", c_time_str)
    return c_time_str


class Analyser:

    def __init__(self, folder, name, model="weights/yolov8n.pt", graph: bool = False, threshold: float = 0.1,
                 watch_classes=None, verbose:bool=False, frame_nb:int = 2, screenshots = False):
        if watch_classes is None:
            watch_classes = ["car", "truck", "motorbike", "bus", "bicycle", "person"]
        if verbose: print("Initialising analyser...")
        Line.nb_lines = 0
        self.name = name
        self.url = folder + "/" + name
        self.folder = folder
        self.cap = cv2.VideoCapture(self.url)
        self.threshold = threshold
        self.watch_classes = watch_classes
        self.graph = graph
        self.screenshots = screenshots
        self.mask = None
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.points: List[(int, int)] = []
        self.lines: List[Line] = []
        self.frame_nb = frame_nb
        del self.cap
        if verbose: print("Video loaded...")
        self.yolo = YOLO(model)
        if verbose: print("YOLO loaded...")
        self.tracker = Sort(max_age=50, min_hits=3, iou_threshold=0.3)
        if verbose: print("Tracker loaded...")
        self.class_labels = [
            "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
            "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird",
            "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
            "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
            "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
            "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
            "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
            "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse",
            "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
            "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
        self.watch_classes_ids = [self.class_labels.index(c) for c in self.watch_classes]
        self.fleet = Fleet()
        if verbose: print("Analyser initiated.")

    def starter(self, lines: (List[Line], List) = None, trust_time = False):
        if lines:
            self.lines = lines[0]
            self.mask = lines[1]
        self.cap = cv2.VideoCapture(self.url)
        succ, frame = self.cap.read()
        while not succ:
            succ, frame = self.cap.read()
        save_frame = deepcopy(frame)

        ret = False
        ret = self.get_start_time(trust_time)

        while 1:
            frame = deepcopy(save_frame)
            for l in self.lines:
                draw_line(frame, l)
            cv2.imshow("Line setup", frame)
            self.create_line(frame)

            self.end = time_1(self.strt + int(self.length / self.fps))

            key = cv2.waitKey(0) & 0xFF
            if not lines is None or (key == 13):
                f_name = f"{self.folder}/product/{str_time(self.strt)}-{str_time(self.end)[11:]}.jpg"
                #print(f_name)
                cv2.imwrite(f_name, frame)
                #print("saved")
                cv2.destroyAllWindows()
                del self.cap
                break
            elif key == 8:
                print("cancel")

        return ret

    def get_start_time(self, trust_time):
        global ret
        ret = False
        c_time = os.path.getmtime(self.url) - int(self.length / self.fps)
        c_time = time_1(c_time)
        if trust_time:
            self.strt = c_time
            return True
        strtime = str_time(c_time)
        root = tk.Tk()
        time_L = tk.Label(root, text=f"Heure de début de la vidéo : {strtime}")
        time_L.grid(row = 0, column = 0, columnspan = 2)
        def validate():
            ret = True
            self.strt = c_time
            root.destroy()
        val_b = tk.Button(root, text="Valider", command=validate)
        val_b.grid(row = 2, column = 0)

        date_label = tk.Label(root, text="Entrez la date et l'heure si changement :\n(yyyy-mm-dd hh:mm)")
        date_label.grid(row=1, column=0)
        date_entry = tk.Entry(root, width=20)
        date_entry.grid(row=1, column=1)
        def change():
            ret = False
            date_str = date_entry.get()
            try:
                user_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                self.strt = user_datetime.timestamp()
                root.destroy()
            except ValueError:
                date_entry.delete(0, tk.END)
        chg_b = tk.Button(root, text="Changer", command=change)
        chg_b.grid(row=2, column=1)
        root.mainloop()
        return ret

    def process(self):
        c_time = None
        self.cap = cv2.VideoCapture(self.url)
        time_last_save = saves = count = 0
        print(f"File : {self.url} - {self.fps} FPS - {int(self.length / self.fps)} seconds")

        while self.cap.isOpened():

            if self.frame_nb == 2:
                #! Double frame
                succ, frame = self.cap.read()
                succ2, frame2 = self.cap.read()
                count += 2
                if not succ:
                    #print("corrupted frame")
                    if not succ2:
                        if count >= self.length:
                            break
                        continue
                    frame = frame2
            elif self.frame_nb == 1:
                #! Single frame
                succ, frame = self.cap.read()
                count += 1
                if not succ:
                    if count >= self.length:
                        break
                    continue

            if not self.mask is None:
                frame = cv2.bitwise_and(frame, self.mask)

            detected = self.yolo(frame, stream=True, verbose=False, classes=self.watch_classes_ids, device='cpu')
            detection = np.empty((0, 5))

            class_map = {}

            for res in detected:
                for box in res.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = np.ceil((box.conf[0] * 100)) / 100
                    class_id = int(box.cls[0])
                    class_name = self.class_labels[class_id]
                    class_map[(x1, y1, x2, y2)] = (class_name, conf)

                    if class_name in self.watch_classes and conf > self.threshold:
                        entry = np.array([x1, y1, x2, y2, conf])
                        detection = np.vstack((detection, entry))

                tracked = self.tracker.update(detection)
                ids = self.fleet.ids
                for t in tracked:
                    x1, y1, x2, y2, id = map(int, t)
                    class_name, conf = dic_search(class_map, (x1, y1, x2, y2))

                    if id in ids:
                        box = vBox(x1, y1, x2 - x1, y2 - y1)
                        self.fleet.update_vehicle(id, box, class_name, conf, count)
                    else:
                        box = vBox(x1, y1, x2 - x1, y2 - y1)
                        self.fleet.add_vehicle(id, box, class_name, conf, count)

                    color = (255, 255, 0)
                    for l in self.lines:
                        x, y = box.center
                        if l.inbound(x, y):
                            crossed = l.cross(self.fleet.get(id))
                            if crossed and self.screenshots:
                                self.screen(frame, box.xyxy, id)
                            color = (255, 0, 0)

                    if self.graph:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        v = self.fleet.get(id)
                        cv2.putText(frame, f'{v.id} ({v._class})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (255, 255, 0), 2)

            self.fleet.watch_bikes()

            if cv2.waitKey(1) & 0xFF == 13:
                del self.cap
                break
            if self.graph:
                for l in self.lines:
                    draw_line(frame, l)
                cv2.imshow("Line setup", frame)

            time_last_save = count / self.fps - saves * 60
            if time_last_save > 60:
                if not c_time:
                    c_time = self.strt
                c_time_str = str_time(c_time)
                self.save(c_time_str, c_time + time_last_save, tracked)
                c_time += time_last_save
                saves += 1

        if not c_time:
            c_time = self.strt
        c_time_str = str_time(c_time)
        self.save(c_time_str, c_time + time_last_save, [])

    def save(self, c_time, e_time, tracked):

        e_time = str_time(time_1(e_time))
        method = "w" if not os.path.exists(f"{self.folder}/product/results.txt") else "a"
        with open(f"{self.folder}/product/results.txt", method) as f:
            f.write(f"@{c_time}, {e_time}, {len(self.lines)}\n")
            for l in self.lines:
                f.write(f"{l.id} : {l.counter.count()}\n")

        for l in self.lines:
            l.cleanse()
        keep_ids = []
        for t in tracked:
            _, _, _, _, id = map(int, t)
            keep_ids.append(id)
        self.fleet.cleanse(keep_ids)

    def screen(self, frame, box, id):
        x1, y1, x2, y2 = map(int, box)
        roi = frame[y1:y2, x1:x2]
        file_name = fr'{self.folder}/product/screens/{str_time(self.strt)}_{id}.jpg'
        #print(file_name)
        cv2.imwrite(file_name, roi)

    def create_line(self, frame):

        def click_event(event, x, y, _, __):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.points.append((x, y))
                if len(self.points) == 3:
                    self.lines.append(Line(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1],
                                           self.points[2][0], self.points[2][1]))
                    draw_line(frame, self.lines[-1])
                    cv2.imshow("Line setup", frame)
                    self.points = []
                    self.create_mask(frame)

        cv2.setMouseCallback("Line setup", click_event, param=frame)

        cv2.setMouseCallback("Line setup", click_event, param=frame)

    # noinspection PyTypeChecker
    def create_mask(self, frame):
        height, width = frame.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)

        (x1, y1, x2, y2)= map(int, Line.get_total_bounding_box(self.lines))
        cv2.rectangle(mask, (x1, y1), (x2, y2), color=255, thickness=cv2.FILLED)

        if len(frame.shape) == 3:
            mask = np.stack([mask] * frame.shape[2], axis=-1)
        self.mask = mask

    def get_lines(self):
        return self.lines, self.mask


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action="store", dest="file_name", default="media/Fait_Aix 1_15' _piétons.mp4")
    parser.add_argument("-g", "--graph", action="store", dest="graph_bool", default=False)
    parser.add_argument("-c", "--classes", action="store", dest="watch_classes", nargs="+",
                        default=["car", "truck", "motorbike", "bus", "bicycle", "person"])
    args = parser.parse_args()

    #os.mkdir("product")

    if args.file_name:
        An = Analyser("", args.file_name, graph=args.graph_bool, watch_classes=args.watch_classes)
        An.starter()
        An.process()
