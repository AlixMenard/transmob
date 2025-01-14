### Additional tools
#### Results formatting (Formattage des résultats)
You simply need to drag & drop the `results.txt` file produces by the program, then "Valider". A csv file will be created in the same location.
#### Video renaming (Renommer vidéos)
Drag & drop the folder in which you want to rename the videos. Fill in the camera name (e.g. `GP07`) and the location, then click "Valider". Every video will be renamed in the format `camera_location_YYYYMMDD_HHhmm.ext` with *ext* being the file extension, preserved, and *YYYYMMDD_HHhmm* being the formatted date of the video.
#### Video splitting (Séparer vidéos)
In case of numerous videos to analyse (>10), it is necessary to split them in several subfolders. It is also recommended over 5 videos as it allows the program for better memory management, but isn't mandatory. The folder can still be given whole to the program afterwise, as every subfolder will be treated.\
To do so, drag & drop the folder containing the videos, then fill in the number of videos per subfolder, then click "Valider".
#### Results aggregation (Aggréger résultats)
If videos were split in subfolders, you might still want to retrieve the results for the whole video set. You only need to drag & drop the folder and click "Valider". The tool will look recursively into every subfolder for `results.txt` files and combine them in a single one inside the parent folder.
#### Video repair (Réparer vidéos)
If videos are damaged (e.g. VLC Media Player shows an error message similar to "Video index damaged or missing") the program will not be able to read them, thus it is necessary to repair the videos before hand. Drag & drop the folder on the window and click "Valider". The tool will recursively look for videos inside the folder to repair them using [FFmpeg](#ffmpeg). The video files `file.ext` with *file* the video name and *ext* the video format extension will be **replaced** by `file.r.mkv`. If this repair fails, good luck.\
**/!\\** The repair can cause the video's length to be modified, resulting in a time shift : make sure the the video's timing stays aligned afterward, or correct it when asked before analysis.

<a name="ffmpeg"></a>
### FFMPEG
FFmpeg is a free and open-source software project for handling video, audio, and other multimedia files and streams. FFmpeg is **not** natively installed on windows devices, thus it is necessary to install it in order to use the Video Repair tool.\
Here is a [Tutorial](https://phoenixnap.com/kb/ffmpeg-windows) to install FFmpeg on windows 11.\
*Reminder : You can open a Windows terminal by pressing `win + r`, typing `cmd` then pressing `Enter`
