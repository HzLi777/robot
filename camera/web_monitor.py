import os
import cv2
import time
from flask import Flask, Response

app = Flask(__name__)

image_path = "/home/Haozhe/robot/camera/cam_output/output.jpg"

def generate_frames():
    """ Continuously yield updated image frames for Flask streaming. """
    while True:
        try:
            
            if os.path.exists(image_path):
                # Read the latest image
                frame = cv2.imread(image_path)
                if frame is None:
                    print("Frame processing, skipping...")
                    time.sleep(0.1)
                    continue                
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # Send the frame to the client
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error {e}")

            time.sleep(0.1)  # Prevent high CPU usage, adjust update rate if needed

@app.route('/')
def index():
    """ Simple webpage to display the video stream. """
    return '''
    <html>
        <head><title>YOLO Real-Time Detection</title></head>
        <body>
            <h1> Real-time Detection Stream</h1>
            <img src="/video_feed">
        </body>
    </html>
    '''

@app.route('/video_feed')
def video_feed():
    """ Streaming route that continuously serves updated images. """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
