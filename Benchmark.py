import Transmob.VideoProcesser as vp
import TransmobNT.VideoProcesser as vpNT
import torch
if not torch.cuda.is_available():
    import TransmobYT.VideoProcesser as vpYT
else:
    import TransmobYTC.VideoProcesser as vpYT


if __name__ == '__main__':
    processes = {"Classique" : None, "NT" : None, "YT" : None}

    f = r"C:\Users\guest_l5dyhea\Desktop\transmob\videos\media2shortmult"

    processes["Classique"], lines = vp.models_trials(f, cores =4)
    processes["NT"] = vpNT.models_trials(f, 3, lines)
    processes["YT"] = vpYT.models_trials(f, 4, lines)