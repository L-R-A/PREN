import cv2

# import matplotlib
# matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt


import numpy as np
import os
import helper as hp

#region CONFIGURATION CONSTANTS

IN_DEBUG_MODE = True
FRAME_STEP_BY_STEP = True
VIDEO_PATH = '../ressources/video_example/01_config.mp4'
CALLIBRATION_VIDEO_PATH = '../ressources/video_example/callibration_video.mp4'

OUTPUT_FILE_DIR = "../tmp"

#endregion

#region VIDEO CALIBRATION

def calcualte_corners_on_chessboard(frame, gray):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    object_point = np.zeros((6*7,3), np.float32)
    object_point[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    ret, chess_corners = cv2.findChessboardCorners(gray, (7,6), None)

    if ret == True:
        image_point = cv2.cornerSubPix(gray, chess_corners, (11,11), (-1,-1), criteria)

        cv2.drawChessboardCorners(frame, (7,6), image_point, ret)

        hp.Out.image_show('Frame', frame, IN_DEBUG_MODE)
        cv2.waitKey(500)

        return object_point, image_point

    

# Necessary to undistort a video (Remove angles created by lenses etc.)
# The camera callibration is different for each camera
# Can be calculated by holding a chessboard in front of the specific camera used
def camera_calibration():
    cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), CALLIBRATION_VIDEO_PATH))
    
    object_points = [] # 3d point in real world space
    image_points = [] # 2d points in image plane.

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        object_point, image_point = calcualte_corners_on_chessboard(gray)

        if object_point and image_point:
            object_points.append(object_point)
            image_points.append(image_point)

        if not ret:
            break

    # Generate camera matrix, distortion coefficients, rotation and translation vectors
    return cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)


#endregion

#region DEPTH MAP

def stereo(frame_left, frame_right):
    stereo = cv2.StereoBM.create(numDisparities=16, blockSize=15)

    grey_left = hp.Video.grey_mask(frame_left)
    grey_right = hp.Video.grey_mask(frame_right)

    disparity = stereo.compute(grey_left, grey_right)
    disparity = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)


    depth_map = hp.Constants.CAMERA_CALIBRATION["BASELINE"] * hp.Constants.CAMERA_CALIBRATION["FOCAL_LENGTH"] / (disparity + 0.0001)  # Avoid division by zero

    if IN_DEBUG_MODE:
        hp.Out.image_show("Frame left", frame_left, IN_DEBUG_MODE)
        hp.Out.image_show("Frame Right", frame_right, IN_DEBUG_MODE)
        hp.Out.image_show("Disparity", disparity, IN_DEBUG_MODE)
        hp.Out.image_show("Depth_map", depth_map, IN_DEBUG_MODE)
        if FRAME_STEP_BY_STEP:
            while True:
                # Press enter to run next frame
                if cv2.waitKey(1) == 13:
                    return depth_map


def generate_depth_map(cap, frame_count):
        # The offset of the two viewpoints necesseray to calculate the stereo image
        # Should be around 1 - 5 degrees
        frame_offset = 10

        # ToDo: check 

        # Read frame in original position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret1, frame_left = cap.read()

        hsv = cv2.cvtColor(frame_left, cv2.COLOR_BGR2HSV)
        color_mask = hp.Mask.create_color_mask(hsv, hp.HSVRanges.red_color + hp.HSVRanges.blue_color + hp.HSVRanges.yellow_color)
        frame_left_masked = cv2.bitwise_and(frame_left, frame_left, mask=color_mask)


        # Read 1-5 degrees turned frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, (frame_count + frame_offset))
        ret2, frame_right = cap.read()

        hsv = cv2.cvtColor(frame_right, cv2.COLOR_BGR2HSV)
        color_mask = hp.Mask.create_color_mask(hsv, hp.HSVRanges.red_color + hp.HSVRanges.blue_color + hp.HSVRanges.yellow_color)
        frame_right_masked = cv2.bitwise_and(frame_right, frame_right, mask=color_mask)

        if not ret1:
            return
        
    

        return stereo(frame_left_masked, frame_right_masked)

#endregion

#region 3D-SCENE-RECONSTRUCTION

def scene_reconstruction(depth_map):

    height, width = depth_map.shape

    x_coords, y_coords, z_coords = [], [], []

    for v in range(height):
        for u in range(width):
            # Calculate the 3D point's x, y, z coordinates
            depth = depth_map[v, u] / 1000.0  # Convert from millimeters to meters
            x = (u - width / 2.0) * depth / hp.Constants.CAMERA_CALIBRATION["FOCAL_LENGTH"]
            y = (v - height / 2.0) * depth / hp.Constants.CAMERA_CALIBRATION["FOCAL_LENGTH"]
            z = depth

            # Add the coordinates to the arrays
            x_coords.append(x)
            y_coords.append(y)
            z_coords.append(z)


    # Create a 3D scatter plot using matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coords, y_coords, z_coords, c='b', marker='o')

    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    if IN_DEBUG_MODE:
        # plt.show()
        plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_FILE_DIR, "scene_reconstruction.png"))


        if FRAME_STEP_BY_STEP:
            while True:
                # Press enter to run next frame
                if cv2.waitKey(1) == 13:
                    return


#endregion

def main():

    # Camera calibration has to be only once for each camera model used
    # It is necessary to undistort the video to make a 3D-Reconstruction
    # ret, camera_matrix, distortion_coefficients  = camera_calibration()

    cap = cv2.VideoCapture(os.path.join(os.path.dirname(os.path.abspath(__file__)), VIDEO_PATH))

    frame_count = 0

    while True:

        #region UNDISTORT FRAME

        # hp.Video.undistort_frame(camera_matrix, distortion_coefficients, frame)

        #endregion

        #region DEPTH MAP

        depth_map = generate_depth_map(cap, frame_count)

        # if not depth_map:
        #     continue

        #endregion


        #region 3D Scene reconstruction

        # scene_reconstruction(depth_map)

        #endregion


        frame_count += 1


if __name__ == "__main__":
    main()
