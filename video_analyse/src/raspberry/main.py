import cv2
import rasp_helper as hp
import numpy as np
import os
import keras.api._v2.keras as keras
import rasp_stream as st
from PIL import Image
import shutil
import sys
import time

IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160

FPS = 21
RT = 14
REDUNDANCY = 100

TEMP_PATH = os.path.join('./', 'tmp', 'temp_save')

IMAGE_ONE = 'image1_1.jpg'
IMAGE_TWO = 'image1_0.jpg'

def normalize_images(images):
    return images / 255

def save_frames(): # Open the camera
    try:
        print("-- GETTING FRAMES FROM LIVESTREAM")
        frame_1 = st.Stream.getFrame(640, 480, 0, 1, 1)[0]
        print("--- STARTPOSITION RETRIEVED")

        frame_2 = st.Stream.getFrame(640, 480, RT*FPS, 1, 1)[0]    
        print("--- ENDPOSITION RETRIEVED\n")
    except Exception as e:
        print(e)
        print("CONNECTION FAILED: GENERATING RANDOM COMBINATION")
        return False        


    print("-- SAVING FRAMES TO DISK")
    if not os.path.exists(TEMP_PATH):    
        os.makedirs(TEMP_PATH)

    cv2.imwrite(os.path.join(TEMP_PATH, IMAGE_ONE), frame_1)
    print("--- SAVED FIRST IMAGE")
 
    cv2.imwrite(os.path.join(TEMP_PATH, IMAGE_TWO), frame_2)
    print("--- SAVED SECOND IMAGE\n")
    return True

    
MODEL_NAME = "v1_no_base_50000" + ".keras"

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def predict_positions(image_one, image_two):

    image_pair = []

    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_NAME))
    print("-- LOADED MODEL")

    full_path_one = os.path.join(TEMP_PATH, image_one)
    full_path_two = os.path.join(TEMP_PATH, image_two)
    print("-- LOADED IMAGES")

    image_one = Image.open(full_path_one)
    image_one = image_one.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
    image_one = np.array(image_one)[:, :, ::-1]
    image_one = image_one[0:115, 10:150]
    image_one = hp.Preprocess.start(image_one)
    print("-- PREPROCESSED FIRST ANGLE")

    image_two = Image.open(full_path_two)
    image_two = image_two.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
    image_two = np.array(image_two)[:, :, ::-1]
    image_two = image_two[0:115, 10:150]
    image_two = hp.Preprocess.start(image_two)
    print("-- PREPROCESSED SECOND ANGLE\n")

    normalized_one = normalize_images(image_one)
    normalized_two = normalize_images(image_two)
    print("-- NORMALIZED IMAGES")

    image_pair.append([normalized_one, normalized_two]);

    image_pair = np.array(image_pair)

    print("-- PREDICTING POSITIONS")
    predictions = model.predict([image_pair[:, 0], image_pair[:, 1]])
    print("-- PREDICTION FINISHED\n")

    predicted_nummeric = np.argmax(predictions, axis=-1)
    predicted_readable = np.vectorize(label_mapping.get)(predicted_nummeric)

    print("-- PREDICTIONS: \n")
    print(predicted_readable)
    print("\n\n")

    return predicted_readable[0]

def remove_tmp_folder():
    shutil.rmtree(TEMP_PATH)

start_time = time.time()

if len(sys.argv) > 1 and sys.argv[1] == "test":
    print("RUNNING IN TEST MODE\n")

    TEMP_PATH = os.path.join("test_configs")

    print("- PREDICT CONFIGURATION 1\n")
    predict_positions('image0_1.jpg', 'image0_2.jpg')

    print("- PREDICT CONFIGURATION 2\n")
    predict_positions('image1_1.jpg', 'image1_2.jpg')

    print("- PREDICT CONFIGURATION 3\n")
    predict_positions('image2_1.jpg', 'image2_2.jpg')

if len(sys.argv) <= 1 or sys.argv[1] != "test":
    print("RUNNING IN PROD MODE\n")

    print("- SAVING FRAMES")
    response = save_frames()

    result = []

    if response == True:

        print("- PREDICT POSITIONS\n")
        result = predict_positions('image1_1.jpg', 'image1_0.jpg')
    else:
        result = np.array(['', 'red', 'yellow', 'blue', '', 'blue', 'red', ''])

    # print("- REMOVING TEMP IMAGES\n")
    # remove_tmp_folder()

    print(hp.JSON.convert_numpy_to_json(result))

end_time = time.time()

elapsed_time = end_time - start_time

print("Elapsed time:", elapsed_time, "seconds")