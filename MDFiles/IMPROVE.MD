# Here are guidelines to make improvements to the program

## Yolo version

In case a new more performing YOLO version is released, download the weights and put them in the `weights` folder. Then in `GUI.py`, modify this line :
![Yolo version](images/YOLO_version.png?raw=true "Yolo version")
You need to change the generic version on the yolo models (e.g. `yolov8{m}.pt` or `yolo11{m}.pt`). The `{m}` placeholder will change automatically depending on the model size chosen when running. *Check the name of the new version's models to ensure writing in the right generic version.

## Tracking parameters

The vehicle tracking is done using BoT-SORT. The parameters are available in `TransmobYTC/Analyze.py` (for GPU version, otherwise `TransmobYT/Analyze.py`) at the lines :
![YTC tracker](images/Tracker_YTC.png?raw=true "YTC tracker") ![YT tracker](images/Tracker_YT.png?raw=true "YTC tracker")
