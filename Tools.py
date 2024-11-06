import tkinter as tk

def window():
    root = tk.Tk()

    def parse():
        import tools.resultParse as rp
        root.destroy()
        rp.window()
    bt_parse = tk.Button(root, text="Formattage de résultats", command=parse)
    bt_parse.grid(column=0, row=0, pady=10, padx=5)

    #!todo : make rename
    def rename():
        pass
    bt_rename = tk.Button(root, text = "Renommer vidéos", command=rename)
    bt_rename.config(state="disabled")
    bt_rename.grid(column=1, row=0, pady=10, padx=5)

    root.mainloop()

window()