import multiprocessing
import shutil
from typing import Dict
import json

from .Analyze import *


def vidduration(filename):
    import cv2
    
    video = cv2.VideoCapture(filename)
    
    # Check if the video opened successfully
    if not video.isOpened():
        raise ValueError("Error opening video file")

    # Get total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # Get the frame rate (frames per second)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    # Calculate duration in seconds
    duration_seconds = total_frames / fps
    
    # Release the video capture object
    video.release()
    
    return duration_seconds

def format_dur(duration):
    # Convert seconds to hh:mm:ss
    hours, remainder = divmod(int(duration), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format the duration
    duration = f"{hours:02}:{minutes:02}:{seconds:02}"
    return duration

class Playlist:
    def __init__(self, folder:str, cores:int = 1, model:str="weights/yolov8n.pt", watch_classes=None, frame_nb:int = 2,
                 graph = False, screenshots = False, onesetup = False, validation = False, SAHI = False):
        if watch_classes is None:
            watch_classes = ["car", "truck", "motorbike", "bus", "bicycle", "person"]
        self.playlists = None
        if all([os.path.isdir(rf"{folder}/{s}") for s in os.listdir(folder) if s != "playlist.json"]):
            self.playlists = [Playlist(rf"{folder}/{s}", cores, model, watch_classes, frame_nb, graph, screenshots, onesetup, validation) for s in os.listdir(folder) if s != "playlist.json"]
        self.folder = folder
        self.model = model
        self.graph = graph
        self.screenshots = screenshots
        self.watch_classes = watch_classes
        self.files : List[str] = [f for f in os.listdir(self.folder) if f[-4:].lower() in [".mp4", ".mts", ".lrv", ".avi", ".mkv"]]
        self.files.reverse()
        self.cores = min(cores, len(self.files))
        self.analysers : Dict[str, Analyser|None] = {f:None for f in self.files}
        self.frame_nb = frame_nb
        self.onesetup = onesetup
        self.validation = validation
        self.SAHI = SAHI

    def sort_files(self):
        self.files.sort(key=lambda x:os.path.getmtime(fr"{self.folder}/{x}"))

    def initialise(self, lines=None, trust = False):
        if self.playlists is not None:
            for i, p in enumerate(self.playlists):
                print(f"{i+1}/{len(self.playlists)}", end="\r", flush=True)
                lines, trust = p.initialise(lines, trust)
                p.dump()
            print("Complete.", flush=True)
            for i in range(len(self.playlists)):
                del self.playlists[0]
            self.playlists = [rf"{self.folder}/{s}" for s in os.listdir(self.folder) if s != "playlist.json"]
            return lines, trust
        if os.path.exists(f"{self.folder}/product"):
            shutil.rmtree(f"{self.folder}/product")
        os.mkdir(f"{self.folder}/product")
        if os.path.isdir(rf"{self.folder}/product/screens"):
            shutil.rmtree(rf"{self.folder}/product/screens")
        if self.screenshots:
            os.mkdir(f"{self.folder}/product/screens")
        first = True
        for f in self.files:
            an = Analyser(self.folder, f, graph=self.graph, model=self.model, watch_classes=self.watch_classes,
                          frame_nb=self.frame_nb, screenshots=self.screenshots, SAHI=self.SAHI)
            if lines is not None:
                trust = an.starter(lines, trust_time=trust, sp = not self.validation and not first) or trust
            else:
                trust = an.starter(trust_time=trust) or trust
            if self.onesetup:
                lines = an.get_lines()
            an.dump()
            self.analysers[f] = f
            first = False
        self.sort_files()
        return lines, trust

    def start(self, an:Analyser, track = None):
        if type(an) == str:
            an = Analyser.load(self.folder, an)
        start_time = time.time()
        tracker = an.process(track)
        end_time = time.time()
        process_duration = end_time - start_time
        d = vidduration(an.url)
        print(f"{an.name} ({format_dur(d)}) lasted {format_dur(process_duration)}")
        del an
        return d, tracker

    def play(self):
        if self.playlists is not None:
            video_d, process_dur = 0, 0
            for p in self.playlists:
                print(f"Start playing {p} :")
                if type(p) == str:
                    p = Playlist.load(p)
                video_d2, process_dur2, _ = p.play()
                video_d += video_d2
                process_dur += process_dur2
                del p
            diff = round(100 * (process_dur / video_d) - 100, 2) if process_dur < video_d else round(100 * (process_dur / video_d) - 100, 2)
            self.clean()
            return video_d, process_dur, diff
        self.files.reverse()
        An = [self.analysers[f] if self.analysers[f] is not None else f for f in self.files]
        start = time.time()
        results = []
        tracker = None
        for an in An:
            d, tracker = self.start(an, tracker)
            results.append(d)
        end = time.time()
        video_d = sum(results)
        process_dur = end-start
        print("\n"*3)
        diff = round(100*(process_dur/video_d)-100, 2) if process_dur<video_d else round(100*(process_dur/video_d)-100, 2)
        self.clean()
        return video_d, process_dur, diff

    def get_lines(self):
        lines = {}
        for f in self.files:
            lines[f] = self.analysers[f].get_lines()
        return lines

    def dump(self, parent = None):
        if parent is None:
            parent = self.folder

        data = {}

        data["watch_classes"] = self.watch_classes
        data["folder"] = self.folder
        data["model"] = self.model
        data["graph"] = self.graph
        data["screenshots"] = self.screenshots
        data["cores"] = self.cores
        data["frame_nb"] = self.frame_nb
        data["onesetup"] = self.onesetup
        data["validation"] = self.validation
        data["SAHI"] = self.SAHI

        with open(rf"{parent}/playlist.json", "w") as f:
            json.dump(data, f, indent=3)
        del data
        if self.playlists is None:
            for file in self.analysers:
                if self.analysers[file] is not None and not isinstance(self.analysers[file], str):
                    self.analysers[file].dump()
                    self.analysers[file] = 0
        else:
            for p in self.playlists:
                if type(p) == str:
                    p = Playlist.load(rf"{p}")
                p.dump()
                del p

    def clean(self):
        if os.path.exists(rf"{self.folder}/playlist.json"):
            os.remove(rf"{self.folder}/playlist.json")
        if os.path.exists(rf"{self.folder}/cache"):
            shutil.rmtree(rf"{self.folder}/cache")

    @classmethod
    def load(cls, parent):
        data = json.load(open(fr"{parent}/playlist.json", "r"))

        p = cls(parent, cores=data["cores"], model=data["model"], watch_classes=data["watch_classes"], frame_nb=data["frame_nb"],
                graph=data["graph"], screenshots=data["screenshots"], onesetup=data["onesetup"], validation=data["validation"],
                SAHI=data["SAHI"])

        if all([os.path.isdir(rf"{parent}/{s}") for s in os.listdir(parent) if s != "playlist.json"]):
            p.playlists = [rf"{parent}/{s}" for s in os.listdir(parent) if s != "playlist.json"]

        del data
        return p

def models_trials(folder, cores, lines = None):
    #! Growth factors :
    #! {'n': 3.97, 's': 129.22, 'm': 423.48, 'l': 841.08, 'x': 1266.49}
    models = {"n" : None, "s" : None, "m" : None, "l" : None}
    for m in models:
        print("\n"*3)
        print(f"Model size : {m}")
        p = Playlist(folder, model=f"weights/yolov8{m}.pt", cores = cores)
        if not lines is None:
            p.initialise(lines)
        else:
            p.initialise()
        if lines is None:
            lines = p.get_lines()
        diff = p.play()
        models[m] = diff
        print("YAllO", models)
    return models, lines

def accuracy(folder, cores, lines = None):
    models = {"n" : None, "m" : None, "x" : None}
    for m in models:
        print("\n"*3)
        print(f"Model size : {m}")
        p = Playlist(folder, model=f"weights/yolov8{m}.pt", cores = cores, frame_nb = 1)
        if not lines is None:
            p.initialise(lines)
        else:
            p.initialise()
            lines = p.get_lines()
        p.play()
        with open(rf"{folder}/product/results.txt") as f:
            models[m] = f.read()
        print("YT", models)
    return models, lines

if __name__ == "__main__":
    folder = input("Give folder : ")
    #models_trials(folder, 1)
    P = Playlist(folder, cores = 3, model="weights/yolov8m.pt") #, watch_classes=["bicycle", "person"]
    P.initialise()
    P.play()