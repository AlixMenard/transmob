import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import time
import datetime as dt

import cv2

def str_time(_time):
    c_time_str = time.ctime(_time)
    c_time_str = time.strptime(c_time_str)
    c_time_str = time.strftime("%Y%m%d_%Hh%M", c_time_str)
    return c_time_str

def redate(path, start):
    files = os.listdir(path)
    files.sort(key=lambda x:os.path.getctime(rf'{path}/{x}'))
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            continue

        cap = cv2.VideoCapture(rf"{path}/{file}")
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.release()
        duration = length / fps
        duration = dt.timedelta(seconds=duration)

        start += duration
        os.utime(rf"{path}/{file}", (start.timestamp(),start.timestamp()))

def window():
    root = TkinterDnD.Tk()

    file_lab = tk.Label(root, text = "Dossier de vidéos : ")
    file_lab.grid(row = 0, column = 0, pady=10, padx=5)
    file_path = tk.StringVar()
    file_entry = tk.Entry(root, textvariable = file_path)
    file_entry.grid(row = 0, column = 1, pady=10, padx=5)

    date_lab = tk.Label(root, text = "Date de la première vidéo : ")
    date_lab.grid(row = 1, column = 0, pady=10, padx=5)
    date_string = tk.StringVar(value = "YYYY/MM/DD hh:mm")
    date_entry = tk.Entry(root, textvariable = date_string)
    date_entry.grid(row = 1, column = 1, pady=10, padx=5)

    def validate():
        path = file_path.get()
        path = path.strip('"{}')

        date = date_entry.get()
        date = dt.datetime.strptime(date, "%Y/%m/%d %H:%M")

        redate(path, date)

        root.destroy()

    def create_bt():
        bt = tk.Button(root, text = "Valider", command = validate)
        bt.grid(row = 3, column = 0, columnspan = 2, pady=10, padx=5)

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