import cv2
import numpy as np
import os

video_path = '../ressources/video_example/video_example.mp4'

#region PREDEFINED COLOR BOUNDS

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
        "lower_bounds": np.array([20, 100, 100]),
        "upper_bounds": np.array([40, 255, 255]) 
    }
]

blue_color = [
    {
        "color_name": "blue",
        "lower_bounds": np.array([90, 100, 100]),
        "upper_bounds": np.array([130, 255, 255]) 
    }
]

light_grey_color = [
    {
        "color_name": "light grey",
        "lower_bounds": np.array([0, 0, 180]),
        "upper_bounds": np.array([180, 40, 255])
    }
]

#endregion

#region METHODS TO CALCULATE SINGLE ROTATION TIME

def calculate_rectangle_simularity(rect1, rect2, tolerance=0.1):
    # Extract rectangle properties
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    
    # Calculate the aspect ratios
    aspect_ratio1 = w1 / h1
    aspect_ratio2 = w2 / h2
    
    # Check if the rectangles have similar positions, sizes, and aspect ratios
    position_similarity = abs(x1 - x2) < tolerance * max(w1, w2) and abs(y1 - y2) < tolerance * max(h1, h2)
    size_similarity = abs(w1 - w2) < tolerance * max(w1, w2) and abs(h1 - h2) < tolerance * max(h1, h2)
    aspect_ratio_similarity = abs(aspect_ratio1 - aspect_ratio2) < tolerance
    
    return position_similarity and size_similarity and aspect_ratio_similarity


def calculate_rotation_time(color):

    print("Calculate cycle time in frames...")

    cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), video_path))

    frame_count = 0
    
    position_marker_first_frame = (0, 0, 0, 0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = create_color_mask(hsv, color)
            
        objects = calculate_object_cordinates_with_contour(mask)

        frame_count = frame_count + 1
            
        # Fix this part to be more generic
        if (len(objects) == 0):
            continue

        if (frame_count == 1):
            position_marker_first_frame = objects[0]
            continue

        # Calculate frame amount until simular starting patterns reoccur
        # Ignore the first few frames
        if (frame_count > 20 and calculate_rectangle_simularity(position_marker_first_frame, objects[0])):
            print(f"Finished calculating cycle time: {frame_count} frames")
            return frame_count


#endregion



def create_color_mask(hsv, colors):

    mask = []

    for color in colors:
        if len(mask) == 0:
            mask = cv2.inRange(hsv, color["lower_bounds"], color["upper_bounds"])
        else:
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv, color["lower_bounds"], color["upper_bounds"]))

    return mask


def calculate_object_cordinates_with_contour(frame):

    minimal_object_height = 100
    minimal_object_width = 100

    contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objects = []

    for contour in contours:

        contour_area = cv2.contourArea(contour)

        if contour_area >= 1000:            
            x, y, w, h = cv2.boundingRect(contour)

            # Ignore objects that are smaller than a specific height
            if  h > minimal_object_height and w > minimal_object_width:
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                objects.append((x, y, w, h))

    return objects


def calcualte_object_center_cordinates_with_edge_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    edges = cv2.Canny(thresh, threshold1=30, threshold2=100)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objects = []

    for contour in contours:

        contour_area = cv2.contourArea(contour)

        # ToDo: refactor threshold
        if contour_area >= 1000:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
            else:
                x, y = 0, 0

            # Only necesseray for display (debug)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Red dot
            cv2.putText(frame, f"({x}, {y})", (x - 50, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            objects.append((x, y))
        
    return objects


def calculate_object_cordinates_with_blob_detection(mask, frame):
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Use blob detection on the mask to identify objects
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(mask)

    object_coordinates = []

    # Loop through the detected keypoints (blobs)
    for keypoint in keypoints:
        x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
        w = int(keypoint.size)
        h =int(keypoint.size)
        print(x, y, w, h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        object_coordinates.append((x, y, w, h))



    return object_coordinates


def create_contour_mask(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    c = 0
    for i in contours:
            area = cv2.contourArea(i)
            if area > 1000:
                if area > max_area:
                    max_area = area
                    best_cnt = i
                    frame = cv2.drawContours(frame, contours, c, (0, 0, 0), 4)
            c+=1



    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)

    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]



    blur = cv2.GaussianBlur(out, (5,5), 0)
    # thresh = cv2.adaptiveThreshold(blur,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    # Apply morphological operations to connect nearby contours
    kernel = np.ones((10, 10), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    contours, _ = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    c = 0
    for i in contours:
            area = cv2.contourArea(i)
            cv2.drawContours(frame, contours, c, (0, 0, 0), 4 )
            c+=1


quadrants = [
    {
        "lower_x": 0,
        "upper_x": 0,
        "lower_y": 0,
        "upper_y": 0
    },
    {
        "lower_x": 0,
        "upper_x": 0,
        "lower_y": 0,
        "upper_y": 0
    },
    {
        "lower_x": 0,
        "upper_x": 0,
        "lower_y": 0,
        "upper_y": 0
    },
    {
        "lower_x": 0,
        "upper_x": 0,
        "lower_y": 0,
        "upper_y": 0
    }
]

def set_quadrants(x, y, width, height):

    # ToDo: Dynamically calculate offset
    Y_OFFSET = 100

    quadrants[0]["lower_x"] = x
    quadrants[0]["upper_x"] = x + (width / 2)
    quadrants[0]["lower_y"] = (y + (height / 2  )) + Y_OFFSET
    quadrants[0]["upper_y"] = y + height

    quadrants[1]["lower_x"] = x + (width / 2)
    quadrants[1]["upper_x"] = x + width
    quadrants[1]["lower_y"] = (y + (height / 2  )) + Y_OFFSET
    quadrants[1]["upper_y"] = y + height

    quadrants[2]["lower_x"] = x
    quadrants[2]["upper_x"] = x + (width / 2)
    quadrants[2]["lower_y"] = y
    quadrants[2]["lower_y"] = (y + (height / 2  )) + Y_OFFSET

    quadrants[3]["lower_x"] = x + (width / 2)
    quadrants[3]["upper_x"] = x + width
    quadrants[3]["lower_y"] = y
    quadrants[3]["upper_y"] = (y + (height / 2  )) + Y_OFFSET


def calculate_quadrant(x, y):
    if quadrants[0]["lower_x"] <= x <= quadrants[0]["upper_x"]:
        if quadrants[0]["lower_y"] <= y <= quadrants[0]["upper_y"]:
            return 1
        else:
            return 3
    
    if quadrants[1]["lower_x"] <= x <= quadrants[1]["upper_x"]:
        if quadrants[1]["lower_y"] <= y <= quadrants[1]["upper_y"]:
            return 2
        else:
            return 4
        
    return 5

def calcualte_color_at_cordinate(frame, x, y):
    pixel = frame[y, x]

    hsv_color = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]

    merged_colors = red_color + yellow_color + blue_color

    for color in merged_colors:
        print(hsv_color)
        if (color["lower_bounds"][0] <= hsv_color[0] <= color["upper_bounds"][0] and
            color["lower_bounds"][1] <= hsv_color[1] <= color["upper_bounds"][1] and
            color["lower_bounds"][2] <= hsv_color[2] <= color["upper_bounds"][2]):
            return color["color_name"]


def is_approx_modular(value1, value2, tolerance=10):

    if value2 == 0:
        return True
    
    print(value1 % value2)

    return 0 <= value1 % value2 <= tolerance

def main():
    rotation_time_in_frames = calculate_rotation_time(light_grey_color)

    cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), video_path))

    frame_count = 0

    debug = True

    while True:

        exit_analyse = False

        ret, frame = cap.read()


        # Exit if plate has cycled ones
        if frame_count >= rotation_time_in_frames:
            break


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #cropped_frame = frame[ cordinates_complete[0][1]:cordinates_complete[0][1] + cordinates_complete[0][3], cordinates_complete[0][0]:cordinates_complete[0][0] + cordinates_complete[0][2]]
        # hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

        mask_complete = create_color_mask(hsv, red_color + yellow_color + blue_color)
        # mask_red = create_color_mask(hsv, red_color)
        # mask_yellow = create_color_mask(hsv, yellow_color)
        # mask_blue = create_color_mask(hsv, blue_color)

        # print(cv2.countNonZero(mask_complete))
        # print(cv2.countNonZero(mask_red))
        # print(cv2.countNonZero(mask_yellow))
        # print(cv2.countNonZero(mask_blue))

        result_complete = cv2.bitwise_and(frame, frame, mask=mask_complete)
        # result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
        # result_yellow = cv2.bitwise_and(frame, frame, mask=mask_yellow)
        # result_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)

        # ToDo: Dynamically calculate a frame the starting frame    
        if frame_count == 0:
            cordinates_complete = calculate_object_cordinates_with_contour(mask_complete)
            set_quadrants(cordinates_complete[0][0], cordinates_complete[0][1], cordinates_complete[0][2], cordinates_complete[0][3])

        # cordinates_red = calculate_object_cordinates_with_blob_detection(mask_red, result_red)
        # cordinates_yellow = calculate_object_cordinates_with_blob_detection(mask_yellow, result_yellow)
        # cordinates_blue = calculate_object_cordinates_with_blob_detection(mask_blue, result_blue)

        create_contour_mask(result_complete)
        # create_contour_mask(result_red)
        # create_contour_mask(result_yellow)
        # create_contour_mask(result_blue)

        # cordinates_red = calculate_object_cordinates_with_contour(result_red)
        # cordinates_yellow = calculate_object_cordinates_with_contour(result_yellow)
        # cordinates_blue = calculate_object_cordinates_with_contour(result_blue)

        # ToDo: refactor this!!!!
        if is_approx_modular(frame_count, (rotation_time_in_frames / 4) - 5):
            cordinates = calcualte_object_center_cordinates_with_edge_detection(result_complete)
            
            for c in cordinates:
                print("CUBE - ", "QUADRANT: ", calculate_quadrant(c[0], c[1]), "COLOR: ", calcualte_color_at_cordinate(frame, c[0], c[1]))

            

            
 
            


        cv2.imshow('Original', frame)
        cv2.imshow('All cubes', result_complete)
        # cv2.imshow('Red cubes', result_red)
        # cv2.imshow('Yellow cubes', result_yellow)
        # cv2.imshow('Blue cubes', result_blue)

        # Run frame after frame for debugging purposes
        if debug:
            while True:
                # Press enter to run next frame
                if cv2.waitKey(1) == 13:
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    exit_analyse = True
                    break

        if exit_analyse or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

        frame_count = frame_count + 1


    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()

