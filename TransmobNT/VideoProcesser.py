import multiprocessing
import multiprocessing.pool
import shutil
from typing import Dict


from .Analyze import *


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, val):
        pass


class NoDaemonProcessPool(multiprocessing.pool.Pool):

    def Process(self, *args, **kwds):
        proc = super(NoDaemonProcessPool, self).Process(*args, **kwds)
        proc.__class__ = NoDaemonProcess

        return proc

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
        if all([os.path.isdir(rf"{folder}/{s}") for s in os.listdir(folder)]):
            self.playlists = [Playlist(rf"{folder}/{s}", cores, model, watch_classes, frame_nb, graph, screenshots, onesetup, validation) for s in os.listdir(folder)]
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

    def initialise(self, lines=None):
        if self.playlists is not None:
            for p in self.playlists:
                p.initialise(lines)
            return
        trust = False
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
            if lines is not None:
                trust = an.starter(lines, trust_time=trust, sp = not self.validation) or trust
            else:
                trust = an.starter(trust_time=trust) or trust
            if self.onesetup:
                lines = an.get_lines()
            self.analysers[f] = an
        self.sort_files()

    def start(self, an:Analyser):
        start_time = time.time()
        an.process()
        end_time = time.time()
        process_duration = end_time - start_time
        d = vidduration(an.url)
        print(f"{an.name} ({format_dur(d)}) lasted {format_dur(process_duration)}")
        return d

    def play(self):
        if self.playlists is not None:
            video_d, process_dur = 0, 0
            for p in self.playlists:
                video_d2, process_dur2, _ = p.play()
                video_d += video_d2
                process_dur += process_dur2
            diff = round(100 * (process_dur / video_d) - 100, 2) if process_dur < video_d else round(100 * (process_dur / video_d) - 100, 2)
            return video_d, process_dur, diff
        An = [self.analysers[f] for f in self.files]
        start = time.time()
        with NoDaemonProcessPool(processes=self.cores) as pool:
            results = pool.map(self.start, An)
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
        print("NT", models)
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
        print("NT", models)
    return models, lines

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    folder = input("Give folder : ")
    #models_trials(folder, 1)
    P = Playlist(folder, cores = 3, model="weights/yolov8m.pt")
    P.initialise()
    P.play()