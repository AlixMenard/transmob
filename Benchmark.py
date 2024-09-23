import Transmob.VideoProcesser as vp
#import TransmobNT.VideoProcesser as vpNT
#import TransmobYT.VideoProcesser as vpYT

processes = {"Classique" : None, "NT" : None, "YT" : None}

f = r"C:\Users\guest_l5dyhea\Desktop\transmob\videos\media2shortmult"

processes["Classique"], lines = vp.models_trials(f, cores =5)
#processes["NT"] = vpNT.models_trials(f, 3, lines)
#processes["YT"] = vpYT.models_trials(f, 5, lines)