import cv2
import rasp_helper as hp
import numpy as np
import os
import keras.api._v2.keras as keras
import rasp_stream as st
from PIL import Image
import time
import sys

IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160
FPS = 22
RT = 13
TEMP_PATH = os.path.join('./', 'tmp', 'temp_save')
MODEL_NAME = "model.keras"
MODEL_PATH = os.path.join("..", "model")

REDUNDANCY = 5
DELAY_IN_SECONDS = 1

if len(sys.argv) > 1:
    REDUNDANCY = int(sys.argv[1])

if len(sys.argv) > 2:
    DELAY_IN_SECONDS = float(sys.argv[2])

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def normalize_images(images):
    return images / 255

def save_frames(redundancy, delay): # Open the camera
    try:
        print("-- GETTING FRAMES FROM LIVESTREAM")
        frames_angle_one = st.Stream.getFrame(640, 480, 0, redundancy, FPS * delay)
        print("--- STARTPOSITIONS RETRIEVED")
        frames_angle_two = st.Stream.getFrame(640, 480, (RT - ((redundancy * delay) - delay)) * FPS, redundancy, FPS * delay)
        print("--- ENDPOSITION RETRIEVED\n")

    except:
        print("CONNECTION FAILED: GENERATING RANDOM COMBINATION")
        return False

    print("-- SAVING FRAMES TO DISK")
    if not os.path.exists(TEMP_PATH):    
        os.makedirs(TEMP_PATH)

    for i in range(0, redundancy):
        cv2.imwrite(os.path.join(TEMP_PATH, f'image{i + 1}_1.jpg'), frames_angle_one[i])

    for i in range(0, redundancy):
        cv2.imwrite(os.path.join(TEMP_PATH, f'image{i + 1}_2.jpg'), frames_angle_two[i])   

    return True

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

    print("\n")

    predicted_nummeric = np.argmax(predictions, axis=-1)
    predicted_readable = np.vectorize(label_mapping.get)(predicted_nummeric)

    print("PREDICTIONS: \n")
    print(predicted_readable)
    print("\n\n")

    result_one = calculate_final_result_algorithmus_1(predicted_nummeric)

    print("\n")
    print("RESULT: \n")
    print(np.vectorize(label_mapping.get)(result_one))
    print("\n\n")

    # result_two = calculate_final_result_algorithmus_2(predicted_nummeric)

    # print("ALGORITHMUS 2: FINAL RESULT: \n")
    # print(result_two)
    # print("\n")
    # print("READABLE: \n")
    # print(np.vectorize(label_mapping.get)(result_two))
    # print("\n\n")

    return np.vectorize(label_mapping.get)(result_one)

start_time = time.time()

print("RUNNING IN PROD MODE\n")
print(f"REDUNDANCIES: {REDUNDANCY}")
print(f"DELAY IN SECONDS: {DELAY_IN_SECONDS}\n")

print("- SAVING FRAMES")
response = save_frames(REDUNDANCY, DELAY_IN_SECONDS)

result = []

if response == True:
    filenames_1 = []
    filenames_2 = []

    for i in range(0, REDUNDANCY):
        filenames_1.append(f"image{i + 1}_1.jpg")
        filenames_2.append(f"image{i + 1}_2.jpg")

    print("\n- PREDICT POSITIONS\n")
    result = predict_positions(filenames_1, filenames_2)

else: 
    result = np.array(['', 'red', 'yellow', 'blue', '', 'blue', 'red', ''])

end_time = time.time()

elapsed_time = end_time - start_time

print("RESULT JSON: ")

print(hp.JSON.convert_numpy_to_json(result))

print("Elapsed time:", elapsed_time, "seconds")