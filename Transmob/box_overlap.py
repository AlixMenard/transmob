from .Box import Box as vBox
import numpy as np

def overlap(people:np.array, bikes:np.array, matrix:np.array):
    # ! expects np arrays
    for i in range(people.shape[0]):
        for j in range(bikes.shape[0]):
            xmin1, ymin1, xmax1, ymax1 = list1[i].box.xyxy
            xmin2, ymin2, xmax2, ymax2 = list2[j].box.xyxy
            ixmin = max(xmin1, xmin2)
            iymin = max(ymin1, ymin2)
            ixmax = min(xmax1, xmax2)
            iymax = min(ymax1, ymax2)
            width = max(0, ixmax - ixmin)
            height = max(0, iymax - iymin)
            S1 = (xmax1 - xmin1) * (ymax1 - ymin1)
            S2 = (xmax2 - xmin2) * (ymax2 - ymin2)
            I = width * height
            U = S1 + S2 - I
            matrix[i,j] = I/2 > 0.75