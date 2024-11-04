# transmob
[Yolov11](https://github.com/ultralytics/ultralytics) based vehicle tracking solution\
Languages : [![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/AlixMenard/transmob/blob/main/README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/AlixMenard/transmob/blob/main/README.fr.md)

## Installation
### Pre-requisite
- <a href="https://www.python.org/downloads/release/python-3127/" target="_blank">Python = 3.12</a>
- [Python = 3.12](https://www.python.org/downloads/release/python-3127/)
- [git](https://git-scm.com/downloads/win)
### Optionnal
If the computer has a [CUDA compatible graphic card](https://en.wikipedia.org/wiki/CUDA#GPUs_supported), you need to download and install [NVIDIA CUDA toolkit](https://developer.nvidia.com/cuda-downloads).\
During the next step, after installing the required modules, you need to uninstall pytorch modules (`pip uninstall torch torchvision torchaudio`) and re-install it with CUDA support on the [Pytorch Website](https://pytorch.org/get-started/locally/). Select the *Stable* version, the correct OS, *pip*, *python* and a *CUDA SDK version* ([see here for graphic card/version compatibility](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)), then copy and execute the command given by the website.\
A CUDA compatible graphic card is highly recommended for increased speed performances.

### Install
- Open a powershell/commandline shell : win+r, type "powershell" or "cmd", enter
- Navigate to the desired place to store the algorithm (use `cd <folder_name>` to navigate)
- Execute `git clone https://github.com/AlixMenard/transmob`
- Go in the repository : `cd transmob`
- Install the necessary packages : `pip install -r requirements.txt`\
\* This will install the yolo models of sizes *n*, *s*, *m* and *l*. On the first time you ask the program to use the model of size *x*, it will be automatically downloaded before processing.

### Start option 1
- Open a powershell/commandline shell : win+r, type "powershell" or "cmd", enter
- Navigate to the git repository (at *<previous_path>/transmob*)
- Execute `py GUI.py`
### Start option 2
- Go to the *transmob* folder.
- Run "start.vbs". After the first use, a shortcut will be created on the Desktop for easier access.
- The process will update, then start, no worries if it is a little long.
### Use
- Drag&Drop the folder containing the videos to process (**every** video will be processed, make sure to eliminate duplicates, even with different extension, like "file.mp4" and "file.lrv")
- Choose the fitting options
  - Process (explained below)
  - Frame number : 1, each frame will be processed, 2, one in two frames will be processed (twice as fast, reduces detection rate, heavily not recommended in case of low quality video)
  - YOLO model : bigger models will be better, but slower in most cases. With CUDA support the slow-down is negligible and always using the model of size *x* is highly recommended
  - Classes : Vehicle types to count, the others will be ignored. If pedestrians (*person*) are monitored, *bicycle* and *motorbike* can't be ignored.
  - Number of cores dedicated to the process. If the computer has 10 physical cores or more, the recommendations are *Classic (4)*, *Nested Threads (3)* and *YallO (4)*.
  - With video : If yes, the videos will be displayed as they are treated. This considerably slows down the process. It is however useful to test the quality of detection of a model size if you are unsure about the picture quality.
- Start
- The 1st frame of each video will be displayed successively to create the counting lines. It takes 3 clicks to create a single line : the first 2 clicks define the starting and ending points of the line, the 3rd click defines the direction of counting. At an intersection, it is recommended to do the 3rd click in the middle of the intersection. **/!\\** *The first 2 clicks defining the line through which vehicles will be counted, they must be accurate so not to miss vehicles or count additional ones. However, the 3rd click's accuracy is not to worry about. In case multiple lines are placed, the order has to be consistent across all videos.*
- Along with the first frame, a pop-up will be displayed to assess the video's start time. The program will show the time the video was created as a first proposition, which you can confirm using "Valider". If that time is not correct, you can type the actual start time in the entry, in the format (yyyy-mm-dd hh:mm), then click "Changer".
- After defining all the lines on the picture, press `Enter` to validate and repeat the process for every video.
- Once no more video is shown, the setup is over and the program will process every video on its own. Do not open the `results.txt` during the process, as it could prevent the program from writing the result and freeze it. \
*Note : If python commands such as `py GUI.py` do not work, try replacing `py` with `python` (e.g. `python GUI.py`)*

### Good practice
- Folder and file names must not include spaces and special characters
- On complex intersections, such as roundabouts, make sure to place the lines such that vehicles engaged in the intersection and passing by a line will not be considered as passing the lines
- Be sure to cover the whole potential crossing area, especially around crosswalks, where people might walk around and not exactly on
- MP4 and LRV will give the same results, as the model scales the resolution down before processing. However, LRV files are much lighter on the CPU and the memory.

## transmob

Yolo object detection, SORT tracking.\
Paralleled video processing.

## transmobNT

Yolo object detection, SORT tracking.\
Paralleled video processing.\
Nested Threads for processing (frame processing // tracking) \
**/!\\** *Graph version must not be interrupted before video is fully processed. Otherwise, a restart will be necessary.*

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
From lightest to heaviest : *n*, *s*, *m*, *l*, *x*. \
*m* and above reach perfect detection on single frame with YT and YTC, while *n* is around ~95% and *s* is estimated above 97%. \
With double frame, models are located between 80% and 95% (estimate of max), with the best performance for *l*.

### todo
- [x] file sorting for better core workload share 
- [X] adapt to cuda devices
- [X] benchmark (except model x, too long)
- [x] Make sure person + bicycle -> bicycle only (same with motorbikes)
  - [x] └> running on CUDA with Numba
    - [X] └> benchmark numba's efficiency
- [x] ~Try nested thread on YTC~ *Threading doesn't work with CUDA*
- [X] Screenshot passing vehicles on all processes
- [X] Fast setup for multiple pictures with same POV
- [X] Cancel line creation if mistake made
- [ ] Directional process


### Legal
As Yolo is under an [AGPL-3.0 License](https://firebasestorage.googleapis.com/v0/b/ultralytics-public-site.appspot.com/o/license%2FAGPL-3.0-Software-License.pdf?alt=media), so is this work. In shortterms, it can be used for commercial reasons inside the company's area, and cannot be a hosted service available to public or private users. In such case, the whole source code has to be made available to the users.

This project used the [COCO dataset](https://cocodataset.org/#home) and the additional [Maryam Mahmood](https://universe.roboflow.com/maryam-mahmood-6hoeq/vans/dataset/3) van dataset to further train the YOLO model.
