import cv2
import helper as hp
import copy as cp

IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160

def open_camera_profile(ip_address, username, password, profile): # Open the camera
    cap = cv2.VideoCapture('rtsp://' +
        username + ':' +
        password +
        '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', ip_address)
        return None
    while True:
        
        #frame size 640x480
        ret, frame = cap.read() 
        frame = cv2.resize(frame, (IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        frame = frame[0:115, 10:150]
        copy = cp.deepcopy(frame)
        preprocessed_frame = hp.Preprocess.start(copy)

        if not ret:
            print('Warning: unable to read next frame')
            break
        cv2.imshow('frame', frame)
        cv2.imshow('preprocessed', preprocessed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

open_camera_profile('147.88.48.131', 'pren', '463997', 'pren_profile_small')