import os
import numpy as np
import keras.api._v2.keras as keras
from PIL import Image

MODEL_PATH = "../tmp/models/b5fee2f7-e6c1-4e97-83b2-710c5393cc14"

SNIPPET_PATHS = [
    {
        'one': './images/Image_9050_1.jpg',
        'two': './images/Image_9050_2.jpg',
    },
]

IMAGE_HEIGHT_PX = 180
IMAGE_WIDTH_PX = 320
NORMALIZE_VALUE = 255

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def normalize_images(images):
    return images / NORMALIZE_VALUE



def main():
    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH))
    images = []

    for snippets in SNIPPET_PATHS:
        image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), snippets['one']))
        image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), snippets['two']))

        image_one = image_one.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        image_two = image_two.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))

        image_one = np.array(image_one)[:, :, ::-1]
        image_two = np.array(image_two)[:, :, ::-1]

        normalized_one = normalize_images(image_one)
        normalized_two = normalize_images(image_two)

        images.append([normalized_one, normalized_two])

    images = np.array(images)

    
    predictions = np.argmax(model.predict([images[:, 0], images[:, 1]]), axis=-1)


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