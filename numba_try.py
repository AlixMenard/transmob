import numpy as np
import time
from numba import cuda
from random import randint
import matplotlib.pyplot as plt

def benchmark(size):
    def create_list(size):
        # Create an array of zeros with shape (size, 4)
        L = np.zeros((size, 4), dtype=np.int32)

        for i in range(size):
            x1, y1 = randint(0, 630), randint(0, 630)
            x2, y2 = randint(x1, 640), randint(y1, 640)

            # Assign the values directly to the array
            L[i] = [x1, y1, x2, y2]

        return L

    list1 = create_list(size)
    list2 = create_list(size)
    print("box created", size)

    def box_overlap_cpu(list1, list2):
        overlaps = np.zeros((list1.shape[0], list2.shape[0]), dtype=np.float32)
        for i in range(list1.shape[0]):
            for j in range(list2.shape[0]):
                xmin1, ymin1, xmax1, ymax1 = list1[i]
                xmin2, ymin2, xmax2, ymax2 = list2[j]
                ixmin = max(xmin1, xmin2)
                iymin = max(ymin1, ymin2)
                ixmax = min(xmax1, xmax2)
                iymax = min(ymax1, ymax2)
                width = max(0, ixmax - ixmin)
                height = max(0, iymax - iymin)
                overlaps[i, j] = width * height
        return overlaps

    # Measure CPU time
    start_cpu = time.time()
    overlaps_cpu = box_overlap_cpu(list1, list2)
    end_cpu = time.time()
    cpu_dur = end_cpu - start_cpu

    @cuda.jit
    def box_overlap_kernel(list1, list2, overlaps):
        # Get 2D grid indices
        ix, iy = cuda.grid(2)  # The first index is the fastest dimension
        threads_per_grid_x, threads_per_grid_y = cuda.gridsize(2)  # threads per grid dimension
        n0, n1 = list1.shape(0), list2.shape(0)
        for i in range(iy, n0, threads_per_grid_y):
            for j in range(ix, n1, threads_per_grid_x):
                xmin1, ymin1, xmax1, ymax1 = list1[i]
                xmin2, ymin2, xmax2, ymax2 = list2[j]
                ixmin = max(xmin1, xmin2)
                iymin = max(ymin1, ymin2)
                ixmax = min(xmax1, xmax2)
                iymax = min(ymax1, ymax2)
                width = max(0, ixmax - ixmin)
                height = max(0, iymax - iymin)
                overlap_area = width * height
                overlaps[i, j] = overlap_area


    # Transfer data to the GPU
    list1_gpu = cuda.to_device(list1)
    list2_gpu = cuda.to_device(list2)
    # Define the thread and block size
    threads_per_block = (16, 16)
    blocks_per_grid = ((list1_gpu.shape[0] + threads_per_block[0] - 1) // threads_per_block[0],
                       (list2_gpu.shape[0] + threads_per_block[1] - 1) // threads_per_block[1])


    # Initialize an array on the GPU to hold the overlap results
    overlaps_gpu = cuda.device_array((list1_gpu.shape[0], list2_gpu.shape[0]), dtype=np.float32)
    box_overlap_kernel[blocks_per_grid, threads_per_block](list1_gpu, list2_gpu, overlaps_gpu) #?Pre-compile

    # Initialize the GPU execution
    start_gpu = time.time()
    # Launch the kernel
    box_overlap_kernel[blocks_per_grid, threads_per_block](list1_gpu, list2_gpu, overlaps_gpu)

    # Copy the results back to the host
    overlaps_gpu2cpu = overlaps_gpu.copy_to_host()

    end_gpu = time.time()

    return cpu_dur, end_gpu - start_gpu

cpus = []
gpus = []
x= []
for i in range(7):
    cpu, gpu = benchmark(10**i)
    cpus.append(cpu)
    gpus.append(gpu)
    x.append(10**i)
plt.plot(x, cpus)
plt.plot(x, gpus)
plt.show()