import os
import numpy as np
import keras.api._v2.keras as keras
import time
import helper as hp
import cv2
from PIL import Image


# MODEL_PATH = "../model/v1_no_base_50000.keras"
MODEL_PATH = "../tmp/models/v2_no_base_100000.keras"
BUNDLES = [
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 3, 2, 2, 3, 3, 1, 0]),
        'name': 'f640e372-95ce-4fc9-a614-cbddb3e5710b'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 3, 2, 2, 3, 3, 1, 0]),
        'name': 'a5119e66-947d-45e0-b229-549b1ca79393'
    }        
]

VIDEO_STREAM_URL = 'http://127.0.0.1:5000/video_feed'


IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160

NORMALIZE_VALUE = 255

IN_DEBUG_MODE = False

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
    return model.predict([input[:, 0], input[:, 1]])
    
def print_table(data):
    headers = ["ID", "Actual", "Prediction", "Accuracy"]
    col_width = [max(len(str(d[col])) for d in data) for col in headers]

    separator = "+".join(["-" * (w + 2) for w in col_width])
    print(separator)
    print("| {:s} | {:s} | {:s} | {:s} |".format(*headers, *col_width))  # String formatting method
    print(separator)

    for row in data:
        actual_value_str = str(row["Actual"])
        prediction = row["Prediction"]
        accuracy = row.get("Accuracy")
        print("| %d | %s | %s | %.2f |" % (row["ID"], actual_value_str, prediction, accuracy))  
    print(separator)

def main():
    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH))

    if IN_DEBUG_MODE:
        model.summary()

    images = []

    for bundle in BUNDLES:
        filenames = sorted(os.listdir(os.path.join(bundle['path'], bundle['name'])))

        for i, filename in enumerate(filenames):
            full_path = os.path.join(bundle['path'], bundle['name'], filename)
            image = Image.open(full_path)
            image = image.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
            image = np.array(image)[:, :, ::-1]
            image = image[0:115, 10:150]
            image = hp.Preprocess.start(image)

            if IN_DEBUG_MODE:
                hp.Out.image_show("Image", image, IN_DEBUG_MODE)

                while True:
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                        break
            
            normalized = normalize_images(image)
                       

            if i % 2 == 0:
                images.append([normalized])
            else:
                images[len(images) - 1].append(normalized)
        print(filenames)
    
    images = np.array(images)

    predictions = np.argmax(predict(model, images), axis=-1)

    data = []

    index = 0

    total_accuracy = 0

    for bundle in BUNDLES:
        files = os.listdir(os.path.join(bundle['path'], bundle['name']))
        for i in range(0, int(len(files) / 2)):
            common_elements = np.count_nonzero(np.in1d(bundle['result'], predictions[index]))
            coverage_percent = (common_elements / len(predictions[index])) * 100
            data.append({"ID": index + 1, "Actual": np.array2string(bundle['result']), "Prediction": np.array2string(predictions[index]), "Accuracy": coverage_percent})
            index = index + 1
            total_accuracy = total_accuracy + coverage_percent

    print_table(data)

    print(f"\n\n Total Accuracy: {total_accuracy / index}")

if __name__ == "__main__":
    main()

