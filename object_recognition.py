import cv2
import numpy as np
from queue import Queue
from threading import Thread
from ultralytics import YOLO
import scrcpy
import cvzone
import math
from adbutils import adb

# List of class names for detections
classNames = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
    "potted plant", "bed", "dining table", "toilet", "tv monitor", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush"
]

# Establish connection to the Android device via ADB
adb.connect("127.0.0.1:5555")

# Load the YOLO model
model = YOLO('yolov8n.pt').cuda()  # Ensure you have the .pt file and CUDA is available

# Queue for holding frames
frame_queue = Queue(maxsize=1)

def process_frames():
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(frame, imgsz=640)
            if len(results):
                annotated_image = visualize(np.copy(frame), results)
                rgb_final = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                rgb_final = cv2.resize(rgb_final, (320, 540))  # Resize to desired dimensions
                cv2.imshow('Annotated Image', rgb_final)
            if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit the display window
                break

def visualize(img, results):
    """ Draw bounding boxes and labels on the image. """
    for r in results:
        boxes = r.boxes
        for box in boxes:vis
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h), 2, rt=0)
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = box.cls[0]
            name = classNames[int(cls)]
            cvzone.putTextRect(img, f'{name} {conf:.2f}', (x1, y1-10), scale=1, thickness=2, colorR=(0,255,0), offset=10)
    return img

# Start a thread to process frames
processing_thread = Thread(target=process_frames)
processing_thread.daemon = True
processing_thread.start()

# Initialize scrcpy client
client = scrcpy.Client(device=adb.device_list()[0])

def on_frame(frame):
    if frame is not None and not frame_queue.full():
        frame_queue.put(frame.copy())

# Add listener and start client
client.add_listener(scrcpy.EVENT_FRAME, on_frame)
client.start(threaded=True)