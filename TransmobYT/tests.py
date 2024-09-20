import os
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
import cv2
from torch.fx.experimental.proxy_tensor import track_tensor

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("weights/yolov8n.pt")

# Open the video file
video_path = r"C:\Users\guest_l5dyhea\Desktop\TransmobYT\media2\19627-304735769_tiny.mp4"
cap = cv2.VideoCapture(video_path)
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, classes=[0, 2], tracker="botsort.yaml", persist=True, verbose=False)
        print(results[0])
        #print(results[0].boxes.id.int().cpu().tolist())
        #print(results[0].boxes.cls.int().cpu().tolist())
        #print(results[0].boxes.conf.float().cpu().tolist())
        print(results[0].boxes.xyxy.cpu().tolist())

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(0) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()