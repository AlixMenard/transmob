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
#### Video re-dating (Changer date de vidéos)
If videos were wrongly dated (*last modification* date should correspond to the time the video ended, or the time it started + the duration), this tool will re-date all videos in a folder (not sub-folders) according to a starting date. Drag & drop the folder on the window, fill in the **starting** time of the first video according to the provided format, then click "Valider".

#### Directionnal formatting (Formattage directionnel)
To get a directionnal result file for the folder. Simply drag & drop the folder on the window and click "Valider". The program will look for screeshots folders to do entry/exit matching. If some vehicles could not be tracked all across the intersection, the program will enter a hand matching phase.

You will be presented an entering vehicle, and 12 potential matches amongst exiting vehicles. The potential matches are selected based on visual ressemblance and crossing time. You can either select the matching vehicle if found, or skip it if you can't surely determine a match. As you do this, the program will start to determine weither it is confident enough to automatically accept or reject some matches, to ease your task.

Once done, 2 files are created :
- `dir1.csv` : This is a csv file where each line shows the number of vehicles counted by type, indexed by unique (time, entering line, exiting line) combinations.
- `dir2.csv` : This csv file contains, for each time analysed, a matrix with entries as lines, exits as columns, as well as the combination of the most busy consecutive hour matrix.


<a name="ffmpeg"></a>
### FFMPEG
FFmpeg is a free and open-source software project for handling video, audio, and other multimedia files and streams. FFmpeg is **not** natively installed on windows devices, thus it is necessary to install it in order to use the Video Repair tool.\
Here is a [Tutorial](https://phoenixnap.com/kb/ffmpeg-windows) to install FFmpeg on windows 11.\
*Reminder : You can open a Windows terminal by pressing `win + r`, typing `cmd` then pressing `Enter`
