import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import time
import argparse

import os
import importlib
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *


###################################################################################
# main
###################################################################################
def main():
    ######################################## kevin args
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--image_id", default='14', help="01~21")
    args = parser.parse_args()

    ########################################## load yaml param
    fs = cv2.FileStorage(
        "data/parameter/matlab_stereo_param.yaml", cv2.FILE_STORAGE_READ)

    IntrinsicMatrix1 = fs.getNode("IntrinsicMatrix1").mat()
    RadialDistortion1 = fs.getNode("RadialDistortion1").mat()
    TangentialDistortion1 = fs.getNode("TangentialDistortion1").mat()

    IntrinsicMatrix2 = fs.getNode("IntrinsicMatrix2").mat()
    RadialDistortion2 = fs.getNode("RadialDistortion2").mat()
    TangentialDistortion2 = fs.getNode("TangentialDistortion2").mat()

    ImageSize = fs.getNode("ImageSize").mat()
    RotationOfCamera2 = fs.getNode("RotationOfCamera2").mat()
    TranslationOfCamera2 = fs.getNode("TranslationOfCamera2").mat()

    cameraMatrix1 = np.transpose(IntrinsicMatrix1).astype('float64')
    distCoeffs1 = np.concatenate(
        (RadialDistortion1, TangentialDistortion1), axis=1).astype('float64')
    cameraMatrix2 = np.transpose(IntrinsicMatrix2).astype('float64')
    distCoeffs2 = np.concatenate(
        (RadialDistortion2, TangentialDistortion2), axis=1).astype('float64')
    imageSize = ImageSize.ravel()[::-1].astype('int64')
    RotationOfCamera2 = np.transpose(RotationOfCamera2).astype('float64')
    TranslationOfCamera2 = np.transpose(TranslationOfCamera2).astype('float64')

    print('\n cameraMatrix1\n', cameraMatrix1)
    print('\n distCoeffs1\n', distCoeffs1)
    print('\n cameraMatrix2\n', cameraMatrix2)
    print('\n distCoeffs2\n', distCoeffs2)
    print('\n imageSize\n', imageSize)
    print('\n RotationOfCamera2\n', RotationOfCamera2)
    print('\n TranslationOfCamera2\n', TranslationOfCamera2)
    print()

    while 1:
        ########################################## get frame
        capFlag = 0
        save_path = 'data/result/chessboard/'

        # Open both cameras
        if capFlag:
            cap_left = cv2.VideoCapture(4)
            cap_right = cv2.VideoCapture(0)
            # cap_left =  cv2.VideoCapture(2, cv2.CAP_DSHOW)
            # cap_right = cv2.VideoCapture(4, cv2.CAP_DSHOW)
            succes_right, frame_right = cap_right.read()
            succes_left, frame_left = cap_left.read()
            if not succes_right or not succes_left:
                break
            else:
                print('Cap read success...')

        # open both picture
        if not capFlag:
            path = "data/stereo_calibration/new/"
            fname = args.image_id + ".jpg"
            frame_left = cv2.imread(path + '1/' + fname)
            frame_right = cv2.imread(path + '2/' + fname)
        # cv2.imshow('frame_left',frame_left)
        # cv2.imshow('frame_right',frame_right)
        # cv2.waitKey(0)

        ########################################## find point
        # Convert the BGR image to gray
        gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_left, corners_left = cv2.findChessboardCorners(
            gray_left, (11, 8), None)
        ret_right, corners_right = cv2.findChessboardCorners(
            gray_right, (11, 8), None)

        # subpix
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) # termination criteria for cornerSubPix
        corners_left = cv2.cornerSubPix(
            gray_left, corners_left, (8, 8), (-1, -1), criteria)
        corners_right = cv2.cornerSubPix(
            gray_right, corners_right, (8, 8), (-1, -1), criteria)

        # select point
        conerNum = 0
        center_point_left = corners_left[conerNum].ravel()
        center_point_right = corners_right[conerNum].ravel()
        print("center_point:", center_point_left, center_point_right)
        conerNum = 1
        center_point_left1 = corners_left[conerNum].ravel()
        center_point_right1 = corners_right[conerNum].ravel()
        print("center_point1:", center_point_left1, center_point_right1)



        ############################################# triangulate
        print("triangulation_depth ========================================")
        world_points = np.zeros((2, 3), np.float64)
        world_points[0] = triangulate(cameraMatrix1, cameraMatrix2, RotationOfCamera2, TranslationOfCamera2, center_point_left, center_point_right)
        world_points[1] = triangulate(cameraMatrix1, cameraMatrix2, RotationOfCamera2, TranslationOfCamera2, center_point_left1, center_point_right1)

        # find distance
        print("world_points:", world_points)
        distance = euclideanDistances3d(world_points[0], world_points[1])
        print("distance:", distance)
        print()

        #################################### cv draw picture
        # draw point
        cv2.circle(frame_left, center_point_left.astype(
                np.int32), 5, (0, 0, 255), -1)
        cv2.circle(frame_left, center_point_left1.astype(
                np.int32), 5, (255, 0, 0), -1)
        cv2.circle(frame_right, center_point_right.astype(
                np.int32), 5, (0, 0, 255), -1)
        cv2.circle(frame_right, center_point_right1.astype(
                np.int32), 5, (255, 0, 0), -1)

        # draw text
        text = "X: " + str(round(world_points[0, 0], 2))
        cv2.putText(frame_left, text,
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        text = "Y: " + str(round(world_points[0, 1], 2))
        cv2.putText(frame_left, text,
                    (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        text = "Depth: " + str(round(world_points[0, 2], 2))
        cv2.putText(frame_left, text,
                    (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        text = "Distance: " + str(round(distance, 2))
        cv2.putText(frame_left, text,
                    (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # mix to show on one picture
        vis = np.concatenate((frame_left, frame_right), axis=1)

        # Show the frames
        # cv2.imshow("frame left", frame_left)
        # cv2.imshow("frame right", frame_right)
        cv2.imshow("vis SubPix" + fname, vis)

        # Hit "q" to close the window
        inputKey = cv2.waitKey(0) & 0xFF

        # if q exit
        if inputKey == ord('q'):
            break

        # if s save image
        elif inputKey == ord('s'):
            current_time = time.time()  # catch time
            filename = save_path + 'chess_vis_tri_' + str(current_time) + '.jpg' # file path and name
            cv2.imwrite(filename, vis) # save image
            print('\nSave:', filename, '\n')

    # Release and destroy all windows before termination
    cap_right.release()
    cap_left.release()

    cv2.destroyAllWindows()


# if main
if __name__ == '__main__':
    main()
