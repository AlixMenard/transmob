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

### Lines for modification

The vehicle tracking is done using BoT-SORT. The parameters are available in `TransmobYTC/Analyze.py` (for GPU version, otherwise `TransmobYT/Analyze.py`) at the lines :
<table>
  <tr>
    <td align="center" width="45%">
      <img src="images/Tracker_YTC.png?raw=true" alt="YTC tracker" title="YTC tracker"/>
      <br/><sub>YTC Tracker</sub>
    </td>
    <td align="center" width="45%">
      <img src="images/Tracker_YT.png?raw=true" alt="YT tracker" title="YT tracker"/>
      <br/><sub>YT Tracker</sub>
    </td>
  </tr>
</table>

### Tracker Parameters

| General Settings      | Detection & Tracking        | Matching Criteria        |
|----------------------|----------------------------|--------------------------|
| **`reid_weights`**: Path to ReID model weights. | **`track_high_thresh`**: Min confidence for detection association. | **`match_thresh`**: IoU threshold for detection-track matching. |
| **`device`**: `cuda:0` (GPU) or `cpu`. | **`track_low_thresh`**: Min confidence for tracking. | **`proximity_thresh`**: Max allowed bounding box distance. |
| **`half`**: Use FP16 for speed if supported. | **`new_track_thresh`**: Min confidence to start a new track. | **`appearance_thresh`**: Min similarity score for ReID matches. |
| **`frame_rate`**: Affects track buffer length. | **`track_buffer`**: Frames to keep a lost track alive. | **`fuse_first_associate`**: Use both appearance & motion cues initially. |
| **`with_reid`**: Enable ReID-based tracking. | | **`cmc_method`**: Camera motion correction method. |
| **`per_class`**: Track objects separately per class. |   |   |


*\* IoU : Area of Intersection / Area of Union

## Tuning Tips
- **Too many ID switches?** Increase `track_buffer`, lower `match_thresh`, `proximity_thresh`, `appearance_thresh`.
- **False associations?** Increase `match_thresh`, `proximity_thresh`, `appearance_thresh`.
- **Missed objects?** Lower `new_track_thresh`, `track_high_thresh`.
- **Track loss after occlusion?** Increase `track_buffer`, adjust `appearance_thresh`.


