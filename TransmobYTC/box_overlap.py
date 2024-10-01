from numba import cuda
import numpy as np

@cuda.jit
def overlap(people, bikes, matrix):
    ix, iy = cuda.grid(2)
    threads_per_grid_x, threads_per_grid_y = cuda.gridsize(2)
    n0, n1 = people.shape[0], bikes.shape[0]
    for i in range(iy, n0, threads_per_grid_y):
        for j in range(ix, n1, threads_per_grid_x):
            xmin1, ymin1, xmax1, ymax1 = people[i]
            dx1, dy1 = xmax1 - xmin1, ymax1 - ymin1
            xmin2, ymin2, xmax2, ymax2 = bikes[j]
            dx2, dy2 = xmax2 - xmin2, ymax2 - ymin2

            ymin1 += dy1 / 2
            xmin2 += dx2 / 5
            xmax2 -= dx2 / 5
            ymax2 -= dy2 / 3

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
            matrix[i, j] = I / U > 0.6 or I / S1 > 0.7 or I / S2 > 0.7