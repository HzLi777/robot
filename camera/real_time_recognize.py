import time
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

rgb_cam = Picamera2(camera_num = 0)
rgb_cam.configure(rgb_cam.create_video_configuration({"format": "RGB888", "size": (1280, 720)}))

model = YOLO("/home/Haozhe/robot/camera/custom.pt")
model2 = YOLO("/home/Haozhe/robot/camera/yolov8n_ncnn_model")


def cam_recognize(mod):
    cam = rgb_cam
    cam.start()
    print("Camera record")
    
    while True:
        frame= cam.capture_array()
        
        results = mod(frame, conf = 0.35)
        annotated_frame = results[0].plot()
        
        """
        cv2.imshow("Camera", annotated_frame)
        print(f"captured from {cam}")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        """
        cv2.imwrite("/home/Haozhe/robot/camera/cam_output/output.jpg",annotated_frame)
        time.sleep(0.1)
        print("Frame saved. Open http://raspberrypi.local:5000 in browser.")
        
if __name__ =="__main__":
    cam_recognize(model2)
        
        