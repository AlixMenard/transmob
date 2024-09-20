# transmob
Yolo based vehicle tracking solution

## transmob

Yolo object detection, SORT tracking.
Paralleled video processing.

## transmobNT

Yolo object detection, SORT tracking.
Paralleled video processing.
Nested Threads for processing (frame processing vs tracking)

## transmobYT

Yolo object detection, Yolo tracking.
Paralleled video processing.

### Performances
**Precision :** transmob == transmobNT, transmobYT to be determined
**Speed :** transmobYT ~= transmobNT > transmob

### todo
- file sorting for better core workload share
- adapt to cuda devices
- benchmark
