import os
import cv2
from moviepy import concatenate_videoclips, VideoFileClip

def aggregate(path, target):
    files = os.listdir(path)
    files = sorted(files, key=lambda t: os.stat(os.path.join(path,t)).st_mtime)
    lengths = [get_vid_length(os.path.join(path,f)) for f in files]
    count = 0
    while files:
        temp = []
        while files and  abs(sum([t[1] for t in temp])-target*60) > abs(sum([t[1] for t in temp+[(files[0],lengths[0])]])-target*60):
            temp.append((files.pop(0),lengths.pop(0)))
        merge(temp, path, count)
        count += 1

def get_vid_length(path):
    video = cv2.VideoCapture(path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    return duration

def merge(temp, path, count):
    vids = [VideoFileClip(os.path.join(path,t[0])) for t in temp]
    n_vid = concatenate_videoclips(vids, method="compose")
    n_vid.write_videofile(os.path.join(path,f"merged_{count}.mp4"))