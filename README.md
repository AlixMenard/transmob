# transmob
[Yolo](https://github.com/ultralytics/ultralytics) based vehicle tracking solution\
Languages : [![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/AlixMenard/transmob/blob/main/README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/AlixMenard/transmob/blob/main/README.fr.md)

## Installation
### Pre-requisite
- Python >= 3.12
- git
### Optionnal
If the computer has a [CUDA compatible graphic card](https://en.wikipedia.org/wiki/CUDA#GPUs_supported), you need to download and install [NVIDIA CUDA toolkit](https://developer.nvidia.com/cuda-downloads).\
During the next step, after installing the required modules, you need to uninstall pytorch modules (`pip uninstall torch torchvision torchaudio`) and re-install it with CUDA support on the [Pytorch Website](https://pytorch.org/get-started/locally/). Select the *Stable* version, the correct OS, *pip*, *python* and a *CUDA version*, then copy and execute the command given by the website.\
A CUDA compatible graphic card is highly recommended for increased speed performances.

### Install
- Open a powershell/commandline shell : win+r, type "powershell" or "cmd", enter
- Navigate to the desired place to store the algorithm (use `cd <folder_name>` to navigate)
- Execute `git clone https://github.com/AlixMenard/transmob`
- Go in the repository : `cd transmob`
- Install the necessary packages : `pip install -r requirements.txt`\
\* This will install the yolo models of sizes *n*, *s*, *m* and *l*. On the first time you ask the program to use the model of size *x*, it will be automatically downloaded before processing.

### Use
- Open a powershell/commandline shell : win+r, type "powershell" or "cmd", enter
- Navigate to the git repository (at *<previous_path>/transmob*)
- Execute `py GUI.py`
- Drag&Drop the folder containing the videos to process (**every** video will be processed, make sure to eliminate duplicates, even with different extension, like "file.mp4" and "file.lrv")
- Choose the fitting options
  - Process (explained below)
  - Frame number : 1, each frame will be processed, 2, one in two frames will be processed (twice as fast, heavily not recommended in case of low quality video)
  - YOLO model : bigger models will be better, but slower in most cases. With CUDA support the slow-down is negligible and always using the model of size *x* is highly recommended
  - Classes : Vehicle types to count, the others will be ignored. If pedestrians (*person*) are monitored, *bicycle* and *motorbike* can't be ignored.
  - Number of cores dedicated to the process. If the computer has 10 physical cores or more, the recommendations are *Classic (4)*, *Nested Threads (3)* and *YallO (4)*.
  - With video : If yes, the videos will be displayed as they are treated. This considerably slows down the process. It is however useful to test the quality of detection of a model size if you are unsure about the picture quality.
- Start
- The 1st frame of each video will be displayed successively to create the counting lines. It takes 3 clicks to create a single line : the first 2 clicks define the starting and ending points of the line, the 3rd click defines the direction of counting. At an intersection, it is recommended to do the 3rd click in the middle of the intersection. **/!\\** *The first 2 clicks defining the line through which vehicles will be counted, they must be accurate so not to miss vehicles or count additional ones. However, the 3rd click's accuracy is not to worry about.*
- After defining all the lines on the picture, press `Enter` to validate and repeat the process for every video.
- Once no more video is shown, the setup is over and the program will process every video on its own.

## transmob

Yolo object detection, SORT tracking.\
Paralleled video processing.

## transmobNT

Yolo object detection, SORT tracking.\
Paralleled video processing.\
Nested Threads for processing (frame processing // tracking) \
*graph version should not be interrupted before video is fully processed*

## transmobYT

Yolo object detection, Yolo tracking via BoT-SORT.\
Paralleled video processing.\

## transmobYTC

Yolo object detection, Yolo tracking via BoT-SORT.\
YOLO and additional processes running on CUDA\
CUDA usage prevents paralleled processing, serialized is de facto used.

### Performances
**Precision :** transmob == transmobNT < transmobYT == transmobYTC \
**Speed :** transmobYTC >> transmobYT > transmobNT >= transmob \
YTC almost doesn't scale based on model size, very efficient, others scale on a q\~=1.3 ratio \
Videos can be processed every 2 frames to speed up. On low quality, every frame is necessary.

**models :** (best case, my computer)
- n : half-time with double framing
- s :
- m : 
- l :
- x : slightly faster than real time with double framing

### todo
- [x] file sorting for better core workload share 
- [X] adapt to cuda devices
- [X] benchmark (except model x, too long)
- [ ] Make sure person + bicycle -> bicycle only (same with motorbikes)
- [ ] &emsp;└> running on CUDA with Numba
- [X] &emsp;&emsp;&emsp;└> benchmark numba's efficiency
- [ ] ~Try nested thread on YTC~ *Threading doesn't work with CUDA*
- [ ] Screenshot passing vehicles
- [ ] Directional process
