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
*todo : run every yolo step on cuda ?*

### Performances
**Precision :** transmob == transmobNT, transmobYT to be determined\
**Speed :** transmobYT ~= transmobNT > transmob \
Videos can be processed every 2 frames to speed up. On low quality, every frame is necessary.

**models :**
- n : ~real time with double frame
- s
- m : ~x3 with multi threading
- l
- x

### todo
- [x] file sorting for better core workload share 
- [x] adapt to cuda devices
- [x] benchmark
