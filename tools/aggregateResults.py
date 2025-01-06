import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

def aggregateResults(path):
    res_files = get_res_files(path)
    text = ""
    for res_file in res_files:
        with open(res_file, 'r', encoding='utf-8') as f:
            t = f.read()
        if t[-1] != "\n":
            t = t + "\n"
        text += t
    with open(path + '\\results.txt', 'w', encoding='utf-8') as f:
        f.write(text)

def get_res_files(path):
    files = os.listdir(path)
    res_files = []
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            res_files += get_res_files(os.path.join(path, file))
        elif file == "results.txt":
            res_files.append(os.path.join(path, file))
    return res_files

def window():
    root = TkinterDnD.Tk()

    file_lab = tk.Label(root, text = "Dossier à aggréger : ")
    file_lab.grid(row = 0, column = 0, pady=10, padx=5)
    file_path = tk.StringVar()
    file_entry = tk.Entry(root, textvariable = file_path)
    file_entry.grid(row = 0, column = 1, pady=10, padx=5)

    def validate():
        path = file_path.get()
        path = path.strip('"{}')
        aggregateResults(path)
        root.destroy()

    def create_bt():
        bt = tk.Button(root, text = "Valider", command = validate)
        bt.grid(row = 1, column = 0, columnspan = 2, pady=10, padx=5)

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