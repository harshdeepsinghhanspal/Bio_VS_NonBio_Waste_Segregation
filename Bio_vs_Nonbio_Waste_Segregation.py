from ultralytics import YOLO
from picamera2 import Picamera2
from gpiozero import Servo
from time import sleep
import cv2
import math
import time

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Only these classes will be labeled
biodegradable_items = ["apple", "banana", "orange"]
nonbiodegradable_items = ["bottle", "cup", "fork", "spoon"]

# Full COCO class list
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

# Setup servos
servo1 = Servo(17)
servo2 = Servo(27)

# Servo angle helper (convert degree to -1 to +1 for gpiozero)
def set_servo_angle(servo, angle):
    position = (angle - 90) / 90  # Maps 0–180 to -1–+1
    servo.value = position

# Set to neutral
set_servo_angle(servo1, 90)
set_servo_angle(servo2, 90)

# Initialize PiCamera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

prev_frame_time = 0

while True:
    new_frame_time = time.time()
    frame = picam2.capture_array()
    detected_type = "neutral"

    results = model(frame, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            if cls < len(classNames):
                detected_item = classNames[cls]

                if detected_item in biodegradable_items:
                    label = f'biodegradable {conf}'
                    color = (0, 255, 0)
                    detected_type = "bio"
                elif detected_item in nonbiodegradable_items:
                    label = f'nonbiodegradable {conf}'
                    color = (0, 0, 255)
                    detected_type = "nonbio"
                else:
                    continue

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Control servos based on detected type
    if detected_type == "bio":
        set_servo_angle(servo1, 45)
        set_servo_angle(servo2, 45)
    elif detected_type == "nonbio":
        set_servo_angle(servo1, 135)
        set_servo_angle(servo2, 135)
    else:
        set_servo_angle(servo1, 90)
        set_servo_angle(servo2, 90)

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("PiCam YOLOv8 Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.close()
