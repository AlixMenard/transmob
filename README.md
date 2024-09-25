# transmob
Yolo based vehicle tracking solution

## Installation
### Pre-requisite
- Python >= 3.12
- git
### Optionnal
If the computer has a [CUDA compatible graphic card](https://en.wikipedia.org/wiki/CUDA#GPUs_supported), you need to download and install [NVIDIA CUDA toolkit](https://developer.nvidia.com/cuda-downloads).
A CUDA comaptible graphic card is highly recommended for increased speed performances.

### Install
- Open a powershell/commandline shell : win+r, type "powershell" or "cmd", enter
- Navigate to the desired place to store the algorithm (use `cd <folder_name>` to navigate)
- Execute `git clone https://github.com/AlixMenard/transmob`
- Go in the repository : `cd transmob`
- Install the necessary packages : `pip install -r requiremetns.txt`

### Use
- Open a powershell/commandline shell : win+r, type "powershell" or "cmd", enter
- Navigate to the git repository (at *<previous_path>/transmob*)
- Execute `py GUI.py`
- Drag&Drop the folder containing the videos to process (every video will be processed, make sure to eliminate duplicates, even with different extension, like "file.mp4" and "file.lrv")
- Choose the fitting options
- Start and let the program run

## transmob

Yolo object detection, SORT tracking.\
Paralleled video processing.

## transmobNT

Yolo object detection, SORT tracking.\
Paralleled video processing.\
Nested Threads for processing (frame processing vs tracking)

## transmobYT

Yolo object detection, Yolo tracking.\
Paralleled video processing.\

## transmobYTC

Yolo object detection, Yolo tracking.\
Paralleled video processing.\
YOLO runs on CUDA

### Performances
**Precision :** transmob == transmobNT < transmobYT == transmobYTC \
**Speed :** transmobYTC > transmobYT \~= transmobNT > transmob \
YTC almost doesn't scale based on model size, very efficient, others scale on a q\~=1.3 ratio \
Videos can be processed every 2 frames to speed up. On low quality, every frame is necessary.

**models :** (best case, my computer)
- n : half time with double framing
- s
- m : 
- l
- x : slightly faster than real time with double framing

### todo
- [x] file sorting for better core workload share 
- [X] adapt to cuda devices
- [X] benchmark (except model x, too long)
- [ ] Make sure person + bicycle -> bicycle only (same with motorbikes)
- [ ] &emsp;└> running on CUDA with Numba
- [ ] &emsp;&emsp;&emsp;└> benchmark numba's efficiency
- [ ] Try nested thread on YTC
- [ ] Directional process
