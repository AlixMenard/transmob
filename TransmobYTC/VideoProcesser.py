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
    def __init__(self, folder:str, cores:int = 2, model:str="weights/yolov8n.pt", watch_classes=None, frame_nb:int = 2,
                 graph = False, screenshots = False, onesetup = False, validation = False):
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
        self.files : List[str] = [f for f in os.listdir(self.folder) if f[-4:].lower() in [".mp4", ".mts", ".lrv", ".avi"]]
        self.files.reverse()
        self.cores = min(cores, len(self.files))
        self.analysers : Dict[str, Analyser|None] = {f:None for f in self.files}
        self.frame_nb = frame_nb
        self.onesetup = onesetup
        self.validation = validation

    def sort_files(self):
        durations = {f:int(vidduration(self.folder+"/"+f)) for f in self.files}
        cores = [[("",0,0)] for _ in range(self.cores)]
        while durations:
            longest_vid = max(zip(durations.values(), durations.keys()))[1]
            shortest_core = min(cores, key=lambda x: x[-1][-1])
            d = durations.pop(longest_vid)
            shortest_core.append((longest_vid, d,shortest_core[-1][-1] + d))

        for core in cores:
            core.pop(0)
        final_order = []
        while any([len(c) > 0 for c in cores]):
            earliest = min(cores, key=lambda x: x[0][-1] - x[0][-2])
            final_order.append(earliest.pop(0))
            if len(earliest) == 0:
                cores.remove(earliest)

        self.files = [f[0] for f in final_order]

    def initialise(self, lines=None, trust = False, first = False):
        if self.playlists is not None:
            first = True
            for i,p in enumerate(self.playlists):
                print(f"{i}/{len(self.playlists)}", end="\r", flush=True)
                lines, trust = p.initialise(lines, trust, first)
                first = False
                p.dump()
            print("Complete.", flush=True)
            for i in range(len(self.playlists)):
                del self.playlists[0]
            self.playlists = [rf"{self.folder}/{s}" for s in os.listdir(self.folder) if s != "playlist.json"]
            return
        if os.path.exists(f"{self.folder}/product"):
            shutil.rmtree(f"{self.folder}/product")
        os.mkdir(f"{self.folder}/product")
        if self.screenshots:
            if os.path.isdir(rf"{self.folder}/product/screens"):
                shutil.rmtree(rf"{self.folder}/product/screens")
            os.mkdir(f"{self.folder}/product/screens")
        for f in self.files:
            an = Analyser(self.folder, f, graph=self.graph, model=self.model, watch_classes=self.watch_classes,
                          frame_nb=self.frame_nb, screenshots=self.screenshots)
            if (lines is not None) or (not first):
                trust = an.starter(lines, trust_time=trust, sp = not self.validation) or trust
            else:
                trust = an.starter(trust_time=trust) or trust
            if self.onesetup:
                lines = an.get_lines()
            self.analysers[f] = an
        self.sort_files()
        return lines, trust

    def start(self, an:Analyser):
        if type(an) == str:
            an = Analyser.load(self.folder, an)
        start_time = time.time()
        an.process()
        end_time = time.time()
        process_duration = end_time - start_time
        d = vidduration(an.url)
        print(f"{an.name} ({format_dur(d)}) lasted {format_dur(process_duration)}", flush = True)
        return d

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
            return video_d, process_dur, diff
        An = [self.analysers[f] if self.analysers[f] is not None else f for f in self.files]
        start = time.time()
        results = []
        for an in An:
            results.append(self.start(an))
        end = time.time()
        video_d = sum(results)
        process_dur = end-start
        print("\n"*3)
        diff = round(100*(process_dur/video_d)-100, 2) if process_dur<video_d else round(100*(process_dur/video_d)-100, 2)
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

        with open(rf"{parent}/playlist.json", "w") as f:
            json.dump(data, f, indent=3)
        del data
        if self.playlists is None:
            for file in self.analysers:
                if self.analysers[file] is not None:
                    self.analysers[file].dump()
                    del self.analysers[file]
        else:
            for p in self.playlists:
                if type(p) == str:
                    p = Playlist.load(rf"{p}")
                p.dump()
                del p

    @classmethod
    def load(cls, parent):
        data = json.load(open(fr"{parent}/playlist.json", "r"))

        p = cls(parent, cores=data["cores"], model=data["model"], watch_classes=data["watch_classes"], frame_nb=data["frame_nb"],
                graph=data["graph"], screenshots=data["screenshots"], onesetup=data["onesetup"], validation=data["validation"])

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
        print("YTC", models)
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
        print("YTC", models)
    return models, lines

if __name__ == "__main__":
    folder = input("Give folder : ")
    #models_trials(folder, 1)
    P = Playlist(folder, cores = 3, model="weights/yolov8m.pt") #, watch_classes=["bicycle", "person"]
    P.initialise()
    P.play()