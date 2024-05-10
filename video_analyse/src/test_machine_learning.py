import os
import numpy as np
import keras.api._v2.keras as keras
import time
import helper as hp
import cv2
from PIL import Image


# MODEL_PATH = "../model/v1_no_base_50000.keras"
# MODEL_PATH = "../tmp/models/v2_no_base_100000.keras"
# MODEL_PATH = "../model/v1_no_base_10000.keras"
# MODEL_PATH = "../tmp/models/v3_no_base_100000.keras"
# MODEL_PATH = "../tmp/models/v1_no_base_150000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_10000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_20000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_30000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_40000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_50000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_60000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_70000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_120000.keras"

# MODEL_PATH = "../tmp/models/v6_no_base_50000.keras"
# MODEL_PATH = "../tmp/models/v7_no_base_50000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_10000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_20000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_30000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_50000.keras"
# MODEL_PATH = "../tmp/models/v2_E25_50000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_90000.keras"

# MODEL_PATH = "../tmp/models/v2_E25_PAT4_10000.keras"
# MODEL_PATH = "../tmp/models/v1_E50_PAT5_10000.keras"

# MODEL_PATH = "../tmp/models/v1_E25_PAT4_20000.keras" # 95.6%

# MODEL_PATH = "../tmp/models/v1_E50_PAT4_LR05_PAT1_10000.keras"

# MODEL_PATH = "../tmp/models/v2_E25_PAT4_20000.keras" 
# MODEL_PATH = "../tmp/models/v2_E50_PAT4_10000.keras"
# MODEL_PATH = "../tmp/models/v2_E50_PAT4_LR_10000.keras"

# MODEL_PATH = "../tmp/models/v1_E25_PAT4_30000.keras"

# MODEL_PATH = "../tmp/models/v1_E25_PAT4_LRF08_10000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_PAT4_LRF04_10000.keras"

# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_10000.keras" # 96.25
# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_20000.keras"

# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL00001_LR05_PAT1_10000.keras"
# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_DATASET2_10000.keras" # 96.99%
# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_TRANSLATE_10000.keras"

# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_DATASET3_10000.keras" # 95
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATE_30000.keras"
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_30000.keras" # 97%
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_50000.keras" # 97%

MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_30000.keras" # 98%

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
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 3, 2, 2, 3, 3, 1, 0]),
        'name': 'f33fa7bf-4a55-47c1-85bf-3c62ea456efc'
    },       
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 3, 2, 2, 3, 3, 1, 0]),
        'name': '6137b988-bfa4-4aa8-8034-f91382cbd425'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 1, 2, 2, 3, 3, 3, 0]),
        'name': 'a2ce3e86-8590-4986-8c36-07e931b1dfaa'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([3, 1, 3, 2, 3, 0, 3, 3]),
        'name': '958960b8-aeb3-403f-89ba-862ec773bd51'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([3, 1, 3, 2, 3, 0, 3, 3]),
        'name': '51cd8bf3-1ea3-4bc4-aa5e-f7c117f0d3a6'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 1, 3, 2, 2, 1, 3, 3]),
        'name': '46ae10ae-bf46-46a8-81b0-a69dfdef9d51'
    }, 
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 3, 0, 1, 3, 3, 2, 1]),
        'name': '29b57f52-82b5-422d-af4b-186e72f509b2'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 1, 3, 3, 3, 3, 3, 3]),
        'name': '635eabd2-6084-4413-bcb8-f80bd05556d4'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([3, 2, 0, 0, 3, 1, 1, 3]),
        'name': 'dfbdb9fe-0e53-4d8e-829c-6cfd0a968bc1'
    },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 2, 0, 0, 0, 1, 1, 2]),
    #     'name': '22710caf-0412-4d7a-b986-4d2e599c5efc'
    # },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 0, 1, 2, 1, 2, 0, 1]),
        'name': 'd95bcdb3-0dee-452e-9979-8268f9345d66'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 0, 1, 2, 1, 2, 0, 1]),
        'name': '91cbc884-e0cf-49fa-9c9f-1175986c4716'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 0, 1, 2, 1, 2, 0, 1]),
        'name': '4cb8d403-328f-4e44-8f50-e6b5ed25a1e2'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([3, 0, 1, 2, 3, 2, 0, 3]),
        'name': 'd00b6d45-25d6-4baf-909a-fe36c1af2f90'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([3, 0, 1, 2, 3, 2, 0, 3]),
        'name': '3a83a9f6-35e6-4aef-9302-36895b42aa92'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 0, 1, 2, 1, 2, 0, 0]),
        'name': 'a44f06a7-7a0a-4e3f-827a-936fdbe1bdff'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 0, 2, 2, 0, 1, 1, 0]),
        'name': 'b535d337-68fe-4ebe-a7c6-8146c962b401'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 0, 2, 2, 0, 1, 1, 0]),
        'name': 'cd30bc4b-735b-4e2b-99c6-e497c3d5cc1b'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 0, 3, 0, 3, 1, 3, 1]),
        'name': '9087d8e9-2e84-4dda-a786-5697aae54552'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 0, 3, 0, 3, 1, 3, 1]),
        'name': '0eeb1650-c02f-421e-97c6-b90e395a2f25'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([3, 0, 0, 0, 3, 1, 2, 3]),
        'name': '4c20a053-09c2-4b7c-a9c7-269fcac8a0d6'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 1, 3, 0, 3, 1, 3, 3]),
        'name': 'ec511388-1d57-4b0b-accd-3e8bc5ba4b70'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([1, 1, 2, 1, 3, 3, 2, 3]),
        'name': 'b2d4eb7e-835d-40ee-9f47-803cf33e2aae'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 3, 0, 1, 3, 3, 3, 3]),
        'name': '5ad4c890-fbe0-491f-9674-8cfa78f0cfd1'
    },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([2, 3, 3, 1, 3, 3, 3, 0]),
    #     'name': '3901c79d-3576-4a63-a8b5-52f7c0774731'
    # },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 2, 0, 0, 0, 3, 1, 3]),
        'name': '9734b4dc-58ab-4173-881f-e8225841b0a4'
    }
]

IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160
NORMALIZE_VALUE = 255
IN_DEBUG_MODE = False

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

def compare_arrays(arr1, arr2, not_3_err):
    # Convert arrays to numpy arrays if they are not already
    arr1 = np.array(arr1)
    arr2 = np.array(arr2)
    
    # Find differing values and their positions
    differing_values = np.where(arr1 != arr2)[0]

    
    # Prepare the result
    result = []
    for i, pos in enumerate(differing_values):
        if arr2[pos] != 3:
            not_3_err = not_3_err + 1
        
        result.append(f"{i+1}. Pos: {pos}, Value: {arr2[pos]}")
    
    return result, not_3_err
    
def print_table(data):
    headers = ["Bundle", "ID", "Actual", "Prediction", "Accuracy", "Diff"]
    col_width = [max(len(str(d[col])) for d in data) for col in headers]

    separator = "+".join(["-" * (w + 2) for w in col_width])
    print(separator)
    print("| {:s} | {:s} | {:s} | {:s} | {:s} |".format(*headers, *col_width)) 
    print(separator)

    counter = 0

    for row in data:
        actual_value_str = str(row["Actual"])
        prediction = row["Prediction"]
        accuracy = row.get("Accuracy")

        if accuracy > 87.5 or accuracy == 0:
            continue
        
        counter = counter + 1
        print("| %s | %d | %s | %s | %.2f | %s |" % (row["Bundle"], row["ID"], actual_value_str, prediction, accuracy, row["Diff"]))  
    print(separator)
    print("Amount (<= 87.5%): " + str(counter))
    print("Total: " + str(len(data)))

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

            # image = hp.Augmentation.black_spots(image, 100)

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
    images = np.array(images)

    predictions = np.argmax(predict(model, images), axis=-1)

    data = []

    index = 0

    total_accuracy = 0

    not_3_err = 0


    for bundle in BUNDLES:
        files = os.listdir(os.path.join(bundle['path'], bundle['name']))
        for i in range(0, int(len(files) / 2)):
            intersection = np.sum(bundle['result'] == predictions[index])
            coverage_percent = (intersection / len(bundle['result'])) * 100
            diff, not_3_err = compare_arrays(bundle['result'], predictions[index], not_3_err)

            data.append({"Bundle": bundle['name'], "ID": index + 1, "Actual": np.array2string(bundle['result']), "Prediction": np.array2string(predictions[index]), "Accuracy": coverage_percent, "Diff": diff})
            index = index + 1
            total_accuracy = total_accuracy + coverage_percent

    print_table(data)

    print(f"\n\n Total Accuracy: {total_accuracy / index}")
    print(f"\n Total errors confusing colors: " + str(not_3_err))

if __name__ == "__main__":
    main()

