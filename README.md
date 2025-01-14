# transmob
[Yolov11](https://github.com/ultralytics/ultralytics) based vehicle tracking solution\
Languages : [![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/AlixMenard/transmob/blob/main/README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/AlixMenard/transmob/blob/main/README.fr.md)

#### Installation
Follow the instructions in [Install](https://github.com/AlixMenard/transmob/blob/main/INSTALL.md).

### Start option 1
- Go to the *transmob* folder.
- Run "start.vbs". After the first use, a shortcut will be created on the Desktop for easier access.
- The process will update, then start, no worries if it is a little long.
### Start option 2
- Open a powershell/commandline shell : win+r, type "powershell" or "cmd", enter
- Navigate to the git repository (at *<previous_path>/transmob*). See [Install](https://github.com/AlixMenard/transmob/blob/main/INSTALL.md) for more info about shell navigation.
- Execute `py GUI.py`
### Use
- Drag&Drop the folder containing the videos to process (**every** video will be processed, make sure to eliminate duplicates, even with different extension, like "file.mp4" and "file.lrv")
- Choose the fitting options
  - `Nombre de frames` : 1, each frame will be processed, 2, one in two frames will be processed (twice as fast, reduces detection rate, heavily not recommended in case of low quality video)
  - `Model YOLO` : bigger models will be better, but slower in most cases. With CUDA support the slow-down is negligible and always using the model of size *x* is highly recommended
  - `Types de véhicules` : Vehicle types to count, the others will be ignored. If pedestrians (*person*) are monitored, *bicycle* and *motorbike* can't be ignored.
  - `Avec vidéo` : If yes, the videos will be displayed as they are treated. This considerably slows down the process. It is however useful to test the quality of detection of a model size if you are unsure about the picture quality.
  - `Avec captures d'écran` : This will keep a screenshot of every counted vehicule, with its class, for verification purposes or further analysis.
  - `Un seul setup` : If yes, only the first video of the folder will be shown to trace the counting lines. Every other video will have the exact same lines.
  - `Valider les lignes` (if `Un seul setup` is selected) : The lines will be transfered to every video in the folder, but shown to enable modifications.
- Start
- For each video :
  - A small window will appear to confirm the video starting time. The window's name corresponds to the video's title. The window displays the estimated time the video was recorded, based on the file's creation date. If correct, click on "Valider", and the program will then consider the estimated time of every other video in the folder to be correct. If not, type in the correct time **entirely**, the format must be respected.
  - The 1st frame be displayed to create the counting lines. It takes 3 clicks to create a single line : the first 2 clicks define the starting and ending points of the line, the 3rd click defines the direction of counting. At an intersection, it is recommended to do the 3rd click in the middle of the intersection.\
    **/!\\** *The first 2 clicks defining the line through which vehicles will be counted, they must be accurate so not to miss vehicles or count additional ones. However, the 3rd click's accuracy is not to worry about. In case multiple lines are placed, the order has to be consistent across all videos.*
  - After defining all the lines on the picture, press `Enter` to validate and repeat the process for every video.
- Once no more video is shown, the setup is over and the program will process every video on its own. Do not open the `results.txt` during the process, as it could prevent the program from writing the result and freeze it. \
*Note : If python commands such as `py GUI.py` do not work, try replacing `py` with `python` (e.g. `python GUI.py`)*

### Good practice
- Folder and file names must not include spaces and special characters
- On complex intersections, such as roundabouts, make sure to place the lines such that vehicles engaged in the intersection and passing by a line will not be considered as passing the line
- Be sure to cover the whole potential crossing area, especially around crosswalks, where people might walk around and not exactly on
- ~MP4 and LRV will give the same results, as the model scales the resolution down before processing. However, LRV files are much lighter on the CPU and the memory.~ MP4 files are more robust to compressing than LRV to decompressing, and performs better under SAHI.

### Additional tools
Additional useful tools are made available. You can access them by opening a shell and navigating to the project folder (see [the installation part](#Install) for more information about shell navigation). Then execute `py Tools.py` (or `python Tools.py`) to open a window presenting the different tools.
The tools include :
- Results formatting
- Video renaming
- Video splitting
- Results aggregation
- Video repair\
More details are available [here](https://github.com/AlixMenard/transmob/blob/main/Tools.md)

## ~~transmob~~

Yolo object detection, SORT tracking.\
Paralleled video processing.

## ~~transmobNT~~

Yolo object detection, SORT tracking.\
Paralleled video processing.\
Nested Threads for processing (frame processing // tracking) \
**/!\\** *Graph version must not be interrupted before video is fully processed. Otherwise, a restart will be necessary.*

## transmobYT

Yolo object detection, Yolo tracking via BoT-SORT.\
Paralleled video processing.

## transmobYTC

Yolo object detection, Yolo tracking via BoT-SORT.\
YOLO and additional processes running on CUDA\
CUDA usage prevents paralleled processing, serialized is de facto used.\
CUDA performances allow for further discrimancy of *trucks & cars* into *trucks & cars & vans*.

## Notes
- Classic and NT versions are discontinued for efficiency reasons
- Performance is to be enhanced with SAHI -> Implement BoTSORT and ReId independently from YOLO

### Performances
**Precision :** transmob == transmobNT < transmobYT == transmobYTC

**Discrimination of vans vs cars & trucks :** 
- Standalone model, retrained with COCO and additional data on vans, performs poorly (84% of vans are still categorized as car/truck). The original COCO dataset might already contain several vans listed as one or the other, and/or the additional van dataset is too scarce in comparison to COCO dataset. 
- Additional model, trained specifically on vans dataset, recognizes with high conficence vans, allowing for a confidence comparison between the original detection on yolo11 and the second detection with this model. On validation tests, by comparing the COCO-trained YOLO model and the standalone model confidence on pictures of cars and trucks (from COCO) and vans (from the additional data set), a 90% discrimination accuracy is achieved by setting a confidence ratio (YOLO/standalone) threshold of approximately `1.08211`. (Above the threshold, COCO-trained YOLO primes, under it, the vehicle is categorised as a van)

**Speed :** transmobYTC >> transmobYT > transmobNT >= transmob \
YTC almost doesn't scale based on model size, very efficient, others scale on a q\~=1.3 ratio \
Videos can be processed every 2 frames to speed up. On low quality, every frame is necessary.
Before van discrimination, process time was approximately lowered by 25% compared to the video running time. More data is necessary for processing with van discrimination.

**models :** (best case, my computer)
From lightest to heaviest : *n*, *s*, *m*, *l*, *x*. \
*m* and above reach perfect detection on single frame with YT and YTC, while *n* is around ~95% and *s* is estimated above 97%. \
With double frame, models are located between 80% and 95% (estimate of max), with (surprisingly) the best performance for *l*.

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
- [X] Memory efficient playlisting
- [X] Discriminate SUV (large cars), vans and trucks
- [ ] Implement ReId to prevent track loss
- [ ] Directional process


### Legal
As Yolo is under an [AGPL-3.0 License](https://firebasestorage.googleapis.com/v0/b/ultralytics-public-site.appspot.com/o/license%2FAGPL-3.0-Software-License.pdf?alt=media), so is this work. In shortterms, it can be used for commercial reasons inside the company's area, and cannot be a hosted service available to public or private users. In such case, the whole source code has to be made available to the users.

This project used the [COCO dataset](https://cocodataset.org/#home) and the additional [Maryam Mahmood](https://universe.roboflow.com/maryam-mahmood-6hoeq/vans/dataset/3) van dataset to further train the YOLO model.


The object detection uses [SAHI method](https://pypi.org/project/sahi/) and the object tracking relies on [BoT-SORT](https://github.com/NirAharon/BoT-SORT) implemented as [BoxMOT](https://github.com/mikel-brostrom/boxmot). 
<a name="FastReId"></a>
Vehicle tracking is enhanced with [FastReId](https://github.com/JDAI-CV/fast-reid) (model available [here](https://github.com/JDAI-CV/fast-reid/releases/download/v0.1.1/veriwild_bot_R50-ibn.pth), trained on [VeRi-Wild](https://github.com/PKU-IMRE/VERI-Wild)) (Although not listed on [PWC](https://paperswithcode.com/), FastReId outperforms most methods available on the website on most datasets).
