import cv2
import numpy as np
import os
import json
import helper as hp
from PIL import Image
import keras.api._v2.keras as keras

MODEL_PATH = "../tmp/models/b6488696-cb4f-469b-b0d1-c1fa7866c24b"
color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def normalize_images(images):
    return images / 255


def main():
    image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/train/ressources/b6488696-cb4f-469b-b0d1-c1fa7866c24b/Test/Images/Image_4737_1.jpg"))
    image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/train/ressources/b6488696-cb4f-469b-b0d1-c1fa7866c24b/Test/Images/Image_4737_2.jpg"))

    image_one = np.array(image_one)[:, :, ::-1]
    image_two = np.array(image_two)[:, :, ::-1]

    hp.Out.image_show("Eingabe 1", image_one, True)
    hp.Out.image_show("Eingabe 2", image_two, True)

    while True:
        if cv2.waitKey(1) == 13:
            break

    image_one = hp.Preprocess.process_color(image_one, hp.HSVRanges.light_grey_color, hp.BGRColors.white_color)
    image_two = hp.Preprocess.process_color(image_two, hp.HSVRanges.light_grey_color, hp.BGRColors.white_color)

    hp.Out.image_show("Eingabe 1", image_one, True)
    hp.Out.image_show("Eingabe 2", image_two, True)

    while True:
        if cv2.waitKey(1) == 13:
            break

    image_one = hp.Preprocess.process_color(image_one, hp.HSVRanges.red_color, hp.BGRColors.red_color)
    image_two = hp.Preprocess.process_color(image_two, hp.HSVRanges.red_color, hp.BGRColors.red_color)

    hp.Out.image_show("Eingabe 1", image_one, True)
    hp.Out.image_show("Eingabe 2", image_two, True)

    while True:
        if cv2.waitKey(1) == 13:
            break


    image_one = hp.Preprocess.process_color(image_one, hp.HSVRanges.blue_color, hp.BGRColors.blue_color)
    image_two = hp.Preprocess.process_color(image_two, hp.HSVRanges.blue_color, hp.BGRColors.blue_color)

    hp.Out.image_show("Eingabe 1", image_one, True)
    hp.Out.image_show("Eingabe 2", image_two, True)

    while True:
        if cv2.waitKey(1) == 13:
            break

    
    image_one = hp.Preprocess.process_color(image_one, hp.HSVRanges.yellow_color, hp.BGRColors.yellow_color)
    image_two = hp.Preprocess.process_color(image_two, hp.HSVRanges.yellow_color, hp.BGRColors.yellow_color)
    
    hp.Out.image_show("Eingabe 1", image_one, True)
    hp.Out.image_show("Eingabe 2", image_two, True)

    while True:
        if cv2.waitKey(1) == 13:
            break

    hsv = cv2.cvtColor(image_one, cv2.COLOR_BGR2HSV)
    color_mask = hp.Mask.create_color_mask(hsv, hp.HSVRanges.red_color + hp.HSVRanges.blue_color + hp.HSVRanges.yellow_color + hp.HSVRanges.light_grey_color)
    image_one = cv2.bitwise_or(image_one, image_one, mask=color_mask)

    hsv = cv2.cvtColor(image_two, cv2.COLOR_BGR2HSV)
    color_mask = hp.Mask.create_color_mask(hsv, hp.HSVRanges.red_color + hp.HSVRanges.blue_color + hp.HSVRanges.yellow_color + hp.HSVRanges.light_grey_color)
    image_two = cv2.bitwise_or(image_two, image_two, mask=color_mask)

    hp.Out.image_show("Eingabe 1", image_one, True)
    hp.Out.image_show("Eingabe 2", image_two, True)

    while True:
        if cv2.waitKey(1) == 13:
            break

    image_one = cv2.resize(image_one, (320, 180))
    image_two = cv2.resize(image_two, (320, 180))

    hp.Out.image_show("Eingabe 1", image_one, True)
    hp.Out.image_show("Eingabe 2", image_two, True)

    while True:
        if cv2.waitKey(1) == 13:
            break


    images = []

    normalized_one = normalize_images(image_one)
    normalized_two = normalize_images(image_two)

    images.append([normalized_one, normalized_two])

    images = np.array(images)

    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH))

    predictions = np.argmax(model.predict([images[:, 0], images[:, 1]]), axis=-1)

    for prediction in predictions:
        predicted_readable = np.vectorize(label_mapping.get)(prediction)
        print("\n\n")
        print(f"------ PREDICTION --------\n")

        print("NUMMERIC:")
        print(prediction)
        print("\n")

        print("READABLE:")
        print(predicted_readable)
        print("\n\n")


if __name__ == "__main__":
    main()