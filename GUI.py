import tkinter as tk
from tkinter.ttk import Label
import os
import signal
import traceback

from pyparsing import one_of

os.environ["OPENCV_LOG_LEVEL"] = "OFF"
import torch

from PIL.ImageColor import colormap
from pandas.io.sas.sas_constants import column_label_length_offset
from tkinterdnd2 import TkinterDnD, DND_FILES
#import Transmob.VideoProcesser as vpYT
#import TransmobNT.VideoProcesser as vpYTNT
if not torch.cuda.is_available():
    import TransmobYT.VideoProcesser as vpYT
    bcuda = False
else:
    bcuda = True
    import TransmobYTC.VideoProcesser as vpYT

def signal_handler(sig, frame):
    print("Caught signal:", sig)
    print("Stack trace:")
    traceback.print_stack(frame)


def setup_window():


    def on_drop(event):
        # When a file is dropped, set the file path into the entry widget
        entry_var.set(event.data)  # event.data contains the file path
        create_bt()

    # Initialize the main window with drag-and-drop support
    root = TkinterDnD.Tk()

    """#? Processer used
    L = tk.Label(root, text = "Processes : ")
    L.grid(row = 0, column = 0, columnspan = 2,  pady=20, padx=5)
    process = tk.StringVar(value = "YT")
    T = tk.Radiobutton(root, text = "Classique", variable = process, value = "Classic")
    TNT = tk.Radiobutton(root, text = "Parallélisation imbriquée", variable = process, value = "NT")
    TYT = tk.Radiobutton(root, text = "YAllO"+(" (CUDA)" if bcuda else ""), variable = process, value = "YT")
    T.grid(row = 0, column = 2, columnspan = 2, pady=20, padx=5)
    TNT.grid(row = 0, column = 4, columnspan = 2, pady=20, padx=5)
    TYT.grid(row = 0, column = 6, columnspan = 2, pady=20, padx=5)"""

    recommended_cores = {"Classic" : 5, "NT" : 4, "YT" : 3}

    # Set window title and dimensions
    root.title("AI Video Processing")

    #? File name

    # Create a tkinter variable to store the entry content
    entry_var = tk.StringVar()

    # Create an Entry widget to show the dropped file path
    entry_l = tk.Label(root, text = "Chemin vers le fichier : ")
    entry_l.grid(row = 1, column = 0, columnspan = 4, pady=20, padx=5)
    entry = tk.Entry(root, textvariable=entry_var, width=50)
    entry.grid(row = 1, column = 4, columnspan = 4, pady=20, padx=5)

    #Processing settings
    #? Frame_nb
    frame_nb = tk.IntVar(value = 1)
    frame_l = tk.Label(root, text = "Nombre de frames : ")
    frame_l.grid(row = 2, column = 0, columnspan = 4, pady=10, padx=5)
    frame_nb_rb1 = tk.Radiobutton(root, text="1", variable=frame_nb, value=1)
    frame_nb_rb1.grid(row = 2, column = 4, columnspan = 2, pady=10, padx=5)
    frame_nb_rb2 = tk.Radiobutton(root, text="2", variable=frame_nb, value=2)
    frame_nb_rb2.grid(row = 2, column = 6, columnspan = 2, pady=10, padx=5)

    #? model
    model_letter = tk.StringVar(value = "x")
    model_l = tk.Label(root, text = "Model YOLO : ")
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

    checkbox_label = tk.Label(root, text="Types de véhicules :")
    checkbox_label.grid(row=4, column=0, columnspan = 2, pady=10, padx=5)
    checkboxes_func = []
    for idx, item in enumerate(items):
        checkboxes_func.append(lambda item=item: update_classes(item))
        checkbox_vars[item] = tk.BooleanVar()
        checkbox = tk.Checkbutton(root, text=item, variable=checkbox_vars[item], command=checkboxes_func[idx])
        checkbox_vars[item].set(True)
        checkbox.grid(row=4, column=idx+2, pady=10, padx=5)
    update_classes("")

    """#? core nb
    def validate_input(value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        return False
    core_nb = tk.IntVar(value=recommended_cores[process.get()])
    core_l = tk.Label(root, text = "Nombre de coeurs")
    core_l.grid(row = 5, column = 0, columnspan= 4, pady=10, padx=5)
    vcmd = (root.register(validate_input), '%P')
    core_entry = tk.Entry(root, textvariable = core_nb, width=10, validate="key", validatecommand=vcmd)
    core_entry.grid(row = 5, column = 4, columnspan= 6, pady=10, padx=5)"""

    # ? graph option
    graphb = tk.BooleanVar(value=False)
    graph_l = tk.Label(root, text = "Avec vidéo")
    graph_l.grid(row = 6, column = 0, columnspan = 4)
    graph_t = tk.Radiobutton(root, text = "Oui", variable = graphb, value = True)
    graph_t.grid(row = 6, column = 4, columnspan = 2)
    graph_f = tk.Radiobutton(root, text = "Non", variable = graphb, value = False)
    graph_f.grid(row = 6, column = 6, columnspan = 2)

    # ? screen option
    screenb = tk.BooleanVar(value=False)
    screen_l = tk.Label(root, text = "Avec captures d'écran")
    screen_l.grid(row = 7, column = 0, columnspan = 4)
    screen_t = tk.Radiobutton(root, text = "Oui", variable = screenb, value = True)
    screen_t.grid(row = 7, column = 4, columnspan = 2)
    screen_f = tk.Radiobutton(root, text = "Non", variable = screenb, value = False)
    screen_f.grid(row = 7, column = 6, columnspan = 2)

    # ? 1 only setup option
    onesetupb = tk.BooleanVar(value=True)
    onesetupb.trace("w", lambda *x: one_setup(onesetupb))
    validationb = tk.BooleanVar(value=False)
    screen_l = tk.Label(root, text = "Un seul setup")
    screen_l.grid(row = 8, column = 0, columnspan = 4)
    screen_t = tk.Radiobutton(root, text = "Oui", variable = onesetupb, value = True)
    screen_t.grid(row = 8, column = 4, columnspan = 2)
    screen_f = tk.Radiobutton(root, text = "Non", variable = onesetupb, value = False)
    screen_f.grid(row = 8, column = 6, columnspan = 2)

    def one_setup(osb):
        if osb.get():
            validation_l = tk.Label(root, text = "Valider les lignes")
            validation_l.grid(row = 9, column = 0, columnspan = 4)
            validation_t = tk.Radiobutton(root, text = "Oui", variable = validationb, value = True)
            validation_t.grid(row = 9, column = 4, columnspan = 2)
            validation_f = tk.Radiobutton(root, text = "Non", variable = validationb, value = False)
            validation_f.grid(row = 9, column = 6, columnspan = 2)
        else:
            for widget in root.grid_slaves():
                if widget.grid_info()["row"] == 9:
                    widget.destroy()
    one_setup(onesetupb)


    # ? SAHI
    sahib = tk.BooleanVar(value=False)
    if torch.cuda.is_available():
        sahi_l = tk.Label(root, text = "Detection fragmentaire")
        sahi_l.grid(row = 10, column = 0, columnspan = 4)
        sahi_t = tk.Radiobutton(root, text = "Oui", variable = sahib, value = True)
        sahi_t.grid(row = 10, column = 4, columnspan = 2)
        sahi_f = tk.Radiobutton(root, text = "Non", variable = sahib, value = False)
        sahi_f.grid(row = 10, column = 6, columnspan = 2)

    """# ? OD
    ODb = tk.BooleanVar(value=False)
    if torch.cuda.is_available():
        OD_l = tk.Label(root, text = "Traitement OD")
        OD_l.grid(row = 11, column = 0, columnspan = 4)
        OD_t = tk.Radiobutton(root, text = "Oui", variable = ODb, value = True)
        OD_t.grid(row = 11, column = 4, columnspan = 2)
        OD_f = tk.Radiobutton(root, text = "Non", variable = ODb, value = False)
        OD_f.grid(row = 11, column = 6, columnspan = 2)"""

    # ! Validation
    def start():
        root.destroy()
        Playlist = vpYT.Playlist
            
        P = Playlist(entry_var.get().strip('"{}'), model=f"weights/yolo11{model_letter.get()}.pt",
                     watch_classes=classes, graph = graphb.get(), screenshots = screenb.get(),
                     onesetup = onesetupb.get(), validation = validationb.get(), SAHI = sahib.get(),
                     #OD = ODb.get()
                     )
        P.initialise()
        results = P.play()
        result_window(results)

    def create_bt():
        val_bt = tk.Button(root, text="Valider", command=start)
        val_bt.grid(row = 12, column=0, columnspan=8, pady=10, padx=5)

    # Bind the entry widget to accept file drops
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    root.mainloop()

def result_window(results):
    vidd, procd, diff = results
    root = tk.Tk()
    L = tk.Label(root, text="Résultats")
    L.pack()
    L1 = tk.Label(root, text = f"Temps total de vidéo   : {vpYT.format_dur(vidd)}")
    L1.pack()
    L2 = tk.Label(root, text = f"Temps total d'analyse  : {vpYT.format_dur(procd)}")
    L2.pack()
    L3 = tk.Label(root, text = f"Différence : {diff}%")
    L3.pack()

    def gosetup():
        root.destroy()
        setup_window()

    bt = tk.Button(root, text = "Ok", command=gosetup)
    bt.pack()

if __name__ == "__main__":
    setup_window()