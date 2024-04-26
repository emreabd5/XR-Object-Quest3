import socket
import time

start_time = time.time()  # Record the start time
run_duration = 3600  # Set the server to run for 1 hour (3600 seconds)

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.0.114', 12345))  # Bind to localhost on port 12345
server.listen(1)
print("Waiting for a connection...")

client, address = server.accept()
print(f"Connected to {address}")

while True:
    current_time = time.time()
    # Supposing 'detection_info' is the YOLO detection data you want to send
    detection_info = "x_center,y_center,width,height,class_id"
    client.send(detection_info.encode())
    if current_time - start_time > run_duration:
        print("Server has reached the maximum run duration.")
        break
    client.send(detection_info.encode())

client.close()
server.close()
