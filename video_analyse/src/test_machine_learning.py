import os
import numpy as np
import keras.api._v2.keras as keras
import time
import helper as hp
import cv2
import requests
from io import BytesIO
from PIL import Image


MODEL_PATH = "../tmp/models/f2cffe42-a088-479b-9eef-c5b0b8621322"
VIDEO_PATHS = [
    '../ressources/video_example/01_config.mp4',
    '../ressources/video_example/02_config.mp4',
    '../ressources/video_example/03_config.mp4'
]

SNIPPET_PATHS = [
    {
        'one': '../ressources/video_example/config_1_snippets/pos1_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/pos1_2.jpg'
    },
    {
        'one': '../tmp/train/ressources/f2cffe42-a088-479b-9eef-c5b0b8621322/Test/Images/Image_9001_1.jpg',
        'two': '../tmp/train/ressources/f2cffe42-a088-479b-9eef-c5b0b8621322/Test/Images/Image_9001_2.jpg',
    }
]

VIDEO_STREAM_URL = 'http://127.0.0.1:5000/video_feed'


IMAGE_HEIGHT_PX = 180
IMAGE_WIDTH_PX = 320
NORMALIZE_VALUE = 255

STRATEGY = 2
IN_DEBUG_MODE = True
FRAME_STEP_BY_STEP = True

HALF_ROTATION_TIME = 15

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def check_time_passed(start_time, interval):
    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time >= interval

def normalize_images(images):
    return images / NORMALIZE_VALUE

def predict(model, input):
    if STRATEGY == 1:
        return model.predict(input)

    if STRATEGY == 2:
        return model.predict([input[:, 0], input[:, 1]])

# def main():
#     response = requests.get(VIDEO_STREAM_URL, stream=True).raw

#     frame = cv2.imdecode(np.frombuffer(response.read(), dtype=np.uint8), cv2.IMREAD_COLOR)

#     print("Herer")
#     hp.Out.image_show("Frame", frame, IN_DEBUG_MODE)

#     if IN_DEBUG_MODE:

#         if FRAME_STEP_BY_STEP:
#             while True:
#                 # Press enter to run next frame
#                 if cv2.waitKey(1) == 13:
#                     break

#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     exit_analyse = True
#                     break


def main():
    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH))

    if IN_DEBUG_MODE:
        model.summary()

    images = []

    for snippets in SNIPPET_PATHS:
        image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), snippets['one']))
        image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), snippets['two']))

        image_one = image_one.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        image_two = image_two.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))

        # Channel order of Pillow is different than OpenCV
        image_one = np.array(image_one)[:, :, ::-1]
        image_two = np.array(image_two)[:, :, ::-1]

        # hsv = cv2.cvtColor(image_one, cv2.COLOR_BGR2HSV)
        # color_mask = hp.Mask.create_color_mask(hsv, hp.HSVRanges.light_grey_color + hp.HSVRanges.blue_color + hp.HSVRanges.red_color + hp.HSVRanges.yellow_color)
        # image_one = cv2.bitwise_and(image_one, image_one, mask=color_mask)

        # hsv = cv2.cvtColor(image_two, cv2.COLOR_BGR2HSV)
        # color_mask = hp.Mask.create_color_mask(hsv, hp.HSVRanges.light_grey_color + hp.HSVRanges.blue_color + hp.HSVRanges.red_color + hp.HSVRanges.yellow_color)
        # image_two = cv2.bitwise_and(image_two, image_two, mask=color_mask)

        hp.Out.image_show("one", image_one, IN_DEBUG_MODE)
        hp.Out.image_show("two", image_two, IN_DEBUG_MODE)

        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break

        normalized_one = normalize_images(image_one)
        normalized_two = normalize_images(image_two)

        images.append([normalized_one, normalized_two])

    images = np.array(images)
    print(images.shape)
    predictions = np.argmax(predict(model, images), axis=-1)

    index = 0

    for prediction in predictions:
        predicted_readable = np.vectorize(label_mapping.get)(prediction)
        print("\n\n")
        print(f"------ PREDICTION: snippets {index} --------\n")


        print("NUMMERIC: \n")
        print(prediction)
        print("READABLE: \n")
        print(predicted_readable)
        print("\n\n")

        index = index + 1



# def main():
#     model = []
#     model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH))

#     if IN_DEBUG_MODE:
#         model.summary()

#     video_predictions = {
#         "config_one": [],
#         "config_two": [],
#         "config_three": []
#     }

#     for video_path in VIDEO_PATHS:


#         start_time = time.time()

#         cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), video_path))

#         predictions = []
#         images = []
#         index = 0

#         while True:
#             ret, frame = cap.read()


#             if not ret:
#                 print("VIDEO FINISHED")
#                 break

#             frame = cv2.resize(frame, (IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))

#             hp.Out.image_show("OUT", frame, IN_DEBUG_MODE)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#             if (index != 0):
#                 if not check_time_passed(start_time, HALF_ROTATION_TIME / 2):
#                     continue

#             normalized = normalize_images(frame)

#             images.append(normalized)

#             if index != 0:
#                 break

#             index = index + 1



#         print(len(images))
#         print(len(images[: 0]))
#         print(len(images[: 1]))
#         print(np.array(images).shape)
#         print(np.array([np.array(images)]).shape)


#         predictions = predict(model, np.array([np.array(images)]))

#         print("\n\n")
#         print(f"------ PREDICTION: video {video_path} --------\n")
#         predicted_nummeric = np.argmax(predictions, axis=-1)
#         predicted_readable = np.vectorize(label_mapping.get)(predicted_nummeric)

#         print("NUMMERIC: \n")
#         print(predicted_nummeric)
#         print("READABLE: \n")
#         print(predicted_readable)
#         print("\n\n")

#     return

if __name__ == "__main__":
    main()

