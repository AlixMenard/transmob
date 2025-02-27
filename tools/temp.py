import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
from scipy.spatial.distance import cdist

class VehicleMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Matching Validation")

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
        for i in range(10):
            frame = tk.Frame(self.matches_frame, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5)

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
        for j in range(len(top_matches), 10):
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

def get_top_matches(enter_vehicle, exit_vehicles, top_k=10):
    if not exit_vehicles:
        return []

    exit_features = np.vstack([v.features for v in exit_vehicles])
    distances = cdist(enter_vehicle.features.reshape(1, -1), exit_features, metric='cosine')[0]
    top_indices = np.argsort(distances)[:top_k]
    return [(exit_vehicles[i], distances[i]) for i in top_indices]

def match_with_user_validation(vehicle_paths, root, top_k=10):
    matcher_gui = VehicleMatcherGUI(root)
    match_list = []

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
            top_matches = get_top_matches(enter_vehicle, exit_vehicles, top_k=top_k)

            matcher_gui.show_images(enter_vehicle, top_matches)
            selected_index = matcher_gui.get_result()

            if selected_index != -1:  # User selected a match
                candidate_exit_vehicle, distance = top_matches[selected_index]
                enter_list.remove(enter_vehicle)
                exit_idx = next(idx for idx, ev in exit_candidates if ev == candidate_exit_vehicle)
                vehicle_paths[exit_idx].remove(candidate_exit_vehicle)
                match_list.append((enter_idx, exit_idx, candidate_exit_vehicle))
            else:
                # User skipped; remove enter_vehicle without matching
                enter_list.remove(enter_vehicle)

    return match_list
