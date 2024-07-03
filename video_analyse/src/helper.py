import cv2
import numpy as np
import json
import random

class HSVRanges:
    red_color = [
        {
            "color_name": "red",
            "lower_bounds": np.array([0, 100, 20]),
            "upper_bounds": np.array([10, 255, 255])
        },
        {
            "color_name": "red",
            "lower_bounds": np.array([160, 50, 20]),
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
            "lower_bounds": np.array([100, 80, 50]),
            "upper_bounds": np.array([140, 255, 255])
        },
    ]

    light_grey_color = [
        {
            "color_name": "light grey",
            "lower_bounds": np.array([0, 0, 185]),
            "upper_bounds": np.array([255, 40, 255])

            # "lower_bounds": np.array([0, 0, 180]), #IF SUN IS NOT THERE THIS WORKS VERY GOOD
            # "upper_bounds": np.array([255, 65 , 255])
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
    
    def lighten_frame(frame, factor=50):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:,:,2] += factor
        hsv[:,:,2] = np.clip(hsv[:,:,2], 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def remove_isolated_white_pixels(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mask = np.ones_like(image, dtype=np.uint8) * 255

        for contour in contours:
            # Minimal white area (pixles) to be not ignored
            if cv2.contourArea(contour) > (500 / 64): 
                cv2.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            else:
                cv2.drawContours(mask, [contour], -1, (0, 0, 0), thickness=cv2.FILLED)

        return cv2.bitwise_and(image, mask)
    

    def remove_isolated_blue_pixels(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mask = np.ones_like(image, dtype=np.uint8) * 255

        for contour in contours:
            # Minimal white area (pixles) to be not ignored
            if cv2.contourArea(contour) > 10: 
                cv2.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            else:
                cv2.drawContours(mask, [contour], -1, (0, 0, 0), thickness=cv2.FILLED)

        return cv2.bitwise_and(image, mask)
    
    def remove_isolated_blue_pixels(image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, HSVRanges.blue_color[0]["lower_bounds"], HSVRanges.blue_color[0]["upper_bounds"])

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        result_mask = np.ones_like(image, dtype=np.uint8) * 255

        for contour in contours:
            # Minimal blue area (pixels) to be not ignored
            if cv2.contourArea(contour) > 200: 
                cv2.drawContours(result_mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            else:
                cv2.drawContours(result_mask, [contour], -1, (0, 0, 0), thickness=cv2.FILLED)

        return cv2.bitwise_and(image, result_mask)
    
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
        frame =  cv2.bitwise_or(frame, frame, mask=color_mask)
        # frame = Preprocess.remove_isolated_white_pixels(frame)
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
    
    def translate_image(frame):
        translation_range = (-1, 1)

        # tx = np.random.randint(translation_range[0], translation_range[1])
        # ty = np.random.randint(translation_range[0], translation_range[1])

        values = [-1, -0.5, 0, 0.5, 1]
        ty = random.choice(values)

    
        M = np.float32([[1, 0, 0],
            [0, 1, ty]])

        return cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
    
    def translate_y(frame, y = 2):
        M = np.float32([[1, 0, 0], [0, 1, y]])
        return cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
    
    def translate_x(frame, x = 1):
        M = np.float32([[1, 0, x], [0, 1, 0]])
        return cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
    

    def zoom(frame, target_height, target_width):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply a threshold to binarize the image
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out small contours based on area
        min_area = 50  # Adjust this value based on the size of small regions to ignore
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= min_area]

        # Create an empty mask to draw the filtered contours
        mask = np.zeros_like(gray)

        # Draw the filtered contours on the mask
        cv2.drawContours(mask, filtered_contours, -1, 255, thickness=cv2.FILLED)

        # Find the bounding box of the non-black regions
        coords = cv2.findNonZero(mask)
        x, y, w, h = cv2.boundingRect(coords)

        # Calculate the aspect ratio of the original bounding box
        aspect_ratio = w / h

        # Target dimensions
        target_aspect_ratio = target_width / target_height

        # Adjust the bounding box to maintain the target aspect ratio
        if aspect_ratio > target_aspect_ratio:
            new_height = int(w / target_aspect_ratio)
            new_y = max(y - (new_height - h) // 2, 0)
            if new_y + new_height > frame.shape[0]:
                new_y = frame.shape[0] - new_height
            cropped = frame[new_y:new_y+new_height, x:x+w]
        else:
            new_width = int(h * target_aspect_ratio)
            new_x = max(x - (new_width - w) // 2, 0)
            if new_x + new_width > frame.shape[1]:
                new_x = frame.shape[1] - new_width
            cropped = frame[y:y+h, new_x:new_x+new_width]

        # Resize the cropped image to 160x120
        resized = cv2.resize(cropped, (target_width, target_height), interpolation=cv2.INTER_LINEAR)

        # Convert the resized image to RGB for displaying
        return cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)


class Augmentation:
    def black_spots(image, num_spots=5, spot_size_range=(20, 40)):
        image_copy = image.copy()

        for _ in range(num_spots):
            # Generate random spot properties
            spot_size = np.random.randint(spot_size_range[0], spot_size_range[1]) // 2  # Integer division for diameter
            spot_center_x = np.random.randint(0 + spot_size, image.shape[1] - spot_size)
            spot_center_y = np.random.randint(0 + spot_size, image.shape[0] - spot_size)

            # Create elliptical mask for the spot
            mask = np.zeros_like(image[:, :, 0], dtype=np.uint8)  # Create mask with same shape as first channel
            cv2.ellipse(mask, (spot_center_x, spot_center_y), (spot_size, spot_size), 0, 0, 360, color=255, thickness=-1)

            # Apply mask to selectively set pixels to black
            image_copy[mask == 255] = [0, 0, 0]  # Set to black in BGR format

        return image_copy

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