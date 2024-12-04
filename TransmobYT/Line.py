import numpy as np
from .Vehicle import Vehicle
from typing import Dict, List
from collections import defaultdict

class Line:

    nb_lines = 0
    def del_line(self):
        Line.nb_lines -= 1

    def set_nb_lines(selfself, n):
        Line.nb_lines = n

    def __init__(self, x1, y1, x2, y2, x3, y3):

        self.maskbound = None
        self.id = Line.nb_lines
        Line.nb_lines += 1
        self.counter = Counter()
        self.vehicles = defaultdict(list)
        self.still_close : Dict[int, Vehicle] = {}

        if x1>x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        self.start = (x1, y1)
        self.center = (int((x1+x2)/2), int((y1+y2)/2))
        self.end = (x2, y2)
        self.p3 = (x3,y3)
        dx, dy = abs(x2-x1), abs(y2-y1)
        self.length = np.sqrt(dx**2 + dy**2)
        self.bounds = [x1-0.1*dy, x2+0.1*dy, min(y1, y2)-0.1*dx, max(y1, y2)+0.1*dx]

        #! ax + by + c = 0
        if dx == 0:
            self.a = 1
            self.b = 0
            self.c = -x1
        else:
            self.a = -dy/dx
            self.b = 1
            self.c = - y1 - self.a*x1

        
        self.vec = np.array([self.end[0] - self.start[0], self.end[1] - self.start[1]])
        self.vec = self.vec / np.linalg.norm(self.vec)
        self.normal = np.array([-self.vec[1], self.vec[0]])
        

        x, y = self.p3
        p_vec = np.array([x - self.center[0], y - self.center[1]])
        y3 = np.dot(p_vec, self.normal)
        self.direction = np.sign(y3) if y3 != 0 else 0

        self.mask_bound()

    def mask_bound(self):
        margin = 4/5
        self.maskbound = [
            self.center[0] - self.length * margin,  # left
            self.center[1] - self.length * margin,  # top
            self.center[0] + self.length * margin,  # right
            self.center[1] + self.length * margin   # bottom
                        ]
        self.maskbound = list(map(int, self.maskbound))

    def cleanse(self, still_tracked):
        self.counter.cleanse(still_tracked)

    @staticmethod
    def get_total_bounding_box(lines:List["Line"]):
        if not lines:
            return None

        bbox = lines[0].maskbound
        min_x1, min_y1, max_x2, max_y2 = bbox[0], bbox[1], bbox[2], bbox[3]

        # Iterate through the remaining Line objects
        for line in lines[1:]:
            x1, y1, x2, y2 = line.maskbound
            min_x1 = min(min_x1, x1)
            min_y1 = min(min_y1, y1)
            max_x2 = max(max_x2, x2)
            max_y2 = max(max_y2, y2)
        
        return [min_x1, min_y1, max_x2, max_y2]


    def proj(self, p):
        x, y = p
        p_vec = np.array([x - self.center[0], y - self.center[1]])
        x = np.dot(p_vec, self.vec)
        y = np.dot(p_vec, self.normal)
        y *= self.direction
        return x, y
    
    def unproj(self, x, y):
        x, y = map(int, np.dot(self.P, np.array([x, y])))
        return x, y
    
    def inbound(self, x:int, y:int, v:Vehicle):
        close = self.bounds[0]<=x<=self.bounds[1] and self.bounds[2]<=y<=self.bounds[3]
        if not close and v.id in self.still_close:
            self.still_close.pop(v.id)
        return close

    def cross(self, v : Vehicle):
        crossed = False
        x, y = v.box.cross_point
        _, p = self.proj((x, y))
        if v.id in self.vehicles and (p * np.mean(self.vehicles[v.id])<0 or p ==0):
            if v.id in self.still_close:
                self.vehicles[v.id].append(p)
                return False
            crossed = True
            self.still_close[v.id] = v
            if np.mean(self.vehicles[v.id])<0:
                self.counter.add(v, direction = 0)
                v.cross(self.id)
            else:
                self.counter.add(v, direction = 1)
                v.cross(-self.id)
        self.vehicles[v.id].append(p)
        return crossed


class Counter:

    def __init__(self):
        self.crossed : List[Vehicle] = []
        self.uncrossed : List[Vehicle] = []
        self.previous_c : List[Vehicle] = []
        self.previous_unc : List[Vehicle] = []
    
    def cleanse(self, still_tracked):
        self.previous_c = [v for v in self.crossed if v.id in still_tracked]
        self.previous_unc = [v for v in self.uncrossed if v.id in still_tracked]
        self.crossed.clear()
        self.uncrossed.clear()

    def count(self, classes=None, include_none: bool = False):
        if classes is None:
            classes = []
        if not classes:
            uniques = list(set([v._class for v in self.crossed]))
            dir_in = {}
            for u in uniques:
                dir_in[u] = sum([1 for v in self.crossed if v._class == u and v.oldid is None])

            uniques = list(set([v._class for v in self.uncrossed]))
            dir_out = {}
            for u in uniques:
                dir_out[u] = sum([1 for v in self.uncrossed if v._class == u and v.oldid is None])
            if not include_none:
                if None in dir_in: dir_in.pop(None)
                if None in dir_out: dir_out.pop(None)
            return [dir_in, dir_out]

    def add(self, v : Vehicle, direction : int = 0):
        if v.id in [i.id for i in self.crossed]+[i.id for i in self.uncrossed]+[i.id for i in self.previous_c]+[i.id for i in self.previous_unc]:
            return
        if not direction:
            #print(f"cross {v._class} ({v.id})")
            self.crossed.append(v)
        else:
            #print(f"uncross {v._class} ({v.id})")
            self.uncrossed.append(v)
