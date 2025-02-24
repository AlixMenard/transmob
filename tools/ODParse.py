import json
import pprint
import tkinter
from datetime import *
from typing import List
import ast
import tkinter as tk

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

        self.decision_var = tk.BooleanVar(value=False)
        self.result = None

        # Display paths
        self.left_path_label = tk.Label(self.root)
        self.left_path_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.right_path_label = tk.Label(self.root)
        self.right_path_label.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

        # Image display frames
        self.left_image_label = tk.Label(root)
        self.left_image_label.grid(row=1, rowspan=3, column=0, padx=10, pady=10)

        self.right_image_label = tk.Label(root)
        self.right_image_label.grid(row=1, rowspan=3, column=3, padx=10, pady=10)

        # Short display
        self.left_short1_label = tk.Label(self.root)
        self.left_short1_label.grid(row=1, column=1, padx=10, pady=10)
        self.left_short2_label = tk.Label(self.root)
        self.left_short2_label.grid(row=2, column=1, padx=10, pady=10)
        self.left_short3_label = tk.Label(self.root)
        self.left_short3_label.grid(row=3, column=1, padx=10, pady=10)

        self.right_short1_label = tk.Label(self.root)
        self.right_short1_label.grid(row=1, column=2, padx=10, pady=10)
        self.right_short2_label = tk.Label(self.root)
        self.right_short2_label.grid(row=2, column=2, padx=10, pady=10)
        self.right_short3_label = tk.Label(self.root)
        self.right_short3_label.grid(row=3, column=2, padx=10, pady=10)

        # Approve and Reject buttons
        self.approve_button = tk.Button(root, text="✅ Approve", command=self.approve_match, width=15, bg="green", fg="white")
        self.approve_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.reject_button = tk.Button(root, text="❌ Reject", command=self.reject_match, width=15, bg="red", fg="white")
        self.reject_button.grid(row=4, column=2, columnspan=2, pady=10)

        # Internal variables
        self.result = None
        self.root.withdraw()  # Hide initially; show when needed

    def show_images(self, enter_vehicle, exit_vehicle):
        """Display two images side-by-side for user validation."""
        self.root.deiconify()  # Show the window if hidden

        # Convert OpenCV images (BGR) to PIL images (RGB)
        enter_image = cv2.imread(enter_vehicle.path)
        enter_image = Image.fromarray(cv2.cvtColor(enter_image, cv2.COLOR_BGR2RGB))
        exit_image = cv2.imread(exit_vehicle.path)
        exit_image = Image.fromarray(cv2.cvtColor(exit_image, cv2.COLOR_BGR2RGB))

        # Resize for display
        enter_image = enter_image.resize((300, 200))
        exit_image = exit_image.resize((300, 200))

        # Convert to Tkinter-compatible format
        self.enter_photo = ImageTk.PhotoImage(enter_image)
        self.exit_photo = ImageTk.PhotoImage(exit_image)

        # Update paths
        self.left_path_label.configure(text=enter_vehicle.path)
        self.right_path_label.configure(text=exit_vehicle.path)

        # Update shorts
        self.left_short1_label.configure(text=enter_vehicle.short["id"])
        self.left_short2_label.configure(text=enter_vehicle.short["time"])
        self.left_short3_label.configure(text=f"Entered from line {enter_vehicle.short['line']}")

        self.right_short1_label.configure(text=exit_vehicle.short["id"])
        self.right_short2_label.configure(text=exit_vehicle.short["time"])
        self.right_short3_label.configure(text=f"Exited from line {exit_vehicle.short['line']}")

        # Update labels
        self.left_image_label.config(image=self.enter_photo)
        self.right_image_label.config(image=self.exit_photo)

        self.result = None
        self.root.wait_variable(self.decision_var)  # Wait for user approval or rejection

    def approve_match(self):
        self.result = True
        self.decision_var.set(True)
        self.root.withdraw()  # Hide window after decision

    def reject_match(self):
        self.result = False
        self.decision_var.set(True)
        self.root.withdraw()

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

def get_top_matches(enter_vehicle, exit_vehicles, top_k=10):
    """Return top_k closest exiting vehicles to the entering vehicle."""
    if not exit_vehicles:
        return []

    exit_features = np.vstack([v.features for v in exit_vehicles])
    distances = cdist(enter_vehicle.features.reshape(1, -1), exit_features, metric='cosine')[0]
    top_indices = np.argsort(distances)[:top_k]
    return [(exit_vehicles[i], distances[i]) for i in top_indices]

def match_with_user_validation(vehicle_paths, root, top_k=10):
    matcher_gui = VehicleMatcherGUI(root)
    match_list = []

    accepted_distances = []
    refused_distances = []

    for enter_idx, enter_list in enumerate(vehicle_paths):
        enter_vehicles = [v for v in enter_list if v.sens == 0]

        for enter_vehicle in enter_vehicles:
            # Gather exiting vehicles from other paths
            exit_candidates = [
                (exit_idx, exit_vehicle)
                for exit_idx, exit_list in enumerate(vehicle_paths)
                for exit_vehicle in exit_list
                if exit_vehicle.sens == 1 and exit_vehicle.id >= enter_vehicle.id
            ]

            if not exit_candidates:
                continue

            exit_vehicles = [ev for _, ev in exit_candidates]
            top_matches = get_top_matches(enter_vehicle, exit_vehicles, top_k=top_k)

            acc_thresh = np.mean(accepted_distances) - 2.5*np.std(accepted_distances) if accepted_distances else 0
            ref_thresh = np.mean(refused_distances) + 2.5*np.std(refused_distances) if refused_distances else float("inf")

            for candidate_exit_vehicle, distance in top_matches:
                decision = None
                if acc_thresh < ref_thresh and candidate_exit_vehicle.short["line"] != enter_vehicle.short["line"]:
                    if distance < acc_thresh and len(accepted_distances)>=10:
                        decision = True
                        print(f"Accepted : {distance}<{acc_thresh}")
                        print(enter_vehicle.short, candidate_exit_vehicle.short)
                    elif distance > ref_thresh and len(refused_distances)>=10:
                        decision = False
                        print(f"Refused : {distance}>{ref_thresh}")
                if decision is None:
                    matcher_gui.show_images(enter_vehicle, candidate_exit_vehicle)
                    decision = matcher_gui.get_result()

                if decision:  # User approved
                    accepted_distances.append(distance)
                    vehicle_paths[enter_idx].remove(enter_vehicle)
                    exit_idx = next(idx for idx, ev in exit_candidates if ev == candidate_exit_vehicle)
                    vehicle_paths[exit_idx].remove(candidate_exit_vehicle)
                    match_list.append((enter_idx, exit_idx, candidate_exit_vehicle))
                    break  # Go to next entering vehicle
                else:
                    refused_distances.append(distance)

            else:
                #print("🚫 No approved match found after top 10 candidates.")
                vehicle_paths[enter_idx].remove(enter_vehicle)
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

    def parse(self, root):

        for widget in root.winfo_children():
            widget.destroy()

        screens_folders = []
        for dirpath, dirnames, _ in os.walk(self.path):
            if "screens" in dirnames:
                screens_folders.append(os.path.join(dirpath, "screens"))

        line_nb = len(os.listdir(screens_folders[0]))

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
        uids = {v.id for l in vehicle_paths for v in l}
        print(f"{unmatched} left unmatched, processing with ReId. {uids}", end = " ", flush = True)

        cfg = get_cfg()
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])
        cfg.merge_from_file(r"FastReId_config/bagtricks_R50-ibn.yml")
        cfg.MODEL.WEIGHTS = "FastReId_config/veriwild_bot_resnet50.pt"
        cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        predictor = DefaultPredictor(cfg)
        for path in vehicle_paths:
            for vehicle in path:
                image = cv2.imread(vehicle.path)[:, :, ::-1]
                image = resize_with_padding(image, cfg.INPUT.SIZE_TEST[::-1])
                image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1)) / 255.0
                image = normalize(image).unsqueeze(0).to(cfg.MODEL.DEVICE)
                vehicle.features = predictor(image)
        print("Matching...", flush = True)
        match_with_user_validation(vehicle_paths, root, top_k=10)



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