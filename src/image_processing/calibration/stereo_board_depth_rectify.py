import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import time
import argparse

###############################################################################################
# find_depth
###############################################################################################


def find_depth(left_point, right_point, baseline, focal):
    x_right = right_point[0]
    x_left = left_point[0]

    # displacement between left and right frames [pixels]
    disparity = abs(x_left - x_right)
    zDepth = (baseline * focal) / disparity            # z depth in [mm]

    return zDepth

###############################################################################################
# calcu_world_point
###############################################################################################


def calcu_world_point(point, z_depth, focal):
    world_points = np.zeros((3), np.float64)
    x_cam = point[0]
    y_cam = point[1]
    world_points[0] = (x_cam * z_depth) / focal
    world_points[1] = (y_cam * z_depth) / focal
    world_points[2] = z_depth
    return world_points

###############################################################################################
# undistortRectify remap
###############################################################################################


def undistortRectify(stereoMapL_x, stereoMapL_y, stereoMapR_x, stereoMapR_y, frameL, frameR):

    # Undistort and rectify images
    undistortedL = cv2.remap(
        frameL, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    undistortedR = cv2.remap(
        frameR, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    return undistortedL, undistortedR


###################################################################################
# main
###################################################################################
def main():
    # kevin args
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--image_id", default='04', help="01~21")
    args = parser.parse_args()

    # load yaml param
    fs = cv2.FileStorage(
        "data/param/matlab_stereo_param.yaml", cv2.FILE_STORAGE_READ)

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
    stereoR = np.transpose(RotationOfCamera2).astype('float64')
    stereoT = np.transpose(TranslationOfCamera2).astype('float64')

    print('\n cameraMatrix1\n', cameraMatrix1)
    print('\n distCoeffs1\n', distCoeffs1)
    print('\n cameraMatrix2\n', cameraMatrix2)
    print('\n distCoeffs2\n', distCoeffs2)
    print('\n imageSize\n', imageSize)
    print('\n stereoR\n', stereoR)
    print('\n stereoT\n', stereoT)
    print()

    ########## Stereo Rectification #################################################
    rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv2.stereoRectify(
        cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, stereoR, stereoT)

    while 1:
        capFlag = 0
        save_path = 'data/result/'

        # Camera parameters to undistort and rectify images
        cv_file = cv2.FileStorage()
        cv_file.open('data/param/stereoMap.xml', cv2.FileStorage_READ)
        stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
        stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
        stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
        stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

        # Stereo vision setup parameters
        fs = cv2.FileStorage(
            "data/param/matlab_stereo_param.yaml", cv2.FILE_STORAGE_READ)
        baseline = abs(fs.getNode("TranslationOfCamera2").mat().ravel()[0])
        focalLength = fs.getNode("FocalLength").mat().ravel()[0]

        # termination criteria for cornerSubPix
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

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

        # triangulation depth
        print("triangulation_depth ========================================")

        # Convert the BGR image to gray
        gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_left, corners_left = cv2.findChessboardCorners(
            gray_left, (9, 6), None)
        ret_right, corners_right = cv2.findChessboardCorners(
            gray_right, (9, 6), None)

        # subpix
        corners_left = cv2.cornerSubPix(
            gray_left, corners_left, (11, 11), (-1, -1), criteria)
        corners_right = cv2.cornerSubPix(
            gray_right, corners_right, (11, 11), (-1, -1), criteria)

        # select point
        conerNum = 0
        center_point_left = corners_left[conerNum].ravel()
        center_point_right = corners_right[conerNum].ravel()
        print("center_point:", center_point_left, center_point_right)
        conerNum = 1
        center_point_left1 = corners_left[conerNum].ravel()
        center_point_right1 = corners_right[conerNum].ravel()
        print("center_point1:", center_point_left1, center_point_right1)

        # tri p1
        tri_k1 = cameraMatrix1
        tri_rt1 = np.array([[1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0]])
        tri_p1 = np.dot(tri_k1, tri_rt1)

        # tri p2
        tri_k2 = cameraMatrix2
        tri_rt2 = np.concatenate((stereoR, stereoT), axis=1)
        tri_p2 = np.dot(tri_k2, tri_rt2)

        # point0
        u1 = center_point_left[0]
        v1 = center_point_left[1]
        u2 = center_point_right[0]
        v2 = center_point_right[1]
        print("uv:", u1, v1, u2, v2)

        A = np.array([u1*tri_p1[2]-tri_p1[0],
                      v1*tri_p1[2]-tri_p1[1],
                      u2*tri_p2[2]-tri_p2[0],
                      v2*tri_p2[2]-tri_p2[1]], dtype='float64')

        U, sigma, VT = np.linalg.svd(A)
        V = VT.transpose()
        X = V[:, -1]
        X = X / X[3]
        print("world_point:", X)
        world_points = np.zeros((2, 3), np.float64)
        world_points[0] = X[0:3]

        # point1
        u1_1 = center_point_left1[0]
        v1_1 = center_point_left1[1]
        u2_1 = center_point_right1[0]
        v2_1 = center_point_right1[1]
        print("uv1", u1_1, v1_1, u2_1, v2_1)

        A = np.array([u1_1*tri_p1[2]-tri_p1[0],
                      v1_1*tri_p1[2]-tri_p1[1],
                      u2_1*tri_p2[2]-tri_p2[0],
                      v2_1*tri_p2[2]-tri_p2[1]], dtype='float64')

        U, sigma, VT = np.linalg.svd(A)
        V = VT.transpose()
        X = V[:, -1]
        X = X / X[3]
        print("world_point1:", X)
        world_points[1] = X[0:3]

        # find distance
        print("world_points:", world_points)
        distance = ((world_points[0, 0] - world_points[1, 0])**2 + (world_points[0, 1] -
                    world_points[1, 1])**2 + (world_points[0, 2] - world_points[1, 2])**2)**0.5
        print("distance:", distance)

        print()

        # point depth
        print("calibration point ========================================")

        # Convert the BGR image to gray
        gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_left, corners_left = cv2.findChessboardCorners(
            gray_left, (9, 6), None)
        ret_right, corners_right = cv2.findChessboardCorners(
            gray_right, (9, 6), None)

        # subpix
        corners_left = cv2.cornerSubPix(
            gray_left, corners_left, (11, 11), (-1, -1), criteria)
        corners_right = cv2.cornerSubPix(
            gray_right, corners_right, (11, 11), (-1, -1), criteria)

        # select point
        conerNum = 0
        center_point_left = corners_left[conerNum].ravel().round()
        center_point_right = corners_right[conerNum].ravel().round()
        print("center_point", center_point_left, center_point_right)

        # stero map
        print("stereoMapL_x shape:", stereoMapL_x.shape)
        test_center_point_left = np.zeros(2)
        stero_map_x = stereoMapL_x[int(
            center_point_left[1]), int(center_point_left[0])]
        stero_map_y = stereoMapL_y[int(
            center_point_left[1]), int(center_point_left[0])]
        print("stero_map:", stero_map_x, stero_map_y)
        test_center_point_left[0] = stero_map_x
        test_center_point_left[1] = stero_map_y
        print("test_center_point_left:", test_center_point_left)

        test_center_point_right = np.zeros(2)
        stero_map_x = stereoMapR_x[int(
            center_point_right[1]), int(center_point_right[0])]
        stero_map_y = stereoMapR_y[int(
            center_point_right[1]), int(center_point_right[0])]
        print("stero_map:", stero_map_x, stero_map_y)
        test_center_point_right[0] = stero_map_x
        test_center_point_right[1] = stero_map_y
        print("test_center_point_right:", test_center_point_right)

        # depth
        test_depth = find_depth(test_center_point_left,
                                test_center_point_right, baseline, focalLength)
        print("test_depth", test_depth)

        # draw
        cv2.circle(frame_left, center_point_left.astype(
            np.int32), 10, (0, 0, 255), -1)

        # draw
        frame_left = cv2.remap(
            frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        cv2.circle(frame_left, test_center_point_left.astype(
            np.int32), 10, (0, 0, 255), -1)
        print()

        ###########################
        # draw green line
        imageSize = (np.shape(stereoMapL_x)[1], np.shape(stereoMapL_x)[0])
        gap = 27
        for i in range(1, int(imageSize[1] / gap) + 1):
            y = gap * i
            cv2.line(frame_left, (0, y), (imageSize[0], y), (0, 255, 0), 1)
            cv2.line(frame_right, (0, y), (imageSize[0], y), (0, 255, 0), 1)

        # mix to show on one picture
        vis = np.concatenate((frame_left, frame_right), axis=1)

        # Show the frames
        cv2.imshow("frame left", frame_left)
        cv2.imshow("frame right", frame_right)
        cv2.imshow("vis SubPix" + fname, vis)

        # Hit "q" to close the window
        inputKey = cv2.waitKey(0) & 0xFF

        # 若按下 q 鍵則離開迴圈
        if inputKey == ord('q'):
            break

        # if s save image
        elif inputKey == ord('s'):
            current_time = time.time()  # catch time
            filename = save_path + 'chess_vis_' + str(current_time) + '.jpg'
            cv2.imwrite(filename, vis)
            print('\nSave:', filename, '\n')

    # Release and destroy all windows before termination
    cap_right.release()
    cap_left.release()

    cv2.destroyAllWindows()


# if main
if __name__ == '__main__':
    main()
