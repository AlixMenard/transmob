from .Box import Box as vBox
import numpy as np
import cv2

def overlap(people:np.array, bikes:np.array, matrix:np.array):
    # ! expects np arrays
    for i in range(people.shape[0]):
        for j in range(bikes.shape[0]):
            xmin1, ymin1, xmax1, ymax1 = people[i].box.xyxy
            dx1, dy1 = xmax1 - xmin1, ymax1 - ymin1
            xmin2, ymin2, xmax2, ymax2 = bikes[j].box.xyxy
            dx2, dy2 = xmax2 - xmin2, ymax2 - ymin2

            ymin1+=int(dy1/2)
            xmin2+=int(dx2/5)
            xmax2-=int(dx2/5)
            ymax2-=int(dy2/3)
            #cv2.rectangle(frame, (xmin1, ymin1), (xmax1, ymax1), (0,255,0), 2)
            #cv2.rectangle(frame, (xmin2, ymin2), (xmax2, ymax2), (0,255,0), 2)

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
            matrix[i,j] = I / U > 0.6 or I / S1 > 0.7 or I / S2 > 0.7