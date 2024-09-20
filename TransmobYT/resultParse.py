import json
import pprint
from collections import defaultdict
from datetime import *
from functools import total_ordering
from typing import List
import ast


class Parser:
    def __init__(self, path, save_path = None):
        self.timelapse = None
        if save_path is None:
            self.save_path = path
        else:
            self.save_path = save_path
        self.path = path
    
    def parse(self):
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
        self.save()
        
    def save(self):
        with open(self.save_path, "w") as f:
            for q in self.timelapse:
                f.write(f"{q.start} - {q.end} - {len(q.count)}\n")
                for line in q.count:
                    f.write(f"{line}:{q.pretty_count(line)}\n")

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

if __name__ == "__main__":
    file = input()
    s = file[:-4] + "2" + file[-4:]
    P = Parser(file, s)
    P.parse()