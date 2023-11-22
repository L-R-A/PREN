import cv2
import numpy as np
import os
import json
import helper as hp

#region CONFIGURATION CONSTANTS

VIDEO_PATH = '../ressources/video_example/video_example.mp4'

IN_DEBUG_MODE = True
FRAME_STEP_BY_STEP = True

ROTATION_SIDES = 4

FRAME_SCALE_PERCENTAGE = 80

CHECKED_FRAMES_PER_SIDE = 10

MIN_CONTOUR_AREA = 1000
MIN_CONTOUR_HEIGHT = 100
MIN_CONTOUR_WIDTH = 100

TOLERANCE_CONTOUR_IS_AROUND_CENTER = 20
TOLERANCE_IS_NEAR_TOP = 50
TOLERANCE_IS_NEAR_BOTTOM = 50

OUTPUT_FILE_NAME = "output.json"
OUTPUT_FILE_DIR = "../tmp"


#endregion

#region PRESTRUCTURED LISTS / DICTIONARIES

result = {
    "time": "",
    "config": {
        "1": "",
        "2": "",
        "3": "",
        "4": "",
        "5": "",
        "6": "",
        "7": "",
        "8": ""
    }
}

result_cache = {
    "1": {
        "color":"",
        "y":0
    },
    "2": {
        "color":"",
        "y":0
    },
    "3": {
        "color":"",
        "y":0
    },
    "4": {
        "color":"",
        "y":0
    },
    "5": {
        "color":"",
        "y":0
    },
    "6": {
        "color":"",
        "y":0
    },
    "7": {
        "color":"",
        "y":0
    },
    "8": {
        "color":"",
        "y":0
    }
}


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

quadrant_enum = {
    "QUADRANT_ONE": 0,
    "QUADRANT_TWO": 1,
    "QUADRANT_THREE": 2,
    "QUADRANT_FOUR": 3
}

sides_enum = {
    "SIDE_ONE": 0,
    "SIDE_TWO": 1,
    "SIDE_THREE": 2,
    "SIDE_FOUR": 3
}

complete = {
    "x": 0,
    "y": 0,
    "width": 0,
    "height": 0
}

center_x = []

#endregion

#region HELPER METHODS

def calcualte_color_at_cordinate(frame, x, y):
    pixel = frame[y, x]

    hsv_color = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]

    merged_colors = hp.HSVRanges.red_color + hp.HSVRanges.yellow_color  + hp.HSVRanges.blue_color

    for color in merged_colors:
        if (color["lower_bounds"][0] <= hsv_color[0] <= color["upper_bounds"][0] and
            color["lower_bounds"][1] <= hsv_color[1] <= color["upper_bounds"][1] and
            color["lower_bounds"][2] <= hsv_color[2] <= color["upper_bounds"][2]):
            return color["color_name"]


def is_approx_modular(value1, value2, tolerance=10):
    if value2 == 0:
        return True

    return 0 <= value1 % value2 <= tolerance

def is_in_range(value1, value2, tolerance=10):
    return abs(value1 - value2) <= tolerance

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

    hp.Out.print_step("STEP 1: CALCULATE SINGLE ROTATION TIME IN FRAMES")

    cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), VIDEO_PATH))

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
            hp.Out.log(f"Finished calculating cycle time: {frame_count} frames", IN_DEBUG_MODE)
            return frame_count


#endregion

#region MASK CREATION

def create_color_mask(hsv, colors):

    mask = []

    for color in colors:
        if len(mask) == 0:
            mask = cv2.inRange(hsv, color["lower_bounds"], color["upper_bounds"])
        else:
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv, color["lower_bounds"], color["upper_bounds"]))

    return mask


def create_contour_mask(frame):

    # Image preprocessing
    grey = hp.Video.grey_mask(frame)
    stretched = hp.Video.contrast_stretching(grey)
    blur = hp.Video.blur_mask(stretched)
    processed = hp.Video.threshold_mask(blur)

    contour_thickness = 20

    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    c = 0
    for i in contours:
            area = cv2.contourArea(i)
            if area > MIN_CONTOUR_AREA:
                if area > max_area:
                    max_area = area
                    best_cnt = i
                    frame = cv2.drawContours(frame, contours, c, (0, 0, 0), contour_thickness)
            c+=1



    mask = np.zeros((grey.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)

    out = np.zeros_like(grey)
    out[mask == 255] = grey[mask == 255]




    # Image preprocessing
    blur = hp.Video.blur_mask(out)
    processed = hp.Video.threshold_mask(blur)
    eroded = hp.Video.eroded_mask(processed, (10,10))

    contours, _ = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    c = 0
    for i in contours:
            cv2.drawContours(frame, contours, c, (0, 0, 0), contour_thickness)
            c+=1

    return frame

#endregion

#region CORDINATE CALCULATION

def calculate_object_cordinates_with_contour(frame):
    contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objects = []

    for contour in contours:

        contour_area = cv2.contourArea(contour)

        if contour_area >= MIN_CONTOUR_AREA:            
            x, y, w, h = cv2.boundingRect(contour)

            if  h > MIN_CONTOUR_HEIGHT and w > MIN_CONTOUR_WIDTH:
                objects.append((x, y, w, h))

    return objects


#region METHODS TO DISQUALIFY CENTER POINTS

def is_near_center_x_position(x, tolerance=20):

    for cX in center_x:
        if is_in_range(x, cX, tolerance):
            return True
    
    return False


def is_lesser_or_near_top(y, tolerance=20):
    if y <= complete["y"]:
        return True

    if is_in_range(y, complete["y"], tolerance):
        return True

    return False

def is_further_or_near_bottom(y, tolerance=20):

    if y > (complete["y"] + complete['height']):
        return True

    if is_in_range(y, complete["y"] +  complete["height"], tolerance):
        return True
    
    return False

#endregion


def calcualte_object_center_cordinates_with_edge_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    edges = cv2.Canny(thresh, threshold1=30, threshold2=100)

    # Apply morphological operations to connect nearby contours
    kernel = np.ones((10, 10), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)


    contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objects = []

    for contour in contours:

        contour_area = cv2.contourArea(contour)

        # ToDo: refactor threshold
        if contour_area >= MIN_CONTOUR_HEIGHT:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
            else:
                x, y = 0, 0

            # Disqualify center points
            if is_near_center_x_position(x, TOLERANCE_CONTOUR_IS_AROUND_CENTER) and not is_lesser_or_near_top(y, TOLERANCE_IS_NEAR_TOP) and not is_further_or_near_bottom(y, TOLERANCE_IS_NEAR_BOTTOM):
                objects.append({"x": x, "y": y})

                if IN_DEBUG_MODE:
                    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                    cv2.putText(frame, f"({x}, {y})", (x - 50, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return objects


#endregion

#region QUADRANT METHODS

def set_quadrants():

    # ToDo: What if there is only one row of cubes or one column of cubes? object widht and height would be wrong!
    # Maybe have to set width and height of complete object static

    # ToDo: Dynamically calculate offset
    Y_OFFSET = 50

    center_x.append(complete["x"] + (complete["width"] / 4))
    center_x.append(complete["x"] + ((complete["width"] / 4) * 3))

    quadrants[quadrant_enum["QUADRANT_ONE"]]["lower_x"] = complete["x"]
    quadrants[quadrant_enum["QUADRANT_ONE"]]["upper_x"] = complete["x"] + (complete["width"] / 2)
    quadrants[quadrant_enum["QUADRANT_ONE"]]["lower_y"] = (complete["y"] + (complete["height"] / 2  )) + Y_OFFSET
    quadrants[quadrant_enum["QUADRANT_ONE"]]["upper_y"] = complete["y"] + complete["height"]

    quadrants[quadrant_enum["QUADRANT_TWO"]]["lower_x"] = complete["x"] + (complete["width"] / 2)
    quadrants[quadrant_enum["QUADRANT_TWO"]]["upper_x"] = complete["x"] + complete["width"]
    quadrants[quadrant_enum["QUADRANT_TWO"]]["lower_y"] = (complete["y"] + (complete["height"] / 2  )) + Y_OFFSET
    quadrants[quadrant_enum["QUADRANT_TWO"]]["upper_y"] = complete["y"] + complete["height"]

    quadrants[quadrant_enum["QUADRANT_THREE"]]["lower_x"] = complete["x"]
    quadrants[quadrant_enum["QUADRANT_THREE"]]["upper_x"] = complete["x"] + (complete["width"] / 2)
    quadrants[quadrant_enum["QUADRANT_THREE"]]["lower_y"] = complete["y"]
    quadrants[quadrant_enum["QUADRANT_THREE"]]["upper_y"] = (complete["y"] + (complete["height"] / 2  )) + Y_OFFSET

    quadrants[quadrant_enum["QUADRANT_FOUR"]]["lower_x"] = complete["x"] + (complete["width"] / 2)
    quadrants[quadrant_enum["QUADRANT_FOUR"]]["upper_x"] = complete["x"] + complete["width"]
    quadrants[quadrant_enum["QUADRANT_FOUR"]]["lower_y"] = complete["y"]
    quadrants[quadrant_enum["QUADRANT_FOUR"]]["upper_y"] = (complete["y"] + (complete["height"] / 2  )) + Y_OFFSET


def calculate_quadrant(x, y):
    if quadrants[quadrant_enum["QUADRANT_ONE"]]["lower_x"] <= x <= quadrants[quadrant_enum["QUADRANT_ONE"]]["upper_x"]:
        if quadrants[quadrant_enum["QUADRANT_ONE"]]["lower_y"] <= y <= quadrants[quadrant_enum["QUADRANT_ONE"]]["upper_y"]:
            return quadrant_enum["QUADRANT_ONE"]
        else:
            return quadrant_enum["QUADRANT_THREE"]
    
    if quadrants[quadrant_enum["QUADRANT_TWO"]]["lower_x"] <= x <= quadrants[quadrant_enum["QUADRANT_TWO"]]["upper_x"]:
        if quadrants[quadrant_enum["QUADRANT_TWO"]]["lower_y"] <= y <= quadrants[quadrant_enum["QUADRANT_TWO"]]["upper_y"]:
            return quadrant_enum["QUADRANT_TWO"]
        else:
            return quadrant_enum["QUADRANT_FOUR"]
        
    return 5

#endregion

#region GENERATE_RESULT

def mapping_2d_to_3d_result(quadrant_one, quadrant_two, quadrant_three, quadrant_four, c_point_quadrant, c_point_color, c_point_y):
    if c_point_quadrant == quadrant_enum["QUADRANT_ONE"]:
        if quadrant_one["y"] < c_point_y:
            quadrant_one["color"] = c_point_color
            quadrant_one["y"] = c_point_y
    elif c_point_quadrant == quadrant_enum["QUADRANT_TWO"]:
        if quadrant_two["y"] < c_point_y:
            quadrant_two["color"] = c_point_color
            quadrant_two["y"] = c_point_y
    elif c_point_quadrant == quadrant_enum["QUADRANT_THREE"]:
        if quadrant_three["y"] < c_point_y:
            quadrant_three["color"] = c_point_color
            quadrant_three["y"] = c_point_y
    elif c_point_quadrant == quadrant_enum["QUADRANT_FOUR"]:
        if quadrant_four["y"] < c_point_y:
            quadrant_four["color"] = c_point_color
            quadrant_four["y"] = c_point_y

def check_if_cube_is_a_runaway(cube, y):
    if not is_in_range(cube["y"], y):
        cube["color"] = ""
        cube["y"] = ""


def analyze_generated_result_and_remove_invalid_cubes(cubes):
    smallest_y = min(cubes["1"]["y"], cubes["2"]["y"], cubes["3"]["y"], cubes["4"]["y"])
    check_if_cube_is_a_runaway(cubes["1"], smallest_y)
    check_if_cube_is_a_runaway(cubes["2"], smallest_y)
    check_if_cube_is_a_runaway(cubes["3"], smallest_y)   
    check_if_cube_is_a_runaway(cubes["4"], smallest_y)

    biggest_y = max(cubes["5"]["y"], cubes["6"]["y"], cubes["7"]["y"], cubes["8"]["y"])
    check_if_cube_is_a_runaway(cubes["5"], biggest_y)
    check_if_cube_is_a_runaway(cubes["6"], biggest_y)
    check_if_cube_is_a_runaway(cubes["7"], biggest_y)
    check_if_cube_is_a_runaway(cubes["8"], biggest_y)

def write_output(cubes):
    try:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_FILE_DIR)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        with open(os.path.join(log_dir, OUTPUT_FILE_NAME), "w") as file:
            file.write(json.dumps(cubes) + '\n')
    except Exception as e:
        hp.Out.log("Writing to log file didn't work!", IN_DEBUG_MODE)
        hp.Out.log(e, IN_DEBUG_MODE)

#endregion

def main():

    rotation_time_in_frames = calculate_rotation_time(hp.HSVRanges.light_grey_color)
    cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), VIDEO_PATH))
    
    frame_count = 0
    side_count = sides_enum["SIDE_ONE"]

    cubes_cordinates =  []

    hp.Out.print_step("STEP 2: CALCULATE 2D CORDINATES OF CUBES USING COLOR, CONTOUR AND EDGE-DETECTION")

    while True:
        exit_analyse = False

        ret, frame = cap.read()
        frame = hp.Video.scale_down_frame(frame, FRAME_SCALE_PERCENTAGE);

        result = frame

        # Exit if plate has cycled ones (going back to start position isn't necessary)
        if frame_count >= rotation_time_in_frames:
            hp.Out.print_step("STEP 3: GENERATE OUTPUT")
            analyze_generated_result_and_remove_invalid_cubes(result_cache)
            hp.Out.log(result_cache, IN_DEBUG_MODE, True)
            write_output(result_cache)
            break

        # ToDo: Dynamically calculate a frame the starting frame    
        if frame_count == 0:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color_mask = create_color_mask(hsv, hp.HSVRanges.red_color + hp.HSVRanges.yellow_color + hp.HSVRanges.blue_color)
            cubes_cordinates = calculate_object_cordinates_with_contour(color_mask)

            complete["x"] = cubes_cordinates[0][0]
            complete["y"] = cubes_cordinates[0][1]
            complete["width"] = cubes_cordinates[0][2]
            complete["height"] = cubes_cordinates[0][3]

            set_quadrants()


        # ToDo: refactor this!!!!
        if is_approx_modular(frame_count, (rotation_time_in_frames / 4)):

            # frame = frame[ cubes_cordinates[0][1]:cubes_cordinates[0][1] + cubes_cordinates[0][3], cubes_cordinates[0][0]:cubes_cordinates[0][0] + cubes_cordinates[0][2]]
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color_mask = create_color_mask(hsv, hp.HSVRanges.red_color + hp.HSVRanges.yellow_color + hp.HSVRanges.blue_color)
            result_color = cv2.bitwise_and(frame, frame, mask=color_mask)
            

            result_contour = create_contour_mask(result_color)
            result = result_contour

            cordinates = calcualte_object_center_cordinates_with_edge_detection(result)

            # Foreach center point inside a  detected rectangle calculate the 2D quadrant, color and map it to a 3D grid
            for c_point in cordinates:

                c_point_quadrant = calculate_quadrant(c_point["x"], c_point["y"])
                c_point_color = calcualte_color_at_cordinate(frame, c_point["x"], c_point["y"])

                if side_count == sides_enum["SIDE_ONE"]:
                    mapping_2d_to_3d_result(result_cache["4"], result_cache["1"], result_cache["8"], result_cache["5"], c_point_quadrant, c_point_color, c_point["y"])
                elif side_count == sides_enum["SIDE_TWO"]:
                    mapping_2d_to_3d_result(result_cache["1"], result_cache["2"], result_cache["5"], result_cache["6"], c_point_quadrant, c_point_color, c_point["y"])
                elif side_count == sides_enum["SIDE_THREE"]:
                    mapping_2d_to_3d_result(result_cache["2"], result_cache["3"], result_cache["6"], result_cache["7"], c_point_quadrant, c_point_color, c_point["y"])           
                elif side_count == sides_enum["SIDE_FOUR"]:
                    mapping_2d_to_3d_result(result_cache["3"], result_cache["4"], result_cache["7"], result_cache["8"], c_point_quadrant, c_point_color, c_point["y"])       
            
            # Go to next side, after the last frame was checked
            if (frame_count % ((rotation_time_in_frames) / ROTATION_SIDES)) - CHECKED_FRAMES_PER_SIDE == 0:
                if side_count == ROTATION_SIDES - 1:
                    side_count = sides_enum["SIDE_ONE"]
                else:
                    side_count = side_count + 1
                
        # Run frame after frame for debugging purposes
        if IN_DEBUG_MODE:

            hp.Out.image_show('Original', frame, IN_DEBUG_MODE)
            hp.Out.image_show('Result', result, IN_DEBUG_MODE)   

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

        frame_count = frame_count + 1


    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()

