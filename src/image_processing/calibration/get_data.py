from itertools import count
import sys
import cv2
from cv2 import split
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import time
import argparse

import os
import importlib
sys.path.append(os.getcwd())
from include.kevin.kevincv import  *
from include.kevin import kevinuart


###################################################################################
# main
###################################################################################
def main():
    ########################################## load yaml param
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

    ########################################### uart
    kuc = kevinuart.UartControl('/dev/ttyUSB1') # right camera
    kuc1 = kevinuart.UartControl('/dev/ttyUSB0') # left camera

    ########################################### file
    data_path = "data/result/point_data.csv" # file path
    data_file = open(data_path, "w") # open file
    count = 0

    while 1:
        ########################################## read_uart
        kuc.uart_ser() # right camera
        kuc1.uart_ser() # left camera

        ########################################### get_point 
        for i in range(4):
            print("p"+str(i), kuc.point2d[i,0],kuc.point2d[i,1],kuc1.point2d[i,0],kuc1.point2d[i,1], end='\t')
        print()

        ############################################# triangulate
        # print("triangulation_depth ========================================")
        points3d = np.zeros((4, 3), np.float64)
        for i in range(4):
            if(kuc.point2d[i,0] or kuc1.point2d[i,0]):
                points3d[i] = triangulate(cameraMatrix1, cameraMatrix2, RotationOfCamera2, TranslationOfCamera2, kuc.point2d[i], kuc1.point2d[i])
            else:
                points3d[i] = [0,0,0]
        #################################### cv draw picture
        blank_image = np.zeros((480,640,3), np.uint8) # create image

        # draw text

        text = "press s to save point"
        cv2.putText(blank_image, text,
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        text = "Save point: " + str(count)
        cv2.putText(blank_image, text,
                    (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        for i in range(4):
            text = "p" + str(i) + " X: " + str(round(points3d[i, 0], 2)) + " Y: " + str(round(points3d[i, 1], 2)) + " Z: " + str(round(points3d[i, 2], 2))
            cv2.putText(blank_image, text,
                        (10, 140+i*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show the frames
        cv2.imshow("blank_image", blank_image)

        # Hit "q" to close the window
        inputKey = cv2.waitKey(1) & 0xFF

        # if q exit
        if inputKey == ord('q'):
            break

        # if s save
        elif inputKey == ord('s'):
            text = ""
            for i in range(4):
                text += str(points3d[i, 0]) + ', ' + str(points3d[i, 1]) + ', ' + str(points3d[i, 2]) + ', '
            text += '\n'
            data_file.write(text) # write data
            print('\nSave...', '\n')
            count += 1

    cv2.destroyAllWindows()
    data_file.close()


# if main
if __name__ == '__main__':
    main()
