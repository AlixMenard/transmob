import tkinter as tk

from PIL.ImageColor import colormap
from pandas.io.sas.sas_constants import column_label_length_offset
from tkinterdnd2 import TkinterDnD, DND_FILES
import Transmob.VideoProcesser as vp
import TransmobNT.VideoProcesser as vpNT
import TransmobYT.VideoProcesser as vpYT
from TransmobYT.VideoProcesser import Playlist


def setup_window():


    def on_drop(event):
        # When a file is dropped, set the file path into the entry widget
        entry_var.set(event.data)  # event.data contains the file path
        create_bt()

    # Initialize the main window with drag-and-drop support
    root = TkinterDnD.Tk()

    #? Processer used
    L = tk.Label(root, text = "Processing scheme : ")
    L.grid(row = 0, column = 0, columnspan = 2,  pady=20, padx=5)
    process = tk.StringVar(value = "NT")
    T = tk.Radiobutton(root, text = "Classic", variable = process, value = "Classic")
    TNT = tk.Radiobutton(root, text = "Nested Threads", variable = process, value = "NT")
    TYT = tk.Radiobutton(root, text = "YAllO", variable = process, value = "YT")
    T.grid(row = 0, column = 2, columnspan = 2, pady=20, padx=5)
    TNT.grid(row = 0, column = 4, columnspan = 2, pady=20, padx=5)
    TYT.grid(row = 0, column = 6, columnspan = 2, pady=20, padx=5)

    # Set window title and dimensions
    root.title("AI Video Processing")

    # Create a tkinter variable to store the entry content
    entry_var = tk.StringVar()

    # Create an Entry widget to show the dropped file path
    entry_l = tk.Label(root, text = "Path to the folder : ")
    entry_l.grid(row = 1, column = 0, columnspan = 4, pady=20, padx=5)
    entry = tk.Entry(root, textvariable=entry_var, width=50)
    entry.grid(row = 1, column = 4, columnspan = 4, pady=20, padx=5)

    #Processing settings
    #? Frame_nb
    frame_nb = tk.IntVar(value = 2)
    frame_l = tk.Label(root, text = "Frame speed : ")
    frame_l.grid(row = 2, column = 0, columnspan = 4, pady=10, padx=5)
    frame_nb_rb1 = tk.Radiobutton(root, text="1", variable=frame_nb, value=1)
    frame_nb_rb1.grid(row = 2, column = 4, columnspan = 2, pady=10, padx=5)
    frame_nb_rb2 = tk.Radiobutton(root, text="2", variable=frame_nb, value=2)
    frame_nb_rb2.grid(row = 2, column = 6, columnspan = 2, pady=10, padx=5)

    #? model
    model_letter = tk.StringVar(value = "m")
    model_l = tk.Label(root, text = "AI model : ")
    model_l.grid(row = 3, column = 0, columnspan = 3, pady=20, padx=5)
    model_rb1 = tk.Radiobutton(root, text="n", variable=model_letter, value="n")
    model_rb1.grid(row = 3, column = 3, pady=10, padx=5)
    model_rb2 = tk.Radiobutton(root, text="s", variable=model_letter, value="s")
    model_rb2.grid(row = 3, column = 4, pady=10, padx=5)
    model_rb3 = tk.Radiobutton(root, text="m", variable=model_letter, value="m")
    model_rb3.grid(row = 3, column = 5, pady=10, padx=5)
    model_rb4 = tk.Radiobutton(root, text="l", variable=model_letter, value="l")
    model_rb4.grid(row = 3, column = 6, pady=10, padx=5)
    model_rb5 = tk.Radiobutton(root, text="x", variable=model_letter, value="x")
    model_rb5.grid(row = 3, column = 7, pady=10, padx=5)

    #? watch classes

    items = ["car", "truck", "motorbike", "bus", "bicycle", "person"]
    classes = []
    checkbox_vars = {}
    # Function to update the 'classes' list when a checkbox is toggled
    def update_classes(c):
        classes.clear()
        if c == "person" and checkbox_vars["person"].get():
            checkbox_vars["bicycle"].set(True)
            checkbox_vars["motorbike"].set(True)
        elif c in ["motorbike", "bicycle"] and (not checkbox_vars["motorbike"].get() or not checkbox_vars["bicycle"].get()):
            checkbox_vars["person"].set(False)
        for item, var in checkbox_vars.items():
            if var.get():
                classes.append(item)

    checkbox_label = tk.Label(root, text="Select classes :")
    checkbox_label.grid(row=4, column=0, columnspan = 2, pady=10, padx=5)
    checkboxes_func = []
    for idx, item in enumerate(items):
        checkboxes_func.append(lambda item=item: update_classes(item))
        checkbox_vars[item] = tk.BooleanVar()
        checkbox = tk.Checkbutton(root, text=item, variable=checkbox_vars[item], command=checkboxes_func[idx])
        checkbox_vars[item].set(True)
        checkbox.grid(row=4, column=idx+2, pady=10, padx=5)
    update_classes("")

    #? core nb
    def validate_input(value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        return False
    core_nb = tk.IntVar(value=3)
    core_l = tk.Label(root, text = "Number of cores")
    core_l.grid(row = 5, column = 0, columnspan= 4, pady=10, padx=5)
    vcmd = (root.register(validate_input), '%P')
    core_entry = tk.Entry(root, textvariable = core_nb, width=10, validate="key", validatecommand=vcmd)
    core_entry.grid(row = 5, column = 4, columnspan= 6, pady=10, padx=5)

    # ! Validation
    def start():
        root.destroy()
        match process.get():
            case "Classic":
                Playlist = vp.Playlist
            case "NT":
                Playlist = vpNT.Playlist
            case "YT":
                Playlist = vpYT.Playlist
        P = Playlist(entry_var.get(), cores=core_nb.get(), model=f"weights/yolov8{model_letter.get()}.pt", watch_classes=classes)
        P.initialise()
        P.play()
        setup_window()

    def create_bt():
        val_bt = tk.Button(root, text="Start", command=start)
        val_bt.grid(row = 6, column=0, columnspan=8, pady=10, padx=5)

    # Bind the entry widget to accept file drops
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    root.mainloop()

if __name__ == "__main__":
    setup_window()