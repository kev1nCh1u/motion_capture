from itertools import count
import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import time

import os
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *
from lib.kevin import kevinuart


###################################################################################
# main
###################################################################################
def main():
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

    FundamentalMatrix = fs.getNode("FundamentalMatrix").mat()

    print('\n cameraMatrix1\n', cameraMatrix1)
    print('\n distCoeffs1\n', distCoeffs1)
    print('\n cameraMatrix2\n', cameraMatrix2)
    print('\n distCoeffs2\n', distCoeffs2)
    print('\n imageSize\n', imageSize)
    print('\n RotationOfCamera2\n', RotationOfCamera2)
    print('\n TranslationOfCamera2\n', TranslationOfCamera2)
    print('\n FundamentalMatrix\n', FundamentalMatrix)
    print()

    ########################################### uart
    kuc = kevinuart.UartControl('/dev/ttyUSB0') # right camera
    kuc1 = kevinuart.UartControl('/dev/ttyUSB1') # left camera
    
    # binary thres:50 100
    kuc.ser_write(1, 50) 
    kuc1.ser_write(1, 50)

    #################################### open camera
    # cap = cv2.VideoCapture(4) # left
    # cap2 = cv2.VideoCapture(2) # right

    ########################################### file
    fs = cv2.FileStorage("data/parameter/create_markers.yaml", cv2.FILE_STORAGE_WRITE)

    ######################################### init value
    count = 0

    while 1:
        ########################################## read_uart
        kuc.uart_ser() # right camera
        kuc1.uart_ser() # left camera

        ########################################### get_point 
        point2d_1 = kuc.point2d
        point2d_2 = kuc1.point2d

        ########################################### epipolar
        # for i in range(4):
        #     point_1 = np.array([[point2d_1[i][0],point2d_1[i][1],1]])
        #     point_2 = np.array([[point2d_2[i][0],point2d_2[i][1],1]])
        #     point2d_1[i,1] = epipolar_line(FundamentalMatrix, point_1, 0, point_1[0][0], 0) # epipolar point
        #     point2d_2[i,1] = epipolar_line(FundamentalMatrix, point_2, 0, point_2[0][0], 1) # epipolar point

        ##################################### sorting
        # point2d_1 = np.sort(point2d_1.view('i8,i8'), order=['f1'], axis=0).view(np.int64)
        # point2d_2 = np.sort(point2d_2.view('i8,i8'), order=['f1'], axis=0).view(np.int64)
        
        #################################### print point
        for i in range(4):
            print("p"+str(i), point2d_1[i,0],point2d_1[i,1],point2d_2[i,0],point2d_2[i,1], end=' ')
        print()

        ########################################### check

        ############################################# triangulate
        # print("triangulation_depth ========================================")
        points3d = np.zeros((4, 3), np.float64)
        for i in range(4):
            if(point2d_1[i,0] or point2d_2[i,0]):
                points3d[i] = triangulate(cameraMatrix1, cameraMatrix2, RotationOfCamera2, TranslationOfCamera2, point2d_1[i], point2d_2[i])
            else:
                points3d[i] = [0,0,0]

        #################################### cv draw picture
        output_image = np.full((480,640*2,3), 255, np.uint8) # create image

        for i in range(4):
            if(point2d_1[i][0] and point2d_2[i][0]):
                cv2.line(output_image, tuple(point2d_1[i].astype(int)-(5,0)), tuple(point2d_1[i].astype(int)+(5,0)), (0, 0, 255))
                cv2.line(output_image, tuple(point2d_1[i].astype(int)-(0,5)), tuple(point2d_1[i].astype(int)+(0,5)), (0, 0, 255))
                cv2.line(output_image, tuple(point2d_2[i].astype(int)-(5,0)+(640,0)), tuple(point2d_2[i].astype(int)+(5,0)+(640,0)), (0, 0, 255))
                cv2.line(output_image, tuple(point2d_2[i].astype(int)-(0,5)+(640,0)), tuple(point2d_2[i].astype(int)+(0,5)+(640,0)), (0, 0, 255))

        text = "press c to capture point"
        cv2.putText(output_image, text,
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        text = "Capture point: " + str(count)
        cv2.putText(output_image, text,
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        for i in range(4):
            text = "p" + str(i) + " X: " + str(round(points3d[i, 0], 2)) + " Y: " + str(round(points3d[i, 1], 2)) + " Z: " + str(round(points3d[i, 2], 2))
            cv2.putText(output_image, text,
                        (10, 60+i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Show the frames
        cv2.imshow("output_image", output_image)

        # Hit "q" to close the window
        inputKey = cv2.waitKey(1) & 0xFF

        # if q exit
        if inputKey == ord('q'):
            break

        # if c capture
        elif inputKey == ord('c'):
            orginPoint = points3d
            orginDistance = findAllDis(points3d)
            fs.write('orginDistance'+str(count), orginDistance)
            fs.write('orginPoint'+str(count), orginPoint)
            count += 1

    cv2.destroyAllWindows()
    fs.release()


# if main
if __name__ == '__main__':
    main()