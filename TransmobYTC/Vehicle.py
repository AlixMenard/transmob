from .Box import Box as vBox
from typing import Dict, List
import numpy as np

class Vehicle:

    def __init__(self, id:int, box:vBox, _class:str, conf:float, frame:int, fleet):
        self.id : int = id
        self.fleet = fleet
        self.crossed : List[int] = []
        self.hist_conf : List[(str, float)] = []
        self._class : str = _class 
        self.conf : float = conf
        self.box : vBox = box
        self.last_frame = frame
        self.coords : List[int] = [self.box.center]
        self.speeds : List[float] = []
    
    def class_check(self):
        classes : Dict[str|None, float] = {}
        temp_save = self._class
        for _class, conf in self.hist_conf:
            if _class in classes:
                classes[_class] += conf
            else:
                classes[_class] = conf
        if len(classes.keys())<1 and None in classes.keys():
            classes.pop(None)
        self._class = max(zip(classes.values(), classes.keys()))[1]
        if self._class is None and not temp_save is None:
            self._class = temp_save
        if self._class == "person" and (self.is_fast or self.close_speed("car")):
            self._class = "scooter"

    def cross(self, id:int):
        self.crossed.append(id)

    def update(self, box:vBox, _class:str, conf:float, frame:int):
        dt = frame - self.last_frame
        x1,y1 = self.box.center
        x2,y2 = box.center
        dx  = x2-x1
        dy = y2-y1
        ds = np.sqrt(dx**2 + dy**2)
        self.speeds.append(ds/dt)
        self.speeds = self.speeds[0:15]

        self.box = box
        self.last_frame = frame
        self.coords.append(self.box.center)
        self.hist_conf.append((_class, conf))
        self.hist_conf = self.hist_conf[:15]

        if _class != self._class:
            self.class_check()

    def close_speed(self, _class):
        avg, std = self.fleet.speed(_class)
        if avg and std:
            return self.avg_spd >= avg - 2*std and self.avg_spd <= avg + 2*std
        else:
            return False

    @property
    def is_fast(self):
        avg, std = self.fleet.speed(self._class)
        #print(avg, std, self.avg_spd)
        if avg and std:
            return self.avg_spd >= avg + 3*std
        else:
            return False

    @property
    def avg_spd(self):
        return np.average(self.speeds) if self.speeds else 0

class Fleet:

    def __init__(self):
        self.vehicles: Dict[int, Vehicle] = {}
    
    def add_vehicle(self, id:int, box:vBox, _class:str, conf:float, frame:int):
        v = Vehicle(id, box, _class, conf, frame, self)
        self.vehicles[id] = v
    
    def update_vehicle(self, id:int, box:vBox, _class:str, conf:float, frame:int) -> None:
        if id in self.ids:
            v = self.vehicles[id]
            v.update(box, _class, conf, frame)
    
    def cleanse(self, ids:List[int]):
        temp = self.vehicles.keys()
        vehicles = {}
        for id in temp:
            if id in ids:
                vehicles[id] =self.vehicles[id]
        del self.vehicles
        self.vehicles = vehicles
        del vehicles

    def get(self, id:int) -> Vehicle:
        return self.vehicles[id]

    def speed(self, _class:str):
        l = [self.vehicles[v].avg_spd for v in self.vehicles if self.vehicles[v]._class == _class and not np.isnan(self.vehicles[v].avg_spd)]
        return np.average(l) if l else None, np.std(l) if l else None

    @property
    def ids(self) -> List[int]:
        return [v[1].id for v in self.vehicles.items()]