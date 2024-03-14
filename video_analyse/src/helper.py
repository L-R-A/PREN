import cv2
import numpy as np
import json

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
            "lower_bounds": np.array([100,  100, 80]),
            "upper_bounds": np.array([180, 255, 255]) 
        },
    ]

    light_grey_color = [
        {
            "color_name": "light grey",
            "lower_bounds": np.array([0, 0, 190]),
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


    def start(frame):
        frame = Preprocess.process_color(frame, HSVRanges.light_grey_color, BGRColors.white_color)
        frame = Preprocess.process_color(frame, HSVRanges.red_color, BGRColors.red_color)
        frame = Preprocess.process_color(frame, HSVRanges.yellow_color, BGRColors.yellow_color)
        frame = Preprocess.process_color(frame, HSVRanges.blue_color, BGRColors.blue_color)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_mask = Mask.create_color_mask(hsv, HSVRanges.red_color + HSVRanges.blue_color + HSVRanges.yellow_color + HSVRanges.light_grey_color)
        frame = cv2.bitwise_or(frame, frame, mask=color_mask)
        return Video.blur_mask(frame)

class Video:
    videoCapture = None

    def __init__(self, path):
        self.videoCapture = cv2.VideoCapture(path)

    def get_next_frame(self):
        return self.videoCapture.read()
    
    def grey_mask(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def blur_mask(frame, size=(5,5)):
        return cv2.GaussianBlur(frame, size, 0)

    def threshold_mask(frame):
        return cv2.adaptiveThreshold(frame, 255, 1, 1, 11, 2)
    
    def contrast_improvement_mask(frame):
        return cv2.equalizeHist(frame)

    def dilate_mask(frame, shape=(5,5)):
        kernel = np.ones(shape, np.uint8)
        eroded = cv2.erode(frame, kernel, iterations=1)
        return cv2.dilate(eroded, kernel, iterations=1)
    
    def eroded_mask(frame, shape=(5,5)):
        kernel = np.ones(shape, np.uint8)
        dilated = cv2.dilate(frame, kernel, iterations=1)
        return cv2.erode(dilated, kernel, iterations=1)
    
    def clahe_correction(frame):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(frame)
    
    def gamma_correction(frame, gamma=1.5):
        frame = np.power(frame / 255.0, gamma) * 255.0
        return np.uint8(frame)
        
    def contrast_stretching(frame, min_intensity=0, max_intensity=255):
        return cv2.normalize(frame, None, min_intensity, max_intensity, cv2.NORM_MINMAX)
    
    def undistort_frame(camera_matrix, distortion_coefficients, frame):
        height, width = frame.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (width,height), 1, (width,height))

        undistorted = cv2.undistort(frame, camera_matrix, distortion_coefficients, None, newcameramtx)

        x, y, w, h = roi
        return undistorted[y:y+h, x:x+w]
    
    def scale_down_frame(frame, percentage):
        width = int((frame.shape[1] * percentage) / 100)
        height = int((frame.shape[0] * percentage) / 100)
        return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

class Terminal_Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Mask: 
    def create_color_mask(hsv, colors):
        mask = []

        for color in colors:
            if len(mask) == 0:
                mask = cv2.inRange(hsv, color["lower_bounds"], color["upper_bounds"])
            else:
                mask = cv2.bitwise_or(mask, cv2.inRange(hsv, color["lower_bounds"], color["upper_bounds"]))

        return mask
    
class Out:
    def image_show(name, frame, debug):
        if debug:
            cv2.imshow(name, frame)

    def log(message, debug, is_json = False):
        if debug:
            if is_json:
                print(json.dumps((message), indent=2))
            else: 
                print(message)

    def print_step(message):
            print(f"{Terminal_Color.BOLD}{message}{Terminal_Color.END}")


class Constants:
    CAMERA_CALIBRATION = {
        "BASELINE": 0.01,  # Distance between the optical centers of the left and right cameras in meters
        "FOCAL_LENGTH": 0.008  # Distance from the camera's image sensor to the lens in meters
    }