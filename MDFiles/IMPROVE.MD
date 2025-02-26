# Here are guidelines to make improvements to the program

## Yolo version

In case a new more performing YOLO version is released, download the weights and put them in the `weights` folder. Then in `GUI.py`, modify this line :
<p align="center">
  <figure style="display: inline-block; text-align: center; margin: 0 10px;">
    <img src="images/YOLO_version.png?raw=true" alt="Yolo version" title="Yolo version" width="45%"/>
    <figcaption style="font-size: 0.9em;">Yolo version</figcaption>
  </figure>
</p>
You need to change the generic version on the yolo models (e.g. `yolov8{m}.pt` or `yolo11{m}.pt`). The `{m}` placeholder will change automatically depending on the model size chosen when running. *Check the name of the new version's models to ensure writing in the right generic version.

## Tracking parameters

The vehicle tracking is done using BoT-SORT. The parameters are available in `TransmobYTC/Analyze.py` (for GPU version, otherwise `TransmobYT/Analyze.py`) at the lines :
<p align="center">
  <figure style="display: inline-block; text-align: center; margin: 0 10px; width=45%">
    <img src="images/Tracker_YTC.png?raw=true" alt="YTC tracker" title="YTC tracker" width="45%"/>
    <figcaption style="font-size: 0.9em;">YTC Tracker</figcaption>
  </figure>
  <figure style="display: inline-block; text-align: center; margin: 0 10px; width=45%">
    <img src="images/Tracker_YT.png?raw=true" alt="YT tracker" title="YT tracker" width="45%"/>
    <figcaption style="font-size: 0.9em;">YT Tracker</figcaption>
  </figure>
</p>
