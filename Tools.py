import tkinter as tk

end = False

def window():
    root = tk.Tk()

    def parse():
        import tools.resultParse as rp
        root.destroy()
        rp.window()
    bt_parse = tk.Button(root, text="Formattage de résultats", command=parse)
    bt_parse.grid(column=0, row=0, pady=10, padx=5)

    def rename():
        import tools.videoRename as vr
        root.destroy()
        vr.window()

    bt_rename = tk.Button(root, text = "Renommer vidéos", command=rename)
    bt_rename.grid(column=1, row=0, pady=10, padx=5)

    def split():
        import tools.splitVids as sv
        root.destroy()
        sv.window()

    bt_split = tk.Button(root, text="Séparer vidéos", command=split)
    bt_split.grid(column=0, row=1, pady=10, padx=5)

    def aggregate():
        import tools.aggregateResults as ar
        root.destroy()
        ar.window()

    bt_split = tk.Button(root, text="Aggréger résultats", command=aggregate)
    bt_split.grid(column=1, row=1, pady=10, padx=5)

    def repair():
        import tools.repairVids as rv
        root.destroy()
        rv.window()

    bt_split = tk.Button(root, text="Réparer vidéos", command=repair)
    bt_split.grid(column=0, row=2, columnspan = 2, pady=10, padx=5)

    def on_closing():
        global end
        end = True
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

while not end:
    window()