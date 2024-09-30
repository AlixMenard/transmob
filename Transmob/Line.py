import numpy as np
from .Vehicle import Vehicle
from typing import Dict, List

class Line:

    nb_lines = 0

    def __init__(self, x1, y1, x2, y2, x3, y3):

        self.maskbound = None
        self.id = Line.nb_lines
        Line.nb_lines += 1
        self.counter = Counter()
        self.vehicles : Dict[int, float] = {}

        if x1>x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        self.start = (x1, y1)
        self.center = (int((x1+x2)/2), int((y1+y2)/2))
        self.end = (x2, y2)
        self.p3 = (x3,y3)
        dx, dy = abs(x2-x1), abs(y2-y1)
        self.length = np.sqrt(dx**2 + dy**2)
        self.bounds = [x1-0.1*self.length, x2+0.1*self.length, min(y1, y2)-0.1*self.length, max(y1, y2)+0.1*self.length]

        #! ax + by + c = 0
        if dx == 0:
            self.a = 1
            self.b = 0
            self.c = -x1
        else:
            self.a = -dy/dx
            self.b = 1
            self.c = - y1 - self.a*x1

        lg = np.sqrt(self.a**2+self.b**2)
        
        self.vec = (-self.b/lg, self.a/lg)
        self.normal = (-self.a/lg, -self.b/lg)

        #! Matrice de chanement de base P = [vec^t, normal^t]
        self.P = np.array([[self.vec[0], self.normal[0]],
                           [self.vec[1], self.normal[1]]])
        
        self.Pt = np.linalg.inv(self.P)
        x3, y3 = x3-self.center[0], y3-self.center[1]
        x3, y3 = map(int, np.dot(self.Pt, np.array([x3, y3])))
        self.direction = y3/abs(y3)

        self.mask_bound()

    def mask_bound(self):
        margin = 2/3
        self.maskbound = [
            self.center[0] - self.length * margin,  # left
            self.center[1] - self.length * margin,  # top
            self.center[0] + self.length * margin,  # right
            self.center[1] + self.length * margin   # bottom
                        ]
        self.maskbound = list(map(int, self.maskbound))

    def cleanse(self):
        self.counter.cleanse()

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


    def proj(self, x, y):
        x, y = map(int, np.dot(self.Pt, np.array([x, y])))
        y *= self.direction
        return x, y
    
    def unproj(self, x, y):
        y *= self.direction
        x, y = map(int, np.dot(self.P, np.array([x, y])))
        return x, y
    
    def inbound(self, x, y):
        return self.bounds[0]<=x<=self.bounds[1] and self.bounds[2]<=y<=self.bounds[3]

    def cross(self, v : Vehicle):
        x, y = v.box.center
        x, y = x-self.center[0], y-self.center[1]
        _, p = self.proj(x, y)
        if v.id in self.vehicles and (p * self.vehicles[v.id]<0 or p ==0):
            if self.vehicles[v.id]<0:
                self.counter.add(v, direction = 0)
                v.cross(self.id)
            else:
                self.counter.add(v, direction = 1)
                v.cross(-self.id)
        self.vehicles[v.id] = p


class Counter:

    def __init__(self):
        self.crossed : List[Vehicle] = []
        self.uncrossed : List[Vehicle] = []
    
    def cleanse(self):
        self.crossed.clear()
        self.uncrossed.clear()
    
    def count(self, classes=None, include_none:bool = False):
        if classes is None:
            classes = []
        if not classes :
            uniques = list(set([v._class for v in self.crossed]))
            dir_in = {}
            for u in uniques:
                dir_in[u] = sum([1 for v in self.crossed if v._class == u and v.oldid is None])
            
            uniques = list(set([v._class for v in self.uncrossed]))
            dir_out = {}
            for u in uniques:
                dir_out[u] = sum([1 for v in self.uncrossed if v._class == u and v.oldid is None])
            if not include_none:
                if None in dir_in:dir_in.pop(None)
                if None in dir_out:dir_out.pop(None)
            return [dir_in, dir_out]

    def add(self, v : Vehicle, direction : int = 0):
        if v.id in [i.id for i in self.crossed]+[i.id for i in self.uncrossed]:
            return
        if not direction:
            #print(f"cross {v._class} ({v.id})")
            self.crossed.append(v)
        else:
            #print(f"uncross {v._class} ({v.id})")
            self.uncrossed.append(v)
