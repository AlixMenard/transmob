import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import math

def split(path, size):
    files = os.listdir(path)
    nb_splits = math.ceil(len(files)/5)
    os.chdir(path)
    for i in range(nb_splits):
        os.mkdir(f"split_{i}")
        for _ in range(size):
            if len(files) == 0:
                break
            f = files.pop(0)
            os.replace(rf"{path}\{f}", rf"{path}\split_{i}\{f}")

def window():
    root = TkinterDnD.Tk()

    file_lab = tk.Label(root, text = "Dossier à séparer : ")
    file_lab.grid(row = 0, column = 0, pady=10, padx=5)
    file_path = tk.StringVar()
    file_entry = tk.Entry(root, textvariable = file_path)
    file_entry.grid(row = 0, column = 1, pady=10, padx=5)

    size_lab = tk.Label(root, text = "Taille des sous-dossiers : ")
    size_lab.grid(row = 1, column = 0, pady=10, padx=5)
    size_var = tk.IntVar(value = 5)
    size_entry = tk.Entry(root, textvariable = size_var)
    size_entry.grid(row = 1, column = 1, pady=10, padx=5)

    def validate():
        path = file_path.get()
        path = path.strip('"{}')
        split(path, int(size_entry.get()))
        root.destroy()

    def create_bt():
        bt = tk.Button(root, text = "Valider", command = validate)
        bt.grid(row = 2, column = 0, columnspan = 2, pady=10, padx=5)

    def on_drop(event):
        # When a file is dropped, set the file path into the entry widget
        file_path.set(event.data)  # event.data contains the file path
        create_bt()

    # Initialize the main window with drag-and-drop support
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)
    root.mainloop()

if __name__ == '__main__':
    window()