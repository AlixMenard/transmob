import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import time

import cv2

def str_time(_time):
    c_time_str = time.ctime(_time)
    c_time_str = time.strptime(c_time_str)
    c_time_str = time.strftime("%Y%m%d_%Hh%M", c_time_str)
    return c_time_str

def rename(path, camera, city):
    camera = camera.replace(" ", "_")
    city = city.replace(" ", "_")
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            continue
        cap = cv2.VideoCapture(rf"{path}/{file}")
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.release()
        c_time = os.path.getmtime(rf"{path}/{file}") - int(length / fps)
        c_time = float(int(c_time / 60) * 60)
        strtime = str_time(c_time)

        ext = os.path.splitext(file)[1]
        name = f"{camera}_{city}_{strtime}"
        os.rename(rf"{path}/{file}", rf"{path}/{name}{ext}")

def window():
    root = TkinterDnD.Tk()

    file_lab = tk.Label(root, text = "Dossier de vidéos : ")
    file_lab.grid(row = 0, column = 0, pady=10, padx=5)
    file_path = tk.StringVar()
    file_entry = tk.Entry(root, textvariable = file_path)
    file_entry.grid(row = 0, column = 1, pady=10, padx=5)

    def validate():
        path = file_path.get()
        path = path.strip('"{}')

        cam = camera.get()
        cit = city.get()
        cit = cit.replace("-"," ")
        cit = cit.replace("'"," ")
        cit = "_".join([m.strip().capitalize() for m in cit.split(" ")])

        rename(path, cam, cit)

        root.destroy()

    def create_bt():
        bt = tk.Button(root, text = "Valider", command = validate)
        bt.grid(row = 3, column = 0, columnspan = 2, pady=10, padx=5)

    def on_drop(event):
        # When a file is dropped, set the file path into the entry widget
        file_path.set(event.data)  # event.data contains the file path
        create_bt()

    camera = tk.StringVar()
    camera_lab = tk.Label(root, text = "Nom de la caméra (GPXX)")
    camera_lab.grid(row = 1, column = 0, pady=10, padx=5)
    camera_entry = tk.Entry(root, textvariable = camera)
    camera_entry.grid(row = 2, column = 0, pady=10, padx=5)
    city = tk.StringVar()
    city_lab = tk.Label(root, text = "Nom de l'emplacement")
    city_lab.grid(row = 1, column = 1, pady=10, padx=5)
    city_entry = tk.Entry(root, textvariable = city)
    city_entry.grid(row = 2, column = 1, pady=10, padx=5)

    # Initialize the main window with drag-and-drop support
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)
    root.mainloop()

if __name__ == "__main__":
    window()