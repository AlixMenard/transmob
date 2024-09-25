# transmob
Yolo based vehicle tracking solution

## transmob

Yolo object detection, SORT tracking.\
Paralleled video processing.

## transmobNT

Yolo object detection, SORT tracking.\
Paralleled video processing.\
Nested Threads for processing (frame processing vs tracking)

## transmobYT

Yolo object detection, Yolo tracking.\
Paralleled video processing.\

## transmobYTC

Yolo object detection, Yolo tracking.\
Paralleled video processing.\
YOLO runs on CUDA

### Performances
**Precision :** transmob == transmobNT < transmobYT == transmobYTC \
**Speed :** transmobYTC > transmobYT \~= transmobNT > transmob \
YTC almost doesn't scale based on model size, very efficient, others scale on a q\~=1.3 ratio \
Videos can be processed every 2 frames to speed up. On low quality, every frame is necessary.

**models :** (best case, my computer)
- n : half time with double framing
- s
- m : 
- l
- x : slightly faster than real time with double framing

### todo
- [x] file sorting for better core workload share 
- [X] adapt to cuda devices
- [X] benchmark (except model x, too long)
- [ ] Make sure person + bicycle -> bicycle only (same with motorbikes)
- [ ]   └> running on CUDA with Numba
- [ ]       └> benchmark numba's efficiency
- [ ] Try nested thread on YTC
- [ ] Directional process
