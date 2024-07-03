import cv2
import numpy as np
import os
import json
import helper as hp
from PIL import Image

#region CONFIGURATION CONSTANTS

VIDEO_PATH = '../ressources/video_example/01_config.mp4'

IN_DEBUG_MODE = True
FRAME_STEP_BY_STEP = True

ROTATION_SIDES = 4

CHECKED_FRAMES_PER_SIDE = 10

OUTPUT_FILE_NAME = "output.json"
OUTPUT_FILE_DIR = "../tmp"


SNIPPET_PATHS = [
    # {
    #     'one': '../ressources/video_example/config_1_snippets/pos1_1.jpg',
    #     'two': '../ressources/video_example/config_1_snippets/pos1_2.jpg'
    # },
    {
        'one': '../tmp/train/ressources/f2cffe42-a088-479b-9eef-c5b0b8621322/Test/Images/Image_9005_1.jpg',
        'two': '../tmp/train/ressources/f2cffe42-a088-479b-9eef-c5b0b8621322/Test/Images/Image_9005_2.jpg',
    },
    {
        'one': '../tmp/train/ressources/b5fee2f7-e6c1-4e97-83b2-710c5393cc14/Test/Images/Image_9030_1.jpg',
        'two': '../tmp/train/ressources/b5fee2f7-e6c1-4e97-83b2-710c5393cc14/Test/Images/Image_9030_2.jpg'
    },
    {
        'one': '../tmp/train/ressources/b5fee2f7-e6c1-4e97-83b2-710c5393cc14/Test/Images/Image_9050_1.jpg',
        'two': '../tmp/train/ressources/b5fee2f7-e6c1-4e97-83b2-710c5393cc14/Test/Images/Image_9050_2.jpg'
    }
]

#endregion

#region CORDINATE CALCULATION

def calculate_object_cordinates_with_blob_detection(gray_image, image):
    params = cv2.SimpleBlobDetector.Params()
    params.filterByColor = True
    params.blobColor = 255

    # params.filterByArea = True
    # params.minArea = 100

    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(gray_image, kernel, iterations=1)
    dilate = cv2.dilate(eroded, kernel, iterations=1)

    # Use blob detection on the mask to identify objects
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(dilate)

    print(keypoints)


    # Loop through the detected keypoints (blobs)
    for keypoint in keypoints:
        x, y, size = int(keypoint.pt[0]), int(keypoint.pt[1]), int(keypoint.size)
        cv2.circle(image, (x, y), size, (0,0,255), 2)

        # Calculate the top-left and bottom-right coordinates of the bounding box
        top_left = (x - size // 2, y - size // 2)
        bottom_right = (x + size // 2, y + size // 2)

        # Draw a rectangle (border) around the blob
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)  # You can change the color and thickness as needed


#endregion

#region IMAGE_PROECESSING

def erode_image_processing(non_erode_mask, result):
    eroded_mask = hp.Video.eroded_mask(non_erode_mask)
    eroded_mask2 = hp.Video.eroded_mask(non_erode_mask, (10,10))        
    eroded_mask3 = hp.Video.eroded_mask(non_erode_mask, (20,20))
    eroded_mask4 = hp.Video.eroded_mask(non_erode_mask, (50,50))


    test = cv2.bitwise_and(result, result, mask=non_erode_mask)
    test2 = cv2.bitwise_and(result, result, mask=eroded_mask)
    test3 = cv2.bitwise_and(result, result, mask=eroded_mask2)
    test4 = cv2.bitwise_and(result, result, mask=eroded_mask3)
    test5 = cv2.bitwise_and(result, result, mask=eroded_mask4)

    hp.Out.image_show('no erode', test, IN_DEBUG_MODE)
    hp.Out.image_show('erode (5,5)', test2, IN_DEBUG_MODE)
    hp.Out.image_show('erode (10,10)', test3, IN_DEBUG_MODE)
    hp.Out.image_show('erode (20,20)', test4, IN_DEBUG_MODE)
    hp.Out.image_show('erode (50,50)', test5, IN_DEBUG_MODE)

def gamma_correction(gray, result):
    gamma = hp.Video.gamma_correction(gray, 1.5)

    test = cv2.bitwise_and(result, result, mask=gamma)

    hp.Out.image_show('no gamma', result, IN_DEBUG_MODE)
    hp.Out.image_show('gamma', test, IN_DEBUG_MODE)


def contrast_stretching(gray, result):
    stretched = hp.Video.contrast_stretching(gray)

    test = cv2.bitwise_and(result, result, mask=stretched)

    hp.Out.image_show('no stretching', result, IN_DEBUG_MODE)
    hp.Out.image_show('stretching', test, IN_DEBUG_MODE)


def contour_enhancement(gray, result):
    # clahe = hp.Video.clahe_correction(gray)
    stretched = hp.Video.contrast_stretching(gray)
    # gamma = hp.Video.gamma_correction(stretched)
    blur = hp.Video.blur_mask(stretched)
    threshed = hp.Video.threshold_mask(blur)
    # eroded_mask = hp.Video.eroded_mask(threshed)


    min_contour_area = 1000  # Adjust this value as needed

    contours, _ = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    c = 0
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if min_contour_area <= contour_area:
            if contour_area > max_area:
                    max_area = contour_area
                    best_cnt = contour
                    result = cv2.drawContours(result, contours, c, (0, 255, 0), 2)
        c+=1

    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)

    print(mask == 0)


    # segment regions of interests (no biggest contours)
    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]

    # hp.Out.image_show("Out image", out, IN_DEBUG_MODE)

    # Image preprocessing
    blur = hp.Video.blur_mask(out)
    processed = hp.Video.threshold_mask(blur)
    eroded = hp.Video.eroded_mask(processed, (10,10))

    # hp.Out.image_show("Enhanced image", eroded, IN_DEBUG_MODE)

    contours, _ = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    c = 0
    for i in contours:
            cv2.drawContours(result, contours, c, (0, 0, 0), 2)
            c+=1



    # Draw the contours on the result image
    # cv2.drawContours(result, contours, -1, (0, 0, 0), -1)  # -1 means fill the contours

    # Display the result (you can also save it if needed)
    # hp.Out.image_show("Result", result, IN_DEBUG_MODE)

    # test = cv2.bitwise_or(result, result, mask=threshed)
    
    # image_show('Contour enhanced Mask', threshed)
    # image_show('Contour enhanced bitwise and', test)
    # image_show('Original', result)


#endregion


def cube_detection(frame):
    # Preprocess the image (e.g., convert to grayscale, apply thresholding)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Find contours of the cubes
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the position of each cube
    cube_positions = []
    grid_size = (2, 2, 2)  # Rows, columns, height
    for contour in contours:
        if cv2.contourArea(contour) > 1:
            # Calculate the centroid of the cube
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])


                # Use the centroid to calculate the position in the grid
                cube_x = int(cx / (frame.shape[1] / grid_size[1]))
                cube_y = int(cy / (frame.shape[0] / grid_size[0]))
                cube_z = 0  # Assuming all cubes are at the same height
                
                cube_positions.append((cube_x, cube_y, cube_z))

    # Display the image with cube positions marked
    for x, y, z in cube_positions:
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    # hp.Out.image_show("RESULT", frame, IN_DEBUG_MODE)

IMAGE_HEIGHT_PX = 120
IMAGE_WIDTH_PX = 160
def main():
    # video = hp.Video(os.path.join(os.path.dirname(os.path.abspath(__file__)), VIDEO_PATH))
    exit_analyse = False

    i = 1

    while True: 
        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/train/ressources/bundle/1f7534fa-6ee2-4e6a-a921-2a635a5fe917/Train/Images/Image_{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/train/ressources/bundle/1f7534fa-6ee2-4e6a-a921-2a635a5fe917/Train/Images/Image_{i}_2.jpg"))

        image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"./raspberry/tmp/temp_save/image1_2.jpg"))

        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/3a9921a1-74cb-4c75-a3cd-f70fea582a6f/image{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/3a9921a1-74cb-4c75-a3cd-f70fea582a6f/image{i}_2.jpg"))

        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/464404c7-d7bf-44f6-95ac-d792597029e6/image{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/464404c7-d7bf-44f6-95ac-d792597029e6/image{i}_2.jpg"))

        image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/98e2963c-1dc7-4687-844e-0f76f0bedf09/image{i}_1.jpg"))
        image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/98e2963c-1dc7-4687-844e-0f76f0bedf09/image{i}_2.jpg"))

       


        # OLDDD
        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/46ae10ae-bf46-46a8-81b0-a69dfdef9d51/image{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/46ae10ae-bf46-46a8-81b0-a69dfdef9d51/image{i}_2.jpg"))

        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/f7cc00ed-27bc-47f5-aca3-0cfd83091176/image{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/f7cc00ed-27bc-47f5-aca3-0cfd83091176/image{i}_2.jpg"))

        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/7b923782-f604-4306-ad58-3f3461a36d76/image{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/7b923782-f604-4306-ad58-3f3461a36d76/image{i}_2.jpg"))
        
        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/53f6cc9b-0551-4b7b-a7ca-6755baeb1eeb/image{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/53f6cc9b-0551-4b7b-a7ca-6755baeb1eeb/image{i}_2.jpg"))


        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/80747358-0e05-4310-84ad-7ec4eff62942/image{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/80747358-0e05-4310-84ad-7ec4eff62942/image{i}_2.jpg"))

        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/9ab3c5e8-1e9e-4863-a3b0-cd966c758560/image{i}_1.jpg"))
        # image_two = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/ressources/9ab3c5e8-1e9e-4863-a3b0-cd966c758560/image{i}_2.jpg"))
        
        

        # image_one = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tmp/train/ressources/bundle/05c1d782-71b2-4e21-a857-97af015c2fc4/Train/Images/Image_225_1.jpg"))

        image_one = image_one.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        frame = np.array(image_one)
        frame = hp.Preprocess.convert_to_BGR(frame)

        # image_two = image_two.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
        # frame2 = np.array(image_two)
        # frame2 = hp.Preprocess.convert_to_BGR(frame2)


        # frame = hp.Video.translate_image(frame)


        # frame = frame[0:115, 10:150]

        # frame = hp.Augmentation.black_spots(frame, 10)

        hp.Out.image_show("Original", frame, IN_DEBUG_MODE)
        # hp.Out.image_show("Original2", frame2, IN_DEBUG_MODE)

        frame = hp.Preprocess.start(frame)
        frame = hp.Video.zoom(frame, IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX)
        frame = hp.Preprocess.convert_to_BGR(frame)
        # frame2 = hp.Preprocess.start(frame2)
        # frame2 = hp.Video.zoom(frame2, IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX)
        # frame2 = hp.Preprocess.convert_to_BGR(frame2)


        hp.Out.image_show("Processed", frame, IN_DEBUG_MODE)
        # hp.Out.image_show("Processed2", frame2, IN_DEBUG_MODE)

        
        if IN_DEBUG_MODE:

            if FRAME_STEP_BY_STEP:
                while True:
                    # Press enter to run next frame
                    if cv2.waitKey(1) == 13:
                        break

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        exit_analyse = True
                        break

            if exit_analyse or (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        i = i + 1



if __name__ == "__main__":
    main()

