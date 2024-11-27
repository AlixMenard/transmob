import json
import pprint
from collections import defaultdict
from datetime import *
from functools import total_ordering
from typing import List
import ast
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os

from torch.distributions import Pareto


class Parser:
    def __init__(self, path, save_path = None):
        self.timelapse = None
        if save_path is None:
            self.save_path = path
        else:
            self.save_path = save_path
        self.path = path
    
    def parse(self):
        if self.path[-4:] != '.txt':
            if os.path.isdir(self.path):
                for filename in os.listdir(self.path):
                    P = Parser(fr"{self.path}/{filename}")
                    P.parse()
            return

        with open(self.path, "r") as f:
            quarters = f.read().split("@")[1:]
        dates = set(q[:10] for q in quarters)

        def day_q():
            q = []
            for h in range(24):
                for m in range(0, 60, 15):
                    q.append(f"{h:02d}h{m:02d}")
            return q

        timelapse = [Quarter(datetime.strptime(f"{d} {t}",'%Y-%m-%d %Hh%M'))  for d in dates for t in day_q()]
        counted_q : List[Quarter] = []

        for q in quarters:
            lines = q.strip().split("\n")
            times = lines[0].split(", ")
            start = datetime.strptime(times[0],'%Y-%m-%d %Hh%M')
            end = datetime.strptime(times[1],'%Y-%m-%d %Hh%M')
            q = Quarter(start, end)
            counts = lines[1:]
            for c in counts:
                colon_ind = c.index(":")
                count = ast.literal_eval(c[colon_ind+2:])
                q.add(int(c[:colon_ind-1]), count)
            counted_q.append(q)
        
        for q in counted_q:
            for t in timelapse:
                ratio = q/t
                if ratio:
                    for line in q.count:
                        t.add(line, q.count[line], ratio)
        
        timelapse.sort()
        self.timelapse = timelapse[:]
        self.make_csv()
        
    def save(self):
        with open(self.save_path, "w") as f:
            for q in self.timelapse:
                f.write(f"{q.start} - {q.end} - {len(q.count)}\n")
                for line in q.count:
                    f.write(f"{line}:{q.pretty_count(line)}\n")

    def make_csv(self):
        columns = ["car", "truck", "bus", "motorbike", "bicycle", "person", "scooter"]
        with open(self.save_path[:-3]+"csv", "w") as f:
            f.write("date;time;line;sens;" + ";".join(columns) + "\n")
            for q in self.timelapse:
                for l in q.count:
                    #Standard ISO formatting apparently
                    line = [q.start.strftime("%Y-%m-%d"), q.start.strftime("%Hh%M")+q.end.strftime("-%Hh%M"), str(l)]
                    for col in columns:
                        line0 = line[:]
                        line1 = line[:]
                        line0 += ["0"] + [str(q.count[l][0][col]) if col in q.count[l][0] else "0" for col in columns]
                        line1 += ["1"] + [str(q.count[l][1][col]) if col in q.count[l][1] else "0" for col in columns]
                    f.write(";".join(line0) + "\n")
                    f.write(";".join(line1) + "\n")

@total_ordering
class Quarter:
    def __init__(self, start:datetime, end:datetime|None = None):
        self.start = start
        self.end = start + timedelta(minutes=15) if end is None else end
        self.count = defaultdict(lambda: [defaultdict(int), defaultdict(int)])
    
    def pretty_count(self, line:int|None = None):
        return pprint.pformat(json.loads(json.dumps(self.count))) if line is None else pprint.pformat(json.loads(json.dumps(self.count[line])))

    def __repr__(self) -> str:
        return f"{self.start} - {self.end}\n{self.pretty_count()}\n"

    def __truediv__(self, other:"Quarter"):
        #how much of interval self is also in other
        overlap_start = max(self.start, other.start)
        overlap_end = min(self.end, other.end)

        # Check if there is an overlap
        if overlap_start < overlap_end:
            overlap_duration = (overlap_end - overlap_start).total_seconds()
            interval1_duration = (self.end - self.start).total_seconds()

            # Calculate overlap percentage for each interval
            overlap = (overlap_duration / interval1_duration)
            
            return overlap
        else:
            return 0.0  # No overlap

    def __eq__(self, other:"Quarter"):
        return self.start == other.start

    def __lt__(self, other:"Quarter"):
        return self.start < other.start

    def add(self, line:int, count, ratio = 1.):
        for sense in range(2):
            for k in count[sense]:
                self.count[line][sense][k] += int(count[sense][k]*ratio)

def window():
    root = TkinterDnD.Tk()

    file_lab = tk.Label(root, text = "Fichier de résultats : ")
    file_lab.grid(row = 0, column = 0, pady=10, padx=5)
    file_path = tk.StringVar()
    file_entry = tk.Entry(root, textvariable = file_path)
    file_entry.grid(row = 0, column = 1, pady=10, padx=5)

    def validate():
        path = file_path.get()
        path = path.strip('"{}')
        P = Parser(path)
        P.parse()
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

if __name__ == "__main__":
    window()