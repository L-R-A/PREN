import cv2
import helper as hp
import copy as cp
import numpy as np
import os
import keras.api._v2.keras as keras

IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160

FPS = 21
RT = 15
REDUNDANCY = 1

def open_camera_profile(ip_address, username, password, profile): # Open the camera
    cap = cv2.VideoCapture('rtsp://' +
        username + ':' +
        password +
        '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', ip_address)
        return None
     
    angle_one = []
    angle_two = []

    images = []

   

    i = 0

    while True:
        
        #frame size 640x480
        ret, frame = cap.read()
        frame = cv2.resize(frame, (IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        frame = frame[0:115, 10:150]
        copy = cp.deepcopy(frame)
        preprocessed_frame = hp.Preprocess.start(copy)

        # Cache first frame
        if i < REDUNDANCY:
            angle_one.append(preprocessed_frame)
            print("FIRST ANGLE FOUND")
        # Amount of frames needed for half a rotation
        if i >= FPS * RT:
            angle_two.append(preprocessed_frame)
            print("SECOND ANGLE FOUND")
           
        if i >= ((FPS * RT) + REDUNDANCY) - 1:
            break

        if not ret:
            print('Warning: unable to read next frame')
            break

        i = i + 1


    images = [[i1, i2] for i1, i2 in zip(angle_one, angle_two)]

    images = np.array(images)

    print(np.shape(images))

    return images

    
MODEL_NAME = "v5_data_10000" + ".keras"
MODEL_PATH = os.path.join("..", "tmp", "models")

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def predict_positions(image_pair):

    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH, MODEL_NAME))

    while True:
        cv2.imshow('Angle one', image_pair[0, 0])
        cv2.imshow('Angle two', image_pair[0, 1])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    predictions = model.predict([image_pair[:, 0], image_pair[:, 1]])

    predicted_nummeric = np.argmax(predictions, axis=-1)
    predicted_readable = np.vectorize(label_mapping.get)(predicted_nummeric)

    print("NUMMERIC: \n")
    print(predicted_nummeric)
    print("READABLE: \n")
    print(predicted_readable)
    print("\n\n")

result = open_camera_profile('147.88.48.131', 'pren', '463997', 'pren_profile_small')
predict_positions(result)

def stream_only (ip_address, username, password, profile):
    cap = cv2.VideoCapture('rtsp://' +
        username + ':' +
        password +
        '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', ip_address)
        return None
     

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        frame = frame[0:115, 10:150]
        copy = cp.deepcopy(frame)
        preprocessed_frame = hp.Preprocess.start(frame)
        

        while True:
            cv2.imshow('IMAGE', preprocessed_frame)
            cv2.imshow('IMAGE OG', copy)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# stream_only('147.88.48.131', 'pren', '463997', 'pren_profile_small')