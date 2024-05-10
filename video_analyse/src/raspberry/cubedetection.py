import cv2
import rasp_helper as hp
import numpy as np
import os
import keras.api._v2.keras as keras
import rasp_stream as st
from PIL import Image
import time
import sys
from time import sleep

IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160
FPS = 22
RT = 14
TEMP_PATH = os.path.join('./', 'tmp', 'temp_save')
# MODEL_NAME = os.path.join('..', '..', 'tmp', 'models', "v1_E100_PAT4_DEL0001_LR05_PAT1_30000.keras")
MODEL_NAME = "model.keras"
REDUNDANCY = 10
DELAY_IN_SECONDS = 0.5

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

class CubeDetection:
    def normalize_images(images):
        return images / 255

    def save_frames(redundancy, delay): # Open the camera
        try:
            print("-- GETTING FRAMES FROM LIVESTREAM")
            frames_angle_one = st.Stream.getFrame(640, 480, 0, redundancy, FPS * delay)
            print("--- STARTPOSITIONS RETRIEVED")
            frames_angle_two = st.Stream.getFrame(640, 480, (RT - ((redundancy * delay) - delay)) * FPS, redundancy, FPS * delay)
            print("--- ENDPOSITION RETRIEVED\n")

            print("-- SAVING FRAMES TO DISK")
            if not os.path.exists(TEMP_PATH):    
                os.makedirs(TEMP_PATH)

            for i in range(0, redundancy):
                cv2.imwrite(os.path.join(TEMP_PATH, f'image{i + 1}_1.jpg'), frames_angle_one[i])

            for i in range(0, redundancy):
                cv2.imwrite(os.path.join(TEMP_PATH, f'image{i + 1}_2.jpg'), frames_angle_two[i])   

            return True
    
        except:
            print("CONNECTION FAILED: GENERATING RANDOM COMBINATION")
            return False

    def get_unprio_empty_positions(predicted_nummeric):
        result = np.zeros_like(predicted_nummeric[0])

        for i in range(predicted_nummeric.shape[1]):
            values = predicted_nummeric[:, i]
            unique_values, counts = np.unique(values, return_counts=True)
            counts_dict = dict(zip(unique_values, counts))

            if 3 in counts_dict:
                del counts_dict[3]

            if not counts_dict:
                result[i] = 3
            else:
                majority_value = max(counts_dict, key=counts_dict.get)
                result[i] = majority_value

        return result
    
    def get_hightest_probability(arrays):
        result = arrays[0]
        
        for array in arrays[1:]:
            result = np.maximum(result, array)
        
        return result
    
    def get_most_common(arrays):
        result = np.zeros_like(arrays[0])

        for i in range(arrays.shape[1]):
            mode_value, mode_count = np.unique(arrays[:, i], return_counts=True)
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

            normalized_one = CubeDetection.normalize_images(image_one)
            image_pair.append([normalized_one]);
        print("-- PREPROCESSED AND NORMALIZED STARTPOSITIONS")

        for i, image_path in enumerate(image_path_two):
            full_path_two = os.path.join(TEMP_PATH, image_path)

            image_two = Image.open(full_path_two)
            image_two = image_two.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
            image_two = np.array(image_two)[:, :, ::-1]
            image_two = image_two[0:115, 10:150]
            image_two = hp.Preprocess.start(image_two)

            normalized_two = CubeDetection.normalize_images(image_two)
            image_pair[i].append(normalized_two);

        print("-- PREPROCESSED AND NORMALIZED ENDPOSITIONS")

        image_pair = np.array(image_pair)

        print("-- PREDICTING POSITIONS")

        predictions = model.predict([image_pair[:, 0], image_pair[:, 1]])
        predictions_max = np.argmax(predictions, axis=-1)

        highest_probabilty = CubeDetection.get_hightest_probability(predictions)

        common_prediction = CubeDetection.get_most_common(predictions_max)
        common_readable = np.vectorize(label_mapping.get)(common_prediction)

        highest_prediction = np.argmax(highest_probabilty, axis=-1)
        highest_probability_readable = np.vectorize(label_mapping.get)(highest_prediction)

        unprio_empty_prediction = CubeDetection.get_unprio_empty_positions(predictions_max)
        unprio_empty_readable = np.vectorize(label_mapping.get)(unprio_empty_prediction)

        print("\n")

        print("-- OUTPUT \n")

        print("--- COMMON: \n")
        print(common_readable)
        print("\n")
        print("--- HIGHEST: \n")
        print(highest_probability_readable)
        print("\n")
        print("--- UNPRIO EMPTY:")
        print(unprio_empty_readable)
        print("----------------------------------------------------")
        print("\n")
        print("--- FINAL RESULT: \n")
        final_prediction = CubeDetection.get_unprio_empty_positions(np.array([common_prediction, highest_prediction, unprio_empty_prediction]))
        final_readable = np.vectorize(label_mapping.get)(final_prediction)
        print(final_readable)


        print()
        print("\n\n")

        return final_readable
    
    def start():
        start_time = time.time()

        print("RUNNING IN PROD MODE\n")
        print(f"REDUNDANCIES: {REDUNDANCY}")
        print(f"DELAY IN SECONDS: {DELAY_IN_SECONDS}\n")

        print("- SAVING FRAMES")
        response = CubeDetection.save_frames(REDUNDANCY, DELAY_IN_SECONDS)

        result = []

        if response == True:
            filenames_1 = []
            filenames_2 = []

            for i in range(0, REDUNDANCY):
                filenames_1.append(f"image{i + 1}_1.jpg")
                filenames_2.append(f"image{i + 1}_2.jpg")

            print("\n- PREDICT POSITIONS\n")
            result = CubeDetection.predict_positions(filenames_1, filenames_2)

        else: 
            return np.array(['', 'red', 'yellow', 'blue', '', 'blue', 'red', '']).tolist()

        end_time = time.time()

        elapsed_time = end_time - start_time

        print("RESULT JSON: ")

        print("Elapsed time:", elapsed_time, "seconds")

        return result.tolist()

# ----------------- REMOVE THIS: ONLY FOR TESTING PURPOSES ------------------------

# i = 1

# while True:

#     print("Round: " + str(i) + "\n")
#     result = CubeDetection.start()

#     print(hp.JSON.convert_numpy_to_json(result))


#     if (result != ['blue', 'blue', 'red', 'red', 'red', '', 'yellow', '']):
#         print("ERROR IN PREDICTION")
#         break;
    
#     time.sleep(1.5)
    
    
#     i = i + 1

# ----------------- REMOVE THIS: ONLY FOR TESTING PURPOSES ------------------------
