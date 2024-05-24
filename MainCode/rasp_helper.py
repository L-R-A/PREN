import cv2
import numpy as np
import json
from datetime import datetime

class HSVRanges:
    red_color = [
        {
            "color_name": "red",
            "lower_bounds": np.array([0, 100, 20]),
            "upper_bounds": np.array([10, 255, 255])
        },
        {
            "color_name": "red",
            "lower_bounds": np.array([160, 100, 20]),
            "upper_bounds": np.array([180, 255, 255]) 
        }
    ]

    yellow_color = [
        {
            "color_name": "yellow",
            "lower_bounds": np.array([15, 100, 100]),
            "upper_bounds": np.array([50, 255, 255]) 
        }
    ]

    blue_color = [
        {
            "color_name": "blue",
            "lower_bounds": np.array([100, 70, 50]),
            "upper_bounds": np.array([140, 255, 255])
        },
    ]

    light_grey_color = [
        {
            "color_name": "light grey",
            "lower_bounds": np.array([0, 0, 180]),
            "upper_bounds": np.array([255, 65 , 255])
        }
    ]

class BGRColors: 
    red_color = [0, 0, 255]
    yellow_color = [0, 255, 255]
    blue_color = [255, 0, 0]
    white_color = [255, 255, 255]

class Preprocess:    

    def process_color(frame, hsv_color, end_color):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_mask = Mask.create_color_mask(hsv, hsv_color)
        frame[color_mask != 0] = end_color
        return frame
    
    def darken_frame(frame, factor=0.7):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = hsv[:, :, 2] * factor
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def convert_to_BGR(frame):
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def start(frame):
        frame = Preprocess.darken_frame(frame, 0.95)

        frame = Preprocess.process_color(frame, HSVRanges.light_grey_color, BGRColors.white_color)
        frame = Preprocess.process_color(frame, HSVRanges.red_color, BGRColors.red_color)
        frame = Preprocess.process_color(frame, HSVRanges.yellow_color, BGRColors.yellow_color)
        frame = Preprocess.process_color(frame, HSVRanges.blue_color, BGRColors.blue_color)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_mask = Mask.create_color_mask(hsv, HSVRanges.red_color + HSVRanges.blue_color + HSVRanges.yellow_color + HSVRanges.light_grey_color)
        frame = cv2.bitwise_or(frame, frame, mask=color_mask)
        return Video.blur_mask(frame)

class Video:
    def grey_mask(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def blur_mask(frame, size=(5,5)):
        return cv2.GaussianBlur(frame, size, 0)

    
class Mask: 
    def create_color_mask(hsv, colors):
        mask = []

        for color in colors:
            if len(mask) == 0:
                mask = cv2.inRange(hsv, color["lower_bounds"], color["upper_bounds"])
            else:
                mask = cv2.bitwise_or(mask, cv2.inRange(hsv, color["lower_bounds"], color["upper_bounds"]))

        return mask
    
class JSON:
    def convert_numpy_to_json(array):
        
        data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "config": {str(i+1): value for i, value in enumerate(array)}
        }
        
        # Convert the dictionary to JSON
        return json.dumps(data, indent=4)