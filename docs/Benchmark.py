import Transmob.VideoProcesser as vp
import TransmobNT.VideoProcesser as vpNT
import torch
if not torch.cuda.is_available():
    import TransmobYT.VideoProcesser as vpYT
    cudab= False
else:
    import TransmobYTC.VideoProcesser as vpYT
    cudab= True

def process_benchmark_accuracy():
    yt = "YT" if not cudab else "YTC"
    print(yt)
    processes = {"Classique" : None, "NT" : None, yt : None}

    f = r"C:\Users\Utilisateur\Desktop\transmob\videos\1x1min"

    processes["Classique"], lines = vp.accuracy(f, cores =4)
    processes["NT"], _ = vpNT.accuracy(f, 3, lines)
    processes[yt], _ = vpYT.accuracy(f, 4, lines)

    for p in processes:
        print(p, processes[p])


def process_benchmark_speed():
    yt = "YT" if not cudab else "YTC"
    processes = {"Classique" : None, "NT" : None, yt : None}

    f = r"C:\Users\alixm\Desktop\transmob\videos\10x1min"

    processes["Classique"], lines = vp.models_trials(f, cores =4)
    processes["NT"], _ = vpNT.models_trials(f, 3, lines)
    processes[yt], _ = vpYT.models_trials(f, 4, lines)

    for p in processes:
        print(p, processes[p])

if __name__ == '__main__':
    process_benchmark_accuracy()