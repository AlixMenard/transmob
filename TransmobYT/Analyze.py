import os
from copy import deepcopy
import json

import sahi
import torch

os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["OPENCV_FFMPEG_READ_ATTEMPTS"] = "8192"

from .Vehicle import Fleet
from .Box import Box as vBox
from .Line import Line
import cv2

import numpy as np
from ultralytics import YOLO
from typing import List
import time
import tkinter as tk
from datetime import datetime

from boxmot import BotSort
from pathlib import Path
from fastreid.config import get_cfg
import torch

from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

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


def draw_line(frame, line, mask, color = (255, 255, 0), thickness = 3):
    x1, y1, x2, y2 = mask
    strt = line.start[0]-x1, line.start[1]-y1
    end = line.end[0]-x1, line.end[1]-y1
    center = line.center[0]-x1, line.center[1]-y1
    p3 = line.p3[0]-x1, line.p3[1]-y1
    cv2.line(frame, strt, end, color, thickness=thickness)
    cv2.line(frame, center, p3, color, thickness=thickness)
    cv2.putText(frame, f'{line.id}', end, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)


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

    def __init__(self, folder, name, model="weights/yolov8n.pt", graph: bool = False, threshold: float = 0.25,
                 watch_classes=None, verbose:bool=False, frame_nb:int = 2, screenshots = False, SAHI=False):
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
        self.SAHI = SAHI
        self.mask = None
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_shape = (frame_width, frame_height)
        self.points: List[(int, int)] = []
        self.lines: List[Line] = []
        self.frame_nb = frame_nb
        del self.cap
        if verbose: print("Video loaded...")
        self.model = model

        if self.SAHI:
            self.yolo = AutoDetectionModel.from_pretrained(
                model_type='yolo11',
                model_path=os.path.join(os.getcwd(),self.model),
                confidence_threshold=0.25,
                device="cpu",
            )
        else:
            self.yolo = YOLO(model)

        if verbose: print("YOLO loaded...")
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

    def starter(self, lines: (List[Line], List) = None, trust_time = False, sp = True):
        should_pass = False
        if lines:
            self.lines = deepcopy(lines[0])
            self.lines[0].set_nb_lines(len(self.lines))
            self.mask = deepcopy(lines[1])
            should_pass = sp
        self.cap = cv2.VideoCapture(self.url)
        succ, frame = self.cap.read()
        while not succ:
            succ, frame = self.cap.read()
        save_frame = deepcopy(frame)

        ret = self.get_start_time(trust_time)

        while 1:
            frame = deepcopy(save_frame)
            for l in self.lines:
                draw_line(frame, l, (0,0,0,0))
            for p in self.points:
                cv2.circle(frame, p, radius=1, color=(0, 0, 255), thickness=3)
            self.create_line(frame)

            self.end = time_1(self.strt + int(self.length / self.fps))

            if not should_pass:
                key = cv2.waitKey(0) & 0xFF
            if (not lines is None and should_pass) or key == 13:
                f_name = f"{self.folder}/product/{str_time(self.strt)}-{str_time(self.end)[11:]}.jpg"
                #print(f_name)
                cv2.imwrite(f_name, frame)
                #print("saved")
                cv2.destroyAllWindows()
                del self.cap
                break
            elif (not lines is None and not should_pass) or key == 8:
                if self.points:
                    self.points.pop()
                elif self.lines:
                    self.lines.pop().del_line()
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
        root.title(f"{self.name}")
        time_L = tk.Label(root, text=f"Heure de début de la vidéo : {strtime}")
        time_L.grid(row = 0, column = 0, columnspan = 2)
        def validate():
            global ret
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
            global ret
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

    def init_tracker(self):
        self.tracker = BotSort(
            reid_weights=Path(),
            device=torch.device("cpu"),
            half=True,
            frame_rate=self.fps,
            with_reid=False,
            per_class=False,
            track_high_thresh=0.35,
            track_low_thresh=0.1,
            new_track_thresh=0.35,
            track_buffer=self.fps*5,
            proximity_thresh=0.65,
            cmc_method="ecc", # ECC > SIFT > SOF/ORB
        )

    def process(self, track = None):
        c_time = None
        if track is None:
            self.init_tracker()
        else:
            self.tracker = track
        self.cap = cv2.VideoCapture(self.url)
        time_last_save = saves = count = 0
        print(f"File : {self.url} - {self.fps} FPS - {int(self.length / self.fps)} seconds")

        print("start processing")
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
                x1, y1, x2, y2 = self.mask
                frame = frame[y1:y2, x1:x2]

            if self.SAHI:
                w, h, _ = frame.shape
                results = get_sliced_prediction(
                    frame,
                    self.yolo,
                    slice_height=h // 5,
                    slice_width=w // 5,
                    overlap_height_ratio=0.2,
                    overlap_width_ratio=0.2,
                    postprocess_class_agnostic=True,
                    verbose=0
                )
                results = results.object_prediction_list
                results = [r for r in results if r.category.id in self.watch_classes_ids]
                boxes = [map(round,(r.bbox.minx, r.bbox.miny, r.bbox.maxx, r.bbox.maxy)) for r in results]
                boxes = [(x1, y1, x2, y2) for (x1, y1, x2, y2) in boxes]
                classes = [r.category.id for r in results]
                confs = [r.score.value for r in results]
                dets = np.array([[*box, conf, cls] for box, conf, cls in zip(boxes, confs, classes)])
            else:
                results = self.yolo.predict(frame, verbose=False, classes=self.watch_classes_ids, device='cpu', conf = 0.25, agnostic_nms = True)
                try:
                    boxes = results[0].boxes.xyxy.cpu().tolist()
                except:
                    continue
                classes = results[0].boxes.cls.int().cpu().tolist()
                confs = results[0].boxes.conf.float().cpu().tolist()
                dets = np.array([[*box, conf, cls] for box, conf, cls in zip(boxes, confs, classes)])

            res = self.tracker.update(dets, frame) # ? [*t.xyxy, t.id, t.conf, t.cls, t.det_ind]

            fleet_ids = self.fleet.ids
            for *box, id, conf, classe, _ in res:
                id = int(id)
                class_name = self.class_labels[int(classe)]
                if not class_name in self.watch_classes:
                    continue
                x1, y1, x2, y2 = map(int, box)
                dx, dy = self.mask[:2]
                x1+=dx
                x2+=dx
                y1+=dy
                y2+=dy

                box = vBox(x1, y1, x2 - x1, y2 - y1)
                box_frame = vBox(x1-dx, y1-dy, x2 - x1, y2 - y1)
                if id in fleet_ids:
                    self.fleet.update_vehicle(id, box, class_name, conf, count)
                else:
                    self.fleet.add_vehicle(id, box, class_name, conf, count)

                color = (255, 255, 0)
                for l in self.lines:
                    x, y = box.cross_point
                    if l.inbound(x, y, self.fleet.get(id)):
                        crossed = l.cross(self.fleet.get(id))
                        if crossed and self.screenshots:
                            class_name = self.fleet.get(id)._class
                            self.screen(frame, box_frame.xyxy, id, class_name, c_time, l)
                        color = (255, 0, 0)

                if self.graph:
                    cv2.rectangle(frame, (x1-dx, y1-dy), (x2-dx, y2-dy), color, 2)
                    v = self.fleet.get(id)
                    text = f'{v.id} ({v._class})'
                    text_x = x1 - dx + 5
                    text_y = y2 - dy - 5
                    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)

            self.fleet.watch_bikes()

            if self.graph:
                if cv2.waitKey(1) & 0xFF == 13:
                    del self.cap
                    break
                for l in self.lines:
                    draw_line(frame, l, self.mask)
                cv2.imshow("Line setup", frame)

            time_last_save = count / self.fps - saves * 60
            if time_last_save > 60:
                if not c_time:
                    c_time = self.strt
                c_time_str = str_time(c_time)
                self.save(c_time_str, c_time + time_last_save, res[:, 4] if res.shape != (0,) else [])
                c_time += time_last_save
                saves += 1

        if not c_time:
            c_time = self.strt
        c_time_str = str_time(c_time)
        self.save(c_time_str, c_time + time_last_save, [])
        cv2.destroyAllWindows()
        return self.tracker
        #for l in self.lines:
        #    print(l.counter.count())
        #print(f"Done : {self.url}")

    def save(self, c_time, e_time, tracked_ids):

        e_time = str_time(time_1(e_time))
        method = "w" if not os.path.exists(f"{self.folder}/product/results.txt") else "a"
        with open(f"{self.folder}/product/results.txt", method) as f:
            f.write(f"@{c_time}, {e_time}, {len(self.lines)}\n")
            for l in self.lines:
                f.write(f"{l.id} : {l.counter.count()}\n")

        for l in self.lines:
            l.cleanse(tracked_ids)

        self.fleet.cleanse(tracked_ids)

    def screen(self, frame, box, id, class_name, c_time, line):
        nb_lignes = len(self.lines)
        if nb_lignes > 1:
            for l in self.lines:
                if not os.path.exists(fr"{self.folder}/product/screens/{l.id}"):
                    os.makedirs(fr"{self.folder}/product/screens/{l.id}")

        x1, y1, x2, y2 = map(int, box)
        roi = frame[y1:y2, x1:x2]
        if not c_time:
            c_time = self.strt
        if nb_lignes == 1:
            file_name = fr'{self.folder}/product/screens/{str_time(time_1(c_time))}_l{line.id}_{id}_{class_name}.jpg'
        else:
            file_name = fr'{self.folder}/product/screens/{line.id}/{str_time(time_1(c_time))}_{id}_{class_name}.jpg'
        #print(file_name)
        cv2.imwrite(file_name, roi)

    def create_line(self, frame):

        orig_h, orig_w = frame.shape[:2]
        display_w, display_h = 1280, 720
        scale = min(display_w / orig_w, display_h / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        display_frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

        def click_event(event, x, y, _, __):
            if event == cv2.EVENT_LBUTTONDOWN:
                real_x = int(x / scale)
                real_y = int(y / scale)
                self.points.append((real_x, real_y))

                if len(self.points) == 3:
                    dx1, dy1 = int(self.points[0][0] * scale), int(self.points[0][1] * scale)
                    dx2, dy2 = int(self.points[1][0] * scale), int(self.points[1][1] * scale)
                    dx3, dy3 = int(self.points[2][0] * scale), int(self.points[2][1] * scale)
                    temp_l = Line(dx1, dy1, dx2, dy2, dx3, dy3, mock = True)
                    self.lines.append(Line(self.points[0][0], self.points[0][1],
                                           self.points[1][0], self.points[1][1],
                                           self.points[2][0], self.points[2][1]))

                    draw_line(display_frame, temp_l, (0, 0, 0, 0))
                    del temp_l
                    self.points = []
                    self.create_mask()

                for p in self.points:
                    disp_x = int(p[0] * scale)
                    disp_y = int(p[1] * scale)
                    cv2.circle(display_frame, (disp_x, disp_y), radius=1, color=(0, 0, 255), thickness=3)
                cv2.imshow("Line setup", display_frame)

        cv2.imshow("Line setup", display_frame)
        cv2.setMouseCallback("Line setup", click_event, param=display_frame)

    # noinspection PyTypeChecker
    def create_mask(self):
        self.mask = tuple(map(int, Line.get_total_bounding_box(self.lines, self.frame_shape)))

    def get_lines(self):
        return self.lines, self.mask

    def dump(self, parent = None):
        if parent is None:
            parent = self.folder
        if not os.path.exists(rf"{parent}/cache"):
            os.makedirs(rf"{parent}/cache")
        data = {}

        data["name"] = self.name
        data["url"] = self.url
        data["folder"] = self.folder
        data["threshold"] = self.threshold
        data["watch_classes"] = self.watch_classes
        data["graph"] = self.graph
        data["screenshots"] = self.screenshots
        data["frame_nb"] = self.frame_nb
        data["model"] = self.model
        data["strt"] = self.strt
        data["end"] = self.end
        data["SAHI"] = self.SAHI

        data["lines"] = []
        for l in self.lines:
            data["lines"].append([])
            data["lines"][-1].extend(list(l.start))
            data["lines"][-1].extend(list(l.end))
            data["lines"][-1].extend(list(l.p3))
        data["mask"] = self.mask

        with open(rf"{parent}/cache/{self.name[:-4]}.json", "w") as f:
            json.dump(data, f, indent=4)
        del data

    @classmethod
    def load(cls, parent, name):
        data = json.load(open(fr"{parent}/cache/{name[:-4]}.json", "r"))
        an = cls(parent, name, model=data["model"], graph=data["graph"], threshold=data["threshold"], watch_classes=data["watch_classes"],
                 frame_nb=data["frame_nb"], screenshots=data["screenshots"], SAHI=data["SAHI"])
        an.strt = data["strt"]
        an.end = data["end"]
        lines = []
        for l in data["lines"]:
            x1, y1, x2, y2, x3, y3 = map(int, l)
            lines.append(Line(x1, y1, x2, y2, x3, y3))
        an.lines = deepcopy(lines)
        an.mask = data["mask"]

        del data, lines
        return an

if __name__ == "__main__":
    """import argparse

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
        An.process()"""
