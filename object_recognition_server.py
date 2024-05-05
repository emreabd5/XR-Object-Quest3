import cv2
import numpy as np
from ultralytics import YOLO
from PIL import ImageGrab
import time
import socket

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

# Load the YOLO model
model = YOLO('yolov8n.pt')

def visualize(img, results, conn):
    """Draw bounding boxes and labels on the image, and send detections to the client."""
    screen_width, screen_height = 3840, 2160  # Adjust these values based on your actual screen resolution
    for result in results:
        boxes = result.boxes
        for box in boxes:
            xc, yc, w, h = map(int, box.xywh[0])
            # Draw bounding box on image
            cv2.rectangle(img, (xc - w//2, yc - h//2), (xc + w//2, yc + h//2), (0, 255, 0), 2)
            name = classNames[int(box.cls[0])]
            cv2.putText(img, name, (xc - w//2, yc - h//2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Normalize coordinates
            normalized_x = ((xc + w/2) / screen_width * 4128)
            normalized_y = ((yc + h/2) / screen_height * 2208)

            if conn:
                # Create the string to send, including normalized coordinates and the detected object class name
                coordinates = f"{normalized_x},{normalized_y},{name}\n"
                conn.sendall(coordinates.encode('utf-8'))
    return img

def server_setup():
    """Setup the server socket to listen for connections."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.1.112', 12345))  # Bind to IP and port that you want to listen on
    s.listen(1)
    print("Server ready and listening for connections...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    return conn

def run_detection():
    conn = server_setup()  # Start server and wait for a connection
    window_name = 'YOLO Object Detection'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)

    try:
        while True:
            img = ImageGrab.grab(bbox=(0, 0, 3840, 2160))  # Adjust bbox according to your screen resolution
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # Perform object detection
            results = model(frame, imgsz=640, conf=0.6)

            # Visualize results and send detections
            frame = visualize(frame, results, conn)
            cv2.imshow(window_name, frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()
        conn.close()

run_detection()
