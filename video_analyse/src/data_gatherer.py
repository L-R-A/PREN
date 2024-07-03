import cv2
import stream_image as st
import time
import uuid
import os

def gather_images(bundle_name, amount):
    frames_1 = st.Stream.getFrame(640, 480, 0, amount, 1)
    frames_2 = st.Stream.getFrame(640, 480, 0, amount, 1)

    if not os.path.exists(f'./tmp/ressources/{bundle_name}'):
        
        os.makedirs(os.path.join('./', 'tmp', 'ressources', bundle_name))

    for i, frame in enumerate(frames_1):
        cv2.imwrite(os.path.join('./', 'tmp', 'ressources', bundle_name, f'image{i}_1.jpg'), frame) 

    for i, frame in enumerate(frames_2):
        cv2.imwrite(os.path.join('./', 'tmp', 'ressources', bundle_name, f'image{i}_2.jpg'), frame) 

uuid = uuid.uuid4()
amount = 300

if __name__ == '__main__':
    gather_images(str(uuid), amount)
