from flask import Flask, Response
import cv2
import threading
import os

app = Flask(__name__)

VIDEO_PATH = '../ressources/video_example/01_config.mp4'

cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), VIDEO_PATH))

video_running = True

def generate_frames():
    global video_running
    print(video_running)

    while video_running:
        success, frame = cap.read()
        if not success:
            # Reset the video capture object to the beginning of the file
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Encode the frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # Convert JPEG to bytes
        frame_bytes = jpeg.tobytes()

        # Yield the frame bytes as a response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def stop_video_thread():
    global video_running
    video_running = False
    frame_thread.join()

@app.route('/stop_video')
def stop_video():
    stop_video_thread()
    return 'Video stream stopped'

frame_thread = threading.Thread(target=generate_frames)
frame_thread.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
