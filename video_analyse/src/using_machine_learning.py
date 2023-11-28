import os
import json
from PIL import Image
import numpy as np
# import tensorflow as tf
import keras.api._v2.keras as keras


RESSOURCES_PATH = "../tmp/train/ressources/"
MODEL_PATH = "../tmp/models"
TRAIN_DATA_FOLDER = "047a698a-3b28-482b-b761-7778e2375849"
IMAGE_FOLDER = "Images"
LABELS_FOLDER = "Labels"
STRATEGY = 2
IN_DEBUG_MODE = True
JSON_NAME = "scene_results.json"

TRAIN_MODEL = True

IMAGE_HEIGHT_PX = 180
IMAGE_WIDTH_PX = 320
# RGB has 3 channels 
NUM_CHANNELS = 3
NUM_CLASSES = 4
NUM_POSITIONS = 8

NORMALIZE_VALUE = 255

LOSS_FUNCTION = 'categorical_crossentropy'

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }

def get_data(stage):
    labels = []
    images = []

    scene_results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), RESSOURCES_PATH, TRAIN_DATA_FOLDER, stage, JSON_NAME)

    if IN_DEBUG_MODE:
        print("CURRENT STAGE: " + stage + "\n")
        print("READING SCENE RESULTS AT: " + scene_results_path)


    with open(scene_results_path, 'r') as file:
        scene_results = json.load(file)

    for result in scene_results:
        img = [];

        for img_path in result["imagePaths"]:

            if IN_DEBUG_MODE:
                print("READING IMAGE AT: " + img_path)

            i = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), RESSOURCES_PATH, TRAIN_DATA_FOLDER, img_path))
            

            # Scale down image (resize)
            i = i.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))

            img.append(i)    

        images.append(img)
        labels.append(result["positions"])

    if IN_DEBUG_MODE:
        print("\n\n")

    return [images, labels]

def map_labels_to_nummeric(label):
    mapped_label = []

    for pos in label.values():
        mapped_label.append(color_mapping[pos])

    return mapped_label

# Normalize the images so that all values are between 0 and 1
def normalize_images(images):
    return images / NORMALIZE_VALUE

def get_base_model():
    return keras.models.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX, NUM_CHANNELS)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
    ])

def get_complete_model(base_model):
    input_image_1 = keras.layers.Input(shape=(IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX, NUM_CHANNELS), name='input_image_1')
    input_image_2 = keras.layers.Input(shape=(IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX, NUM_CHANNELS), name='input_image_2')

    encoded_left = base_model(input_image_1)
    encoded_right = base_model(input_image_2)

    concatenated = keras.layers.Concatenate(axis=-1)([encoded_left, encoded_right])

    dense_layer = keras.layers.Dense(NUM_POSITIONS * NUM_CLASSES, activation='softmax')(concatenated)
    reshaped_output = keras.layers.Reshape((NUM_POSITIONS, NUM_CLASSES))(dense_layer)

    return keras.models.Model(inputs=[input_image_1, input_image_2], outputs=reshaped_output)


# def get_siamese_network(base_model):
#     input_image_1 = keras.layers.Input(shape=(IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX, NUM_CHANNELS), name='input_image_1')
#     input_image_2 = keras.layers.Input(shape=(IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX, NUM_CHANNELS), name='input_image_2')

#     processed_image_1 = base_model(input_image_1)
#     processed_image_2 = base_model(input_image_2)

#     # concatenated = keras.layers.concatenate([processed_image_1, processed_image_2], axis=-1)

#     # x = keras.layers.Dense(256, activation='relu')(concatenated)
#     # x = keras.layers.Dropout(0.5)(x)
#     # x = keras.layers.Dense(128, activation='relu')(x)

#     L1_layer = keras.layers.Lambda(lambda tensors: abs(tensors[0] - tensors[1]))
#     L1_distance = L1_layer([processed_image_1, processed_image_2])

#     output_layer = keras.layers.Dense(NUM_CLASSES, activation='softmax', name='output')(L1_distance)

#     return keras.models.Model(inputs=[input_image_1, input_image_2], outputs=output_layer)

def create_model():
    model = get_base_model()
    # model = get_siamese_network(base_model)

    model = get_complete_model(model)

    optimizer = keras.optimizers.legacy.Adam(learning_rate=0.001)

    model.compile(optimizer=optimizer, loss=LOSS_FUNCTION, metrics=['accuracy'])

    if IN_DEBUG_MODE:
        model.summary()

    return model


def test_model(model, test_data):
    test_images = normalize_images(np.array((test_data[0])))

    return model.predict([test_images[:, 0], test_images[:, 1]])



def train_model():
    train_data = get_data("Train")
    verify_data = get_data("Verify")

    train_images = normalize_images(np.array(train_data[0]))
    numberic_train_labels = np.array([map_labels_to_nummeric(label) for label in train_data[1]])
    train_labels = keras.utils.to_categorical(numberic_train_labels, num_classes=NUM_CLASSES)

    verify_images = normalize_images(np.array((verify_data[0])))
    numberic_verify_labels = np.array([map_labels_to_nummeric(label) for label in verify_data[1]])
    verify_labels = keras.utils.to_categorical(numberic_verify_labels, num_classes=NUM_CLASSES)


    model = create_model()

    if IN_DEBUG_MODE: 
        print("----- SHAPES ------\n")
        print(f"Train labels shape: {train_labels.shape}")
        print(f"Train images shape: {train_images.shape}")

        print(f"Verify labels shape: {verify_labels.shape}")
        print(f"Verify images shape: {verify_images.shape}")

    model.fit(
        [train_images[:, 0], train_images[:, 1]], train_labels, 
        epochs=10, 
        validation_data=([verify_images[:, 0], verify_images[:, 1]], verify_labels), verbose= 1 if IN_DEBUG_MODE else 0)

    return model



def main():
    model = []
    if TRAIN_MODEL:
        model = train_model()
        model.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH, TRAIN_DATA_FOLDER))
    else:
        model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH, TRAIN_DATA_FOLDER))

    test_data = get_data("Test")
    test_labels = np.array([map_labels_to_nummeric(label) for label in test_data[1]])

    predictions = test_model(model, test_data)


    if IN_DEBUG_MODE:
        print("\n\n")
        print("------ PREDICTIONS --------\n\n")
        predicted_indices = np.argmax(predictions, axis=-1)
        print(predicted_indices)

        print("\n\n")

        print("------ ACTUAL RESULTS ------ \n\n")
        print(test_labels)


    return


if __name__ == "__main__":
    main()