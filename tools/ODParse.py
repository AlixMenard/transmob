import json
import pprint
from datetime import *
from typing import List
import ast
import csv
import tkinter as tk

from copy import deepcopy

import numpy as np
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import shutil

from torch.distributions import Pareto

from fastreid.config import get_cfg
from fastreid.engine import DefaultPredictor
import cv2
import torch
from scipy.spatial.distance import cdist
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
from torchvision import transforms

class VehicleMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Matching Validation")

        def on_close():
            self.root.destroy()
            sys.exit()  # Ensure the program fully exits
        self.root.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event

        self.result = None
        self.selected_index = tk.IntVar(value=-1)  # Index of selected match (-1 for skip)

        # Left (entering vehicle) display
        self.left_image_label = tk.Label(self.root, text="Entering Vehicle")
        self.left_image_label.grid(row=0, column=0, padx=10, pady=10)

        self.left_path_label = tk.Label(self.root)
        self.left_path_label.grid(row=1, column=0, padx=10, pady=5)

        self.left_short_label = tk.Label(self.root)
        self.left_short_label.grid(row=2, column=0, padx=10, pady=5)

        # Right side (top 10 exiting vehicles)
        self.matches_frame = tk.Frame(self.root)
        self.matches_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10)

        self.match_buttons = []
        self.match_images = []
        for i in range(12):
            frame = tk.Frame(self.matches_frame, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=i // 4, column=i % 4, padx=5, pady=5)

            label = tk.Label(frame)
            label.pack()

            info_label = tk.Label(frame)
            info_label.pack()

            button = tk.Button(frame, text=f"Select #{i+1}", command=lambda idx=i: self.select_match(idx))
            button.pack(pady=2)

            self.match_buttons.append((label, info_label, button))

        # Skip button
        self.skip_button = tk.Button(self.root, text="🚫 Skip", command=self.skip_match, bg="gray", fg="white")
        self.skip_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.root.withdraw()  # Hide initially

    def show_images(self, enter_vehicle, top_matches):
        """Display entering vehicle and top 10 exiting vehicles for user selection."""
        self.root.deiconify()

        # Display entering vehicle
        enter_image = cv2.imread(enter_vehicle.path)
        enter_image = Image.fromarray(cv2.cvtColor(enter_image, cv2.COLOR_BGR2RGB)).resize((200, 150))
        self.enter_photo = ImageTk.PhotoImage(enter_image)
        self.left_image_label.config(image=self.enter_photo)
        self.left_path_label.config(text=enter_vehicle.path)
        self.left_short_label.config(text=f"ID: {enter_vehicle.short['id']} | Time: {enter_vehicle.short['time']} | Line: {enter_vehicle.short['line']}")

        # Display top matches
        for i, (candidate_exit_vehicle, distance) in enumerate(top_matches):
            exit_image = cv2.imread(candidate_exit_vehicle.path)
            exit_image = Image.fromarray(cv2.cvtColor(exit_image, cv2.COLOR_BGR2RGB)).resize((200, 150))
            photo = ImageTk.PhotoImage(exit_image)
            self.match_images.append(photo)

            label, info_label, _ = self.match_buttons[i]
            label.config(image=photo)
            info_label.config(text=f"ID: {candidate_exit_vehicle.short['id']} | Time: {candidate_exit_vehicle.short['time']} | Line: {candidate_exit_vehicle.short['line']}\nDistance: {distance:.4f}")

        # Hide unused slots if fewer than 10 matches
        for j in range(len(top_matches), 12):
            label, info_label, _ = self.match_buttons[j]
            label.config(image="")
            info_label.config(text="No Match")

        self.selected_index.set(-1)
        self.root.wait_variable(self.selected_index)
        self.root.withdraw()

    def select_match(self, index):
        self.result = index
        self.selected_index.set(index)

    def skip_match(self):
        self.result = -1
        self.selected_index.set(-1)

    def get_result(self):
        return self.result

def resize_with_padding(image, target_size):
    h, w = image.shape[:2]
    scale = min(target_size[1] / h, target_size[0] / w)
    new_w, new_h = int(w * scale), int(h * scale)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    padded = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)

    top = (target_size[1] - new_h) // 2
    left = (target_size[0] - new_w) // 2
    padded[top:top + new_h, left:left + new_w] = resized
    return padded

import numpy as np
from scipy.spatial.distance import cdist

def get_top_matches(enter_vehicle, exit_vehicles, top_k=12, lambda_id=0.1, max_id=1000):
    if not exit_vehicles:
        return []

    # 1. Compute feature distances (cosine)
    exit_features = np.vstack([v.features for v in exit_vehicles])
    feature_distances = cdist(enter_vehicle.features.reshape(1, -1), exit_features, metric='cosine')[0]

    # 2. Compute ID proximity penalty
    id_differences = np.array([abs(enter_vehicle.id - v.id) for v in exit_vehicles])
    id_penalty = lambda_id * (id_differences / max_id)


    # 3. Combine distances
    combined_distances = feature_distances + id_penalty
    combined_distances = np.array([(d * 2) if enter_vehicle.short["line"] == exit_vehicles[i].short["line"] else d for i, d in
                           enumerate(combined_distances)])
    combined_distances = np.array(
        [0 if enter_vehicle.id == exit_vehicles[i].id else d for i, d in
         enumerate(combined_distances)])

    # 4. Get top matches based on combined distances
    top_indices = np.argsort(combined_distances)[:top_k]
    return [(exit_vehicles[i], combined_distances[i]) for i in top_indices]


def match_with_user_validation(vehicle_paths, root, top_k=12, max_id=1000):
    matcher_gui = VehicleMatcherGUI(root)
    match_list = []
    selected_distances = []
    skipped_distances = []

    for enter_idx, enter_list in enumerate(vehicle_paths):
        enter_vehicles = [v for v in enter_list if v.sens == 0]

        for enter_vehicle in enter_vehicles:
            exit_candidates = [
                (exit_idx, exit_vehicle)
                for exit_idx, exit_list in enumerate(vehicle_paths)
                for exit_vehicle in exit_list
                if exit_vehicle.sens == 1 and exit_vehicle.id >= enter_vehicle.id
            ]

            if not exit_candidates:
                continue

            exit_vehicles = [ev for _, ev in exit_candidates]
            top_matches = get_top_matches(enter_vehicle, exit_vehicles, top_k=top_k, max_id=max_id)

            # Automatic acceptance if criteria met
            if len(selected_distances) >= 10:
                mean_distance = np.mean(selected_distances)
                std_distance = np.std(selected_distances)
                auto_accept_threshold = mean_distance - 3 * std_distance

                best_match, best_distance = top_matches[0]
                if best_distance < auto_accept_threshold:
                    enter_list.remove(enter_vehicle)
                    exit_idx = next(idx for idx, ev in exit_candidates if ev == best_match)
                    vehicle_paths[exit_idx].remove(best_match)
                    match_list.append((enter_idx, exit_idx, best_match))
                    selected_distances.append(best_distance)
                    print(f"✅ Auto-accepted: V1 {enter_vehicle.short} - V2 {best_match.short}")
                    continue
            if len(skipped_distances) >= 10:
                mean_skipped = np.mean(skipped_distances)
                std_skipped = np.std(skipped_distances)
                auto_reject_threshold = mean_skipped + 2 * std_skipped

                best_match, best_distance = top_matches[0]
                if best_distance > auto_reject_threshold:
                    skipped_distances.extend([distance for _, distance in top_matches])
                    print(f"🚫 Auto-rejected: Distance {best_distance:.4f} > {auto_reject_threshold:.4f}")
                    continue

            matcher_gui.show_images(enter_vehicle, top_matches)
            selected_index = matcher_gui.get_result()

            if selected_index != -1:  # User selected a match
                candidate_exit_vehicle, distance = top_matches[selected_index]
                enter_list.remove(enter_vehicle)
                exit_idx = next(idx for idx, ev in exit_candidates if ev == candidate_exit_vehicle)
                vehicle_paths[exit_idx].remove(candidate_exit_vehicle)
                match_list.append((enter_idx, exit_idx, candidate_exit_vehicle))
                selected_distances.append(distance)
            else:
                skipped_distances.extend([distance for _, distance in top_matches])

    return match_list

class Parser:
    def __init__(self, path, conglo=True, save_path=None):
        self.timelapse = None
        if save_path is None:
            self.save_path = path
        else:
            self.save_path = save_path
        self.path = path
        self.conglo = conglo

        self.screens_folders = []
        for dirpath, dirnames, _ in os.walk(self.path):
            if "screens" in dirnames:
                self.screens_folders.append(os.path.join(dirpath, "screens"))
        self.line_nb = len(os.listdir(self.screens_folders[0]))

    def parse(self, root):

        for widget in root.winfo_children():
            widget.destroy()

        screens_folders = self.screens_folders

        line_nb = self.line_nb

        max_id = 0
        vehicle_paths = [[] for _ in range(line_nb)]
        for screens_folder in screens_folders:
            line_folders = os.listdir(screens_folder)
            for line_folder in line_folders:
                line_id = int(line_folder)
                for vehicle_path in os.listdir(os.path.join(screens_folder, line_folder)):
                    v_param = vehicle_path.split("_") #2025-02-19 11h11_1_s1_car.jpg
                    t = v_param[0]
                    id = int(v_param[1])
                    sens = int(v_param[2][1:])
                    type = v_param[3][:-4]
                    p = os.path.join(screens_folder, line_folder, vehicle_path)
                    v = Vehicle(id, type, t, p, sens)
                    max_id = max(max_id, id)
                    vehicle_paths[line_id].append(v)

        start = min((vehicle for vlist in vehicle_paths for vehicle in vlist), key=lambda v: v.time)
        end = max((vehicle for vlist in vehicle_paths for vehicle in vlist), key=lambda v: v.time)

        od_mat = OD(line_nb)

        vehicle_exit_map = {}
        for exit_line in range(line_nb):
            for v in vehicle_paths[exit_line]:
                if v.sens == 1:  # exiting vehicles
                    vehicle_exit_map.setdefault(v.id, set()).add(exit_line)

        for enter in range(line_nb):
            enter_vehicles = [v for v in vehicle_paths[enter] if v.sens == 0]

            found = []
            for enter_vehicle in enter_vehicles:
                # Check if vehicle exits through exactly one line
                if vehicle_exit_map.get(enter_vehicle.id) and len(vehicle_exit_map[enter_vehicle.id]) == 1:
                    exit_line = next(iter(vehicle_exit_map[enter_vehicle.id]))  # get the single exit line
                    od_mat.directions[enter][exit_line].append(enter_vehicle)
                    found.append(enter_vehicle.id)

            vehicle_paths[enter] = [v for v in vehicle_paths[enter] if v.id not in found]
            for exit_line in range(line_nb):
                vehicle_paths[exit_line] = [v for v in vehicle_paths[exit_line] if v.id not in found]

        unmatched = [len(l) for l in vehicle_paths]
        #uids = {v.id for l in vehicle_paths for v in l}
        print(f"{unmatched} left unmatched, processing with ReId.", end = " ", flush = True)

        cfg = get_cfg()
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])
        cfg.merge_from_file(r"FastReId_config/bagtricks_R50-ibn.yml")
        cfg.MODEL.WEIGHTS = "FastReId_config/veriwild_bot_resnet50.pt"
        cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        predictor = DefaultPredictor(cfg)
        for path in vehicle_paths:
            for vehicle in path:
                try:
                    image = cv2.imread(vehicle.path)[:, :, ::-1]
                except:
                    input(vehicle.path)
                image = resize_with_padding(image, cfg.INPUT.SIZE_TEST[::-1])
                image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1)) / 255.0
                image = normalize(image).unsqueeze(0).to(cfg.MODEL.DEVICE)
                vehicle.features = predictor(image)
                del image
        print("Matching...", flush = True)
        id_matched = match_with_user_validation(vehicle_paths, root, top_k=12, max_id=max_id)
        print(f"{len(id_matched)} hand made matches.")
        for enter_id, exit_id, vehicle in id_matched:
            od_mat.directions[enter_id][exit_id].append(vehicle)



        #for l in vehicle_paths:
        #    print([v.path for v in l])
        unmatched = [len(l) for l in vehicle_paths]
        unmatched_ent = [len([v for v in l if v.sens==0]) for l in vehicle_paths]
        unmatched_exit = [len([v for v in l if v.sens==1]) for l in vehicle_paths]
        print(f"{unmatched} left unmatched.")
        print(f"{unmatched_ent} entering.")
        print(f"{unmatched_exit} exiting.")
        print(od_mat)
        if os.path.exists(fr"{self.path}/unmatched"):
            shutil.rmtree(fr"{self.path}/unmatched")
        os.mkdir(fr"{self.path}/unmatched")
        os.mkdir(fr"{self.path}/unmatched/enter")
        os.mkdir(fr"{self.path}/unmatched/exit")
        unmatched_ent = [(i, a) for i, l in enumerate(vehicle_paths) for a in l if a.sens == 0]
        unmatched_exit = [(i, a) for i, l in enumerate(vehicle_paths) for a in l if a.sens == 1]

        for line_id, vehicle in unmatched_ent:
            shutil.copyfile(vehicle.path, fr"{self.path}/unmatched/enter/l{line_id}_{vehicle.short['name']}")
        for line_id, vehicle in unmatched_exit:
            shutil.copyfile(vehicle.path, fr"{self.path}/unmatched/exit/l{line_id}_{vehicle.short['name']}")

        self.parsed = od_mat

    def make_csv(self):
        Quarter._conglo = self.conglo
        Quarter._instances = {}
        for i in range(self.line_nb):
            for j in range(self.line_nb):
                for v in self.parsed.directions[i][j]:
                    q = Quarter.get_quarter_for_time(i, j, v.time)
                    q.add_vehicle(v)

        columns = ["date", "time", "enter", "exit"]
        if self.conglo:
            columns += ["car", "truck", "bus", "motorbike", "bicycle", "person", "scooter"]
        else:
            columns += ["car", "van", "truck", "bus", "motorbike", "bicycle", "person", "scooter"]

        with open(rf"{self.path}/dir1.csv", "wt", newline="") as fp:
            writer = csv.writer(fp, delimiter=";")
            writer.writerow(columns)
            for q in Quarter._instances.values():
                date = q.time_start.strftime("%Y-%m-%d")
                hs = q.time_start.strftime("%Hh%M")
                he = q.time_end.strftime("%Hh%M")
                row = [date, f"{hs}-{he}", q.enter, q.exit] + q.count()
                writer.writerow(row)


        q_mats = Quarter.matrices()
        times = [t for t in q_mats.keys() if t != "HP"]
        times.sort()
        with open(rf"{self.path}/dir2.csv", "wt", newline="") as fp:
            writer = csv.writer(fp, delimiter=";")
            for t in times:
                row = [t.strftime("%Hh%M")]
                for l in range(Quarter.lines()):
                    row += [l,"_","_","_","_"]
                writer.writerow(row)

                row = ["Entrant / Sortant"]
                for l in range(Quarter.lines()):
                    row += ["VL", "PL", "Bus", "M", "Velo"]
                writer.writerow(row)

                for i in range(Quarter.lines()):
                    row = [i]
                    for j in range(Quarter.lines()):
                        row += list(q_mats[t][i, j]) #! dim of q_mats[t] ?
                    writer.writerow(row)

            row = ["HP"]
            for l in range(Quarter.lines()):
                row += [l,"_","_","_","_"]
            writer.writerow(row)

            row = ["Entrant / Sortant"]
            for l in range(Quarter.lines()):
                row += ["VL", "PL", "Bus", "M", "Velo"]
            writer.writerow(row)

            for i in range(Quarter.lines()):
                row = [i]
                for j in range(Quarter.lines()):
                    row += list(q_mats["HP"][i, j])
                writer.writerow(row)


class OD:
    def __init__(self, line_nb:int):
        self.line_nb = line_nb
        self.directions = np.empty(shape=(line_nb, line_nb), dtype=object)
        for i in range(line_nb):
            for j in range(line_nb):
                self.directions[i, j] = []

    def __repr__(self):
        rep = np.empty(shape=(self.line_nb, self.line_nb), dtype=int)
        for i in range(self.line_nb):
            for j in range(self.line_nb):
                rep[i, j] = len(self.directions[i, j])
        return str(rep)

from datetime import datetime, timedelta

class Quarter:
    _instances = {}
    _conglo = True

    def __init__(self, enter: int, exit: int, time_start: datetime, conglo: bool = True):
        self.enter = enter
        self.exit = exit
        self.time_start = time_start
        self.time_end = time_start + timedelta(minutes=15)
        self.conglo = conglo
        self.vehicles = []
        Quarter._instances[(enter, exit, time_start)] = self  # Store with tuple key

    @classmethod
    def get_quarter_for_time(cls, enter: int, exit: int, time: datetime):
        # Align the time to the start of the corresponding quarter
        quarter_start = time.replace(minute=(time.minute // 15) * 15, second=0, microsecond=0)
        key = (enter, exit, quarter_start)

        # Return the existing quarter or create a new one if not found
        return cls._instances.get(key) or cls(enter, exit, quarter_start, cls._conglo)

    def add_vehicle(self, vehicle):
        if self.conglo and vehicle.type == "van":
            vehicle.type = "car"
        self.vehicles.append(vehicle)

    def count(self):
        if self.conglo:
            columns = ["car", "truck", "bus", "motorbike", "bicycle", "person", "scooter"]
        else:
            columns = ["car", "van", "truck", "bus", "motorbike", "bicycle", "person", "scooter"]

        results = []
        for col in columns:
            results.append(0)
            for vehicle in self.vehicles:
                if vehicle.type == col:
                    results[-1] += 1
        return results

    @classmethod
    def grouped(cls):
        times = set(x[2] for x in cls._instances.keys())
        return {time: [q for key, q in cls._instances.items() if key[2] == time] for time in times}

    @classmethod
    def lines(cls):
        return max([max(k[0], k[1]) for k in cls._instances.keys()], default=0)+1

    @classmethod
    def matrices(cls):
        matrices = {}
        affluence = []
        times = cls.grouped()
        lines_nb = cls.lines()

        for time in times:

            od_temp = np.zeros((lines_nb, lines_nb), dtype=object)
            for i in range(lines_nb):
                for j in range(lines_nb):
                    od_temp[i,j] = np.array([0] * 5)


            for q in times[time]:
                columns = q.count()
                if len(columns) == 8:
                    columns[0] += columns.pop(1)
                columns = columns[:5]
                for i in range(5):
                    od_temp[q.enter, q.exit][i] += columns[i]
            matrices[time] = deepcopy(od_temp)
            affluence.append((time, od_temp.sum()))

        affluence.sort(key=lambda x: x[0])
        maxaff = 0
        start = 0
        for i in range(len(affluence)-4):
            if sum(j for _, j in affluence[i:i+4]) > maxaff:
                maxaff = sum(j for _, j in affluence[i:i+4])
                start = i

        matrices["HP"] = sum([matrices[t] for t, _ in affluence[start:start+4]])
        return matrices


class Vehicle:
    def __init__(self, id:int, type:str, time:str, path:str, sens:int|None = None) -> None:
        self.id = id
        self.type = type
        self.time = datetime.strptime(time, "%Y-%m-%d %Hh%M") #2025-02-19 10h11
        self.sens = sens
        path = path.replace("\\", "/")
        self.path = path

        param = self.path.split("/")
        #print(self.path, param)
        self.short = {"id" : self.id, "time" : self.time, "line" : int(param[-2]), "sens" : self.sens, "name" : param[-1]}

def window():
    root = TkinterDnD.Tk()

    file_lab = tk.Label(root, text="Dossier : ")
    file_lab.grid(row=0, column=0, pady=10, padx=5)
    file_path = tk.StringVar()
    file_entry = tk.Entry(root, textvariable=file_path)
    file_entry.grid(row=0, column=1, columnspan=2, pady=10, padx=5)

    conglo = tk.BooleanVar(value=True)
    conglot = tk.Label(root, text="Agglomérer VUL et VL : ")
    conglot.grid(row=1, column=0, pady=10, padx=5)
    conglot = tk.Radiobutton(root, variable=conglo, value=True, text="Oui")
    conglot.grid(row=1, column=1, pady=10, padx=5)
    conglof = tk.Radiobutton(root, variable=conglo, value=False, text="Non")
    conglof.grid(row=1, column=2, pady=10, padx=5)

    def validate():
        path = file_path.get()
        path = path.strip('"{}')
        P = Parser(path, conglo=conglo.get())
        P.parse(root)
        P.make_csv()
        root.destroy()

    def create_bt():
        bt = tk.Button(root, text="Valider", command=validate)
        bt.grid(row=2, column=0, columnspan=3, pady=10, padx=5)

    def on_drop(event):
        # When a file is dropped, set the file path into the entry widget
        file_path.set(event.data)  # event.data contains the file path
        create_bt()

    # Initialize the main window with drag-and-drop support
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)
    root.mainloop()


if __name__ == "__main__":
    window()