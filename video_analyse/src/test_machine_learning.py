import os
import numpy as np
import keras.api._v2.keras as keras
import time
import helper as hp
import cv2
from PIL import Image


MODEL_PATH = "../tmp/models/v1_no_base_50000.keras"

VIDEO_PATHS = [
    '../ressources/video_example/01_config.mp4',
    '../ressources/video_example/02_config.mp4',
    '../ressources/video_example/03_config.mp4'
]

SNIPPET_PATHS = [
    {
        'one': '../ressources/video_example/config_1_snippets/image1_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image1_2.jpg'
    },
    {            
        'one': '../ressources/video_example/config_1_snippets/image2_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image2_2.jpg'
    },
    {
        'one': '../ressources/video_example/config_1_snippets/image3_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image3_2.jpg'
    },
    {
        'one': '../ressources/video_example/config_1_snippets/image4_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image4_2.jpg'
    },
    {
        'one': '../ressources/video_example/config_1_snippets/image5_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image5_2.jpg'
    },
    {
        'one': '../ressources/video_example/config_1_snippets/image6_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image6_2.jpg'
    },
    {
        'one': '../ressources/video_example/config_1_snippets/image7_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image7_2.jpg'
    },
    {
        'one': '../ressources/video_example/config_1_snippets/image8_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image8_2.jpg'
    },
    {
        'one': '../ressources/video_example/config_1_snippets/image9_1.jpg',
        'two': '../ressources/video_example/config_1_snippets/image9_2.jpg'
    },
]

VIDEO_STREAM_URL = 'http://127.0.0.1:5000/video_feed'


IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160

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

        image_one = image_one[0:115, 10:150]
        image_two = image_two[0:115, 10:150]

        image_one = hp.Preprocess.start(image_one)
        image_two = hp.Preprocess.start(image_two)

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


if __name__ == "__main__":
    main()

