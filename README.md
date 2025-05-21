# Biodegradable vs Non-Biodegradable Object Detection with Servo Control

This project uses a Raspberry Pi, PiCamera, YOLOv8, and GPIO-controlled servos to automatically detect and classify objects as biodegradable or nonbiodegradable. Based on the detected class, the servos are actuated to point towards different bins for waste sorting.

## Features

- **Real-time object detection** using YOLOv8.
- **Classification** into biodegradable and nonbiodegradable waste.
- **Servo control** based on detected object type.
- **Visual feedback** with bounding boxes and labels on camera feed.
- **FPS display** for performance monitoring.

## Hardware Requirements

- Raspberry Pi (any model with GPIO support)
- PiCamera2
- Two Servo Motors (connected to GPIO17 and GPIO27)
- Proper power supply for servos

## Software Requirements

- Python 3.7+
- [ultralytics](https://github.com/ultralytics/ultralytics) (for YOLOv8)
- [picamera2](https://github.com/raspberrypi/picamera2)
- [gpiozero](https://gpiozero.readthedocs.io/)
- OpenCV (`cv2`)
- numpy (usually installed with OpenCV)

Install dependencies using pip:
```bash
pip install ultralytics opencv-python gpiozero numpy
# Picamera2 should be installed as per the official Raspberry Pi documentation
```

## How It Works

1. **YOLOv8 Model**: The script loads the YOLOv8 nano model (`yolov8n.pt`) for object detection.
2. **Class Filtering**:
    - Biodegradable: `apple`, `banana`, `orange`
    - Nonbiodegradable: `bottle`, `cup`, `fork`, `spoon`
    - Only these classes are labeled and acted upon; other detected objects are ignored.
3. **Camera Feed**: Captures frames from the PiCamera2.
4. **Detection & Labeling**: Draws bounding boxes and labels for detected objects.
5. **Servo Actuation**:
    - If a biodegradable item is detected, both servos move to 45°.
    - If a nonbiodegradable item is detected, both servos move to 135°.
    - If nothing is detected, servos return to neutral (90°).
6. **User Interface**: Displays the camera feed with detection results and FPS. Press `q` to exit.

## Wiring Diagram

```
GPIO17  ---> Servo 1 Signal
GPIO27  ---> Servo 2 Signal
5V      ---> Servo Power (use external supply if needed)
GND     ---> Common Ground
```
**Note:** Servos can draw significant current; use an external power supply if required.

## Usage

1. Connect the hardware as described above.
2. Place the `yolov8n.pt` model file in the same directory as the script (download from [Ultralytics YOLOv8 releases](https://github.com/ultralytics/ultralytics)).
3. Run the script:
    ```bash
    python your_script_name.py
    ```
4. The camera window will open. Show objects to the camera for detection and observe the servos' movements.

## Customization

- **Object Classes**: Modify the `biodegradable_items` and `nonbiodegradable_items` lists to suit your sorting needs.
- **Servo Angles**: Adapt the servo angles in the `set_servo_angle()` calls for your specific hardware setup.
- **Model**: Try different YOLOv8 models for speed/accuracy trade-offs.

## Troubleshooting

- If servos jitter or do not move as expected, check your power supply.
- If the camera feed is blank, verify your PiCamera2 setup.
- For slow FPS, consider a lighter YOLO model or optimize your Pi's performance.

## License

MIT License

## Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [gpiozero](https://gpiozero.readthedocs.io/)
- [picamera2](https://github.com/raspberrypi/picamera2)

```
For questions or contributions, open an issue or pull request!
```
