import socket
import cv2
import numpy as np
from queue import Queue
from threading import Thread
from ultralytics import YOLO
import scrcpy
import math
from adbutils import adb

# Define class names for detections
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

# Load the YOLO model (ensure the model and CUDA are set up correctly)
model = YOLO('yolov8n.pt').cuda()

# Queue to hold frames for processing
frame_queue = Queue(maxsize=1)
def visualize(img, results):
    """ Draw bounding boxes and labels on the image. """
    coordinates="No detections"
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xcenter= int((x1+x2)/2)
            ycenter = int((y1 + y2) / 2)
            coordinates=str(xcenter)+","+str(ycenter)
    return coordinates
def process_frames(conn):
    """Process frames and send detection results over a socket connection."""
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            height, width, _ = frame.shape
            frame_cropped = frame[:, :width // 2, :]

            # Apply fisheye correction
            frame = fisheye_correction(frame_cropped)

            frame = rotate_image(frame, angle=-10)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(frame, imgsz=640)  # Perform object detection
            if len(results):
                coordinatestosend = visualize(np.copy(frame), results)
                if coordinatestosend != "No detections":
                    conn.sendall((coordinatestosend + '\n').encode('utf-8'))  # Send detection

def rotate_image(image, angle):
    """
    Rotate the image by the given angle.
    """
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image
def fisheye_correction(frame):
    # Define the fisheye correction parameters
    K = np.array([[2226.24649, 0, 1104.46823], [0, 2232.12874, 2043.33422], [0, 0, 1]])
    D = np.array([[-0.00870], [0.03062], [-0.05044], [0.02613]])

    # Perform fisheye correction
    corrected_frame = cv2.fisheye.undistortImage(frame, K, D, Knew=K)

    return corrected_frame
def calculate_center(bbox):
    """Calculate the center of the bounding box."""
    x1, y1, x2, y2 = bbox
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return x_center, y_center


def format_detection_data(results):
    """Format the detection results into a string for transmission."""
    detections = []
    for det in results.xyxy[0]:  # detections per image
        x1, y1, x2, y2, conf, cls = det
        cls_name = classNames[int(cls)]
        detections.append(f"{cls_name},{x1},{y1},{x2},{y2},{conf}")
    return "\n".join(detections)

def server_thread():
    """Set up the server that listens for connections and processes frames."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.168.0.xxx',12345))  # Bind to all interfaces at port 12345
        s.listen(1)
        print("Server listening for connections...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            process_frames(conn)

# Start the server in a new thread
Thread(target=server_thread, daemon=True).start()

# Initialize scrcpy client for frame capture from an Android device
client = scrcpy.Client(device=adb.device_list()[0])

def on_frame(frame):
    """Callback for new frames captured from the Android device."""
    if frame is not None and not frame_queue.full():
        frame_queue.put(frame.copy())  # Put frame in queue for processing

# Add listener for new frames and start client
client.add_listener(scrcpy.EVENT_FRAME, on_frame)
client.start(threaded=True)
