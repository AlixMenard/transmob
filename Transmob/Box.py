class Box:
    def __init__(self, x, y, w, h):
        self.center = [x + w/2, y + h/2]
        self.cross_point = [x + w/2, y + 3*h/4]
        self.xywh = [x, y, w, h]
        self.xyxy = [x, y, x+w, y+h]
    
    @property
    def area(self):
        return self.xywh[2]*self.xywh[3]
