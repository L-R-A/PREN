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

FPS = 22
RT = 14
REDUNDANCY = 100

TEMP_PATH = os.path.join('./', 'tmp', 'temp_save')

def normalize_images(images):
    return images / 255

def save_frames(): # Open the camera
    try:
        print("-- GETTING FRAMES FROM LIVESTREAM")
        frames = st.Stream.getFrame(640, 480, 0, 5, FPS * 1)
        frame_1_1 = frames[0]
        frame_1_2 = frames[1]
        frame_1_3 = frames[2]
        frame_1_4 = frames[3]
        frame_1_5 = frames[4]
        print("--- STARTPOSITIONS RETRIEVED")

        frames = st.Stream.getFrame(640, 480, (RT - 4) * FPS, 5, FPS * 1)
        frame_2_1 = frames[0]
        frame_2_2 = frames[1]
        frame_2_3 = frames[2]
        frame_2_4 = frames[3]
        frame_2_5 = frames[4]
        print("--- ENDPOSITION RETRIEVED\n")

    except:
        print("CONNECTION FAILED: GENERATING RANDOM COMBINATION")
        return False

    print("-- SAVING FRAMES TO DISK")
    if not os.path.exists(TEMP_PATH):    
        os.makedirs(TEMP_PATH)

    cv2.imwrite(os.path.join(TEMP_PATH, f'image1_1.jpg'), frame_1_1)
    print("--- SAVED IMAGE: 1_1") 
    cv2.imwrite(os.path.join(TEMP_PATH, f'image1_2.jpg'), frame_2_1)
    print("--- SAVED IMAGE: 1_2") 
    cv2.imwrite(os.path.join(TEMP_PATH, f'image2_1.jpg'), frame_1_2) 
    print("--- SAVED IMAGE: 2_1") 
    cv2.imwrite(os.path.join(TEMP_PATH, f'image2_2.jpg'), frame_2_2)
    print("--- SAVED IMAGE: 2_2") 
    cv2.imwrite(os.path.join(TEMP_PATH, f'image3_1.jpg'), frame_1_3)
    print("--- SAVED IMAGE: 3_1")  
    cv2.imwrite(os.path.join(TEMP_PATH, f'image3_2.jpg'), frame_2_3) 
    print("--- SAVED IMAGE: 3_2") 
    cv2.imwrite(os.path.join(TEMP_PATH, f'image4_1.jpg'), frame_1_4)
    print("--- SAVED IMAGE: 4_1")  
    cv2.imwrite(os.path.join(TEMP_PATH, f'image4_2.jpg'), frame_2_4)
    print("--- SAVED IMAGE: 4_2")    
    cv2.imwrite(os.path.join(TEMP_PATH, f'image5_1.jpg'), frame_1_5)
    print("--- SAVED IMAGE: 5_1")  
    cv2.imwrite(os.path.join(TEMP_PATH, f'image5_2.jpg'), frame_2_5)
    print("--- SAVED IMAGE: 5_2")    
    return True

    
MODEL_NAME = "v1_no_base_50000" + ".keras"
MODEL_PATH = os.path.join("..", "model")

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def calculate_final_result_algorithmus_1(predicted_nummeric):
    print("--- RUNNING REDUNDANCY CHECK 1: np.all\n")

    result = np.zeros_like(predicted_nummeric[0])

    for i in range(predicted_nummeric.shape[1]):
        values = predicted_nummeric[:, i]
        if np.all(values == 3):
            result[i] = 3
        else:
            result[i] = values[np.where(values != 3)[0][0]]
    return result

def calculate_final_result_algorithmus_2(predicted_nummeric):
    print("--- RUNNING REDUNDANCY CHECK 2: np.argmax\n")
    result = np.zeros_like(predicted_nummeric[0])

    for i in range(predicted_nummeric.shape[1]):
        mode_value, mode_count = np.unique(predicted_nummeric[:, i], return_counts=True)
        max_mode_index = np.argmax(mode_count)
        result[i] = mode_value[max_mode_index]

    return result

def predict_positions(image_path_one, image_path_two):

    image_pair = []

    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_NAME))
    print("-- LOADED MODEL")

    for image_path in image_path_one:
        full_path_one = os.path.join(TEMP_PATH, image_path)

        image_one = Image.open(full_path_one)
        image_one = image_one.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        image_one = np.array(image_one)[:, :, ::-1]
        image_one = image_one[0:115, 10:150]
        image_one = hp.Preprocess.start(image_one)

        normalized_one = normalize_images(image_one)
        image_pair.append([normalized_one]);
    print("-- PREPROCESSED AND NORMALIZED STARTPOSITIONS")

    for i, image_path in enumerate(image_path_two):
        full_path_two = os.path.join(TEMP_PATH, image_path)

        image_two = Image.open(full_path_two)
        image_two = image_two.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        image_two = np.array(image_two)[:, :, ::-1]
        image_two = image_two[0:115, 10:150]
        image_two = hp.Preprocess.start(image_two)

        normalized_two = normalize_images(image_two)
        image_pair[i].append(normalized_two);

    print("-- PREPROCESSED AND NORMALIZED ENDPOSITIONS")

    image_pair = np.array(image_pair)

    print("-- PREDICTING POSITIONS")

    predictions = model.predict([image_pair[:, 0], image_pair[:, 1]])

    print("-- PREDICTION FINISHED\n")

    predicted_nummeric = np.argmax(predictions, axis=-1)
    predicted_readable = np.vectorize(label_mapping.get)(predicted_nummeric)

    print("PREDICTIONS: \n")
    print(predicted_readable)
    print("\n\n")

    result_one = calculate_final_result_algorithmus_1(predicted_nummeric)

    print("ALGORITHMUS 1: FINAL RESULT: \n")
    print(result_one)
    print("\n")
    print("READABLE: \n")
    print(np.vectorize(label_mapping.get)(result_one))
    print("\n\n")

    result_two = calculate_final_result_algorithmus_2(predicted_nummeric)

    print("ALGORITHMUS 2: FINAL RESULT: \n")
    print(result_two)
    print("\n")
    print("READABLE: \n")
    print(np.vectorize(label_mapping.get)(result_two))
    print("\n\n")

    return np.vectorize(label_mapping.get)(result_one)

start_time = time.time()

print("RUNNING IN PROD MODE\n")

print("- SAVING FRAMES")
response = save_frames()

result = []

if response == True:
    print("- PREDICT POSITIONS\n")
    result = predict_positions(
        [
            "image1_1.jpg", 
            "image2_1.jpg", 
            "image3_1.jpg", 
            "image4_1.jpg", 
            "image5_1.jpg"
        ], 
        [
            "image1_2.jpg",
            "image2_2.jpg",
            "image3_2.jpg",
            "image4_2.jpg",
            "image5_2.jpg"
        ]
    )

else: 
    result = np.array(['', 'red', 'yellow', 'blue', '', 'blue', 'red', ''])

end_time = time.time()

elapsed_time = end_time - start_time

print(hp.JSON.convert_numpy_to_json(result))

print("Elapsed time:", elapsed_time, "seconds")