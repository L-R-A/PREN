import cv2
import numpy as np
import os

video_path = '../ressources/video_example/video_example.mp4'

red_range = {
    "lower_bounds": np.array([160, 100, 20]),
    "upper_bounds": np.array([180, 255, 255]) 
}

yellow_range = {
    "lower_bounds": np.array([20, 100, 100]),
    "upper_bounds": np.array([40, 255, 255]) 
}

blue_range = {
    "lower_bounds": np.array([90, 100, 100]),
    "upper_bounds": np.array([130, 255, 255]) 
}

light_grey_range = {
    "lower_bounds": np.array([0, 0, 180]),
    "upper_bounds": np.array([180, 40, 255])

}

color_ranges = [red_range, yellow_range, blue_range, light_grey_range]

def seperate_color_masks():

    for color_range in color_ranges: 

        cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), video_path))

        while True:
            ret, frame = cap.read()

            # Check if the video is finished
            if not ret:
               break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Put on mask over frame
            mask = cv2.inRange(hsv, color_range["lower_bounds"], color_range["upper_bounds"])
            
            result = cv2.bitwise_and(frame, frame, mask=mask)

            analyse_contours(mask, frame)

            # Display original and the edited frame
            cv2.imshow('Original', frame)
            cv2.imshow('Result', result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cv2.destroyAllWindows()
        cap.release()


def analyse_contours(mask, frame):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        print(f"Object Detected at (x, y): ({x}, {y}), Width: {w}, Height: {h}")



def combined_color_masks():
    cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), video_path))
        
    while True:
        ret, frame = cap.read()

        # Check if the video is finished
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Put on mask over frame
        red_mask = cv2.inRange(hsv, red_range["lower_bounds"], red_range["upper_bounds"])
        yellow_mask = cv2.inRange(hsv, yellow_range["lower_bounds"], yellow_range["upper_bounds"])
        blue_mask = cv2.inRange(hsv, blue_range["lower_bounds"], blue_range["upper_bounds"])        
        light_grey_mask = cv2.inRange(hsv, light_grey_range["lower_bounds"], light_grey_range["upper_bounds"])

        combined_mask = cv2.bitwise_or(red_mask, cv2.bitwise_or(blue_mask, cv2.bitwise_or(yellow_mask, light_grey_mask)))
            
        result = cv2.bitwise_and(frame, frame, mask=combined_mask)

        # Display original and the edited frame
        cv2.imshow('Original', frame)
        cv2.imshow('Result', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            breaka


    cv2.destroyAllWindows()
    cap.release()


seperate_color_masks()
# combined_color_masks()


