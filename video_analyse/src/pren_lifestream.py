import cv2
import helper as hp
import numpy as np
import os
import keras.api._v2.keras as keras
import stream_image as st
from PIL import Image
import shutil

IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160

FPS = 21
RT = 15
REDUNDANCY = 100

TEMP_PATH = os.path.join('./', 'tmp', 'temp_save')

def normalize_images(images):
    return images / 255

def save_frames(): # Open the camera
    frame_1 = st.Stream.getFrame(640, 480, 0, 1)[0]
    frame_2 = st.Stream.getFrame(640, 480, 13*21, 1)[0]

    print(frame_1)

    if not os.path.exists(TEMP_PATH):    
        os.makedirs(TEMP_PATH)

    cv2.imwrite(os.path.join(TEMP_PATH, f'image1_1.jpg'), frame_1) 
    cv2.imwrite(os.path.join(TEMP_PATH, f'image1_2.jpg'), frame_2) 
    return 

    
MODEL_NAME = "v2_no_base_100000" + ".keras"
MODEL_PATH = os.path.join("..", "model")

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def predict_positions():

    image_pair = []

    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH, MODEL_NAME))

    full_path_one = os.path.join(TEMP_PATH, 'image1_1.jpg')
    full_path_two = os.path.join(TEMP_PATH, 'image1_2.jpg')

    image_one = Image.open(full_path_one)
    image_one = image_one.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
    image_one = np.array(image_one)[:, :, ::-1]
    image_one = image_one[0:115, 10:150]
    image_one = hp.Preprocess.start(image_one)
    # image_one = hp.Augmentation.black_spots(image_one, 100)

    image_two = Image.open(full_path_two)
    image_two = image_two.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
    image_two = np.array(image_two)[:, :, ::-1]
    image_two = image_two[0:115, 10:150]
    image_two = hp.Preprocess.start(image_two)
    # image_two = hp.Augmentation.black_spots(image_two, 100)

    while True:
        cv2.imshow('Angle one', image_one)
        cv2.imshow('Angle two', image_two)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    normalized_one = normalize_images(image_one)
    normalized_two = normalize_images(image_two)

    image_pair.append([normalized_one, normalized_two]);

    image_pair = np.array(image_pair)

    predictions = model.predict([image_pair[:, 0], image_pair[:, 1]])

    predicted_nummeric = np.argmax(predictions, axis=-1)
    predicted_readable = np.vectorize(label_mapping.get)(predicted_nummeric)

    print("NUMMERIC: \n")
    print(predicted_nummeric)
    print("READABLE: \n")
    print(predicted_readable)
    print("\n\n")

def remove_tmp_folder():
    shutil.rmtree('/path/to/your/dir/')

save_frames()
predict_positions()
# remove_tmp_folder()