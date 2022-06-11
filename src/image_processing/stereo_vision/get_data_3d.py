from itertools import count
import sys
import cv2
from cv2 import split
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import time
import pandas as pd

import os
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *
from lib.kevin import kevinuart

###################################################################################
# GetData
###################################################################################
class GetData():
    def __init__(self, file=0):
        self.file = file
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

        self.cameraMatrix1 = np.transpose(IntrinsicMatrix1).astype('float64')
        self.distCoeffs1 = np.concatenate(
            (RadialDistortion1, TangentialDistortion1), axis=1).astype('float64')
        self.cameraMatrix2 = np.transpose(IntrinsicMatrix2).astype('float64')
        self.distCoeffs2 = np.concatenate(
            (RadialDistortion2, TangentialDistortion2), axis=1).astype('float64')
        self.imageSize = ImageSize.ravel()[::-1].astype('int64')
        self.RotationOfCamera2 = np.transpose(RotationOfCamera2).astype('float64')
        self.TranslationOfCamera2 = np.transpose(TranslationOfCamera2).astype('float64')

        self.FundamentalMatrix = fs.getNode("FundamentalMatrix").mat()

        print('\n cameraMatrix1\n', self.cameraMatrix1)
        print('\n distCoeffs1\n', self.distCoeffs1)
        print('\n cameraMatrix2\n', self.cameraMatrix2)
        print('\n distCoeffs2\n', self.distCoeffs2)
        print('\n imageSize\n', self.imageSize)
        print('\n RotationOfCamera2\n', self.RotationOfCamera2)
        print('\n TranslationOfCamera2\n', self.TranslationOfCamera2)
        print('\n FundamentalMatrix\n', self.FundamentalMatrix)
        print()

        ########################################### uart
        self.kuc = kevinuart.UartControl('/dev/ttyUSB1') # right camera
        self.kuc1 = kevinuart.UartControl('/dev/ttyUSB0') # left camera
        
        # binary thres:50 100
        self.kuc.ser_write(1, 100) 
        self.kuc1.ser_write(1, 100)

        ########################################### file
        self.count = 0
        if(file):
            self.data_file = open("data/result/point_data.csv", "w") # open point_data
            self.input_file = open("data/result/input_data.csv", "w") # open input_data

            text = ""
            for i in range(4): text += "p" + str(i) + "x," + "p" + str(i) + "y," + "p" + str(i) + "z,"
            text += "\n"
            self.data_file.write(text) # write point_data

            text = ""
            for i in range(2*4): text += "p1_x" + str(i) + "," + "p1_y" + str(i) + ","
            for i in range(2*4): text += "p2_x" + str(i) + "," + "p2_y" + str(i) + ","
            text += "\n"
            self.input_file.write(text) # write input_file

    ########################################## get_point 
    def getPoint(self, size=0, point2d_1=[], point2d_2=[]):
        self.kuc.uart_ser() # read uart right camera
        self.kuc1.uart_ser() # read uart left camera

        pointSize = 8
        if(size == 0):
            self.point2d_1 = self.kuc.point2d
            self.point2d_2 = self.kuc1.point2d
        else:
            self.point2d_1 = point2d_1
            self.point2d_2 = point2d_2
            pointSize = size

        ########################################### epipolar
        # for i in range(pointSize):
        #     point_1 = np.array([[self.point2d_1[i][0],self.point2d_1[i][1],1]])
        #     point_2 = np.array([[self.point2d_2[i][0],self.point2d_2[i][1],1]])
        #     self.point2d_1[i,1] = epipolar_line(FundamentalMatrix, point_1, 0, point_1[0][0], 0) # epipolar point
        #     self.point2d_2[i,1] = epipolar_line(FundamentalMatrix, point_2, 0, point_2[0][0], 1) # epipolar point

        ##################################### sorting
        # self.point2d_1 = np.sort(self.point2d_1.view('i8,i8'), order=['f1'], axis=0).view(np.int64)
        # self.point2d_2 = np.sort(self.point2d_2.view('i8,i8'), order=['f1'], axis=0).view(np.int64)
        
        #################################### print point
        # for i in range(pointSize):
        #     print("p"+str(i), self.point2d_1[i,0],self.point2d_1[i,1],self.point2d_2[i,0],self.point2d_2[i,1], end=' ')
        # print()

        ########################################### check

        ############################################# triangulate
        self.points3d = np.zeros((pointSize, 3), np.float64)
        for i in range(pointSize):
            if(self.point2d_1[i,0] or self.point2d_2[i,0]):
                self.points3d[i] = triangulate(self.cameraMatrix1, self.cameraMatrix2, self.RotationOfCamera2, self.TranslationOfCamera2, self.point2d_1[i], self.point2d_2[i])
            else:
                self.points3d[i] = [0.,0.,0.]

        return self.points3d

    ############################################ showImage
    def showImage(self, savePoint=0):
        pointSize = 8
        # cv draw picture
        output_image = np.full((480,640*2,3), 255, np.uint8) # create image

        for i in range(pointSize):
            if(self.point2d_1[i][0] and self.point2d_2[i][0]):
                cv2.line(output_image, tuple(self.point2d_1[i].astype(int)-(5,0)), tuple(self.point2d_1[i].astype(int)+(5,0)), (0, 0, 255))
                cv2.line(output_image, tuple(self.point2d_1[i].astype(int)-(0,5)), tuple(self.point2d_1[i].astype(int)+(0,5)), (0, 0, 255))
                cv2.line(output_image, tuple(self.point2d_2[i].astype(int)-(5,0)+(640,0)), tuple(self.point2d_2[i].astype(int)+(5,0)+(640,0)), (0, 0, 255))
                cv2.line(output_image, tuple(self.point2d_2[i].astype(int)-(0,5)+(640,0)), tuple(self.point2d_2[i].astype(int)+(0,5)+(640,0)), (0, 0, 255))


        text = "press s to save point"
        cv2.putText(output_image, text,
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        text = "Capture point: " + str(self.count)
        cv2.putText(output_image, text,
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        for i in range(pointSize):
            text = "p" + str(i) + " X: " + str(round(self.points3d[i, 0], 2)) + " Y: " + str(round(self.points3d[i, 1], 2)) + " Z: " + str(round(self.points3d[i, 2], 2))
            cv2.putText(output_image, text,
                        (10, 60+i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


        # Show the frames
        cv2.imshow("output_image", output_image)

        # Hit "q" to close the window
        inputKey = cv2.waitKey(1) & 0xFF

        # if q exit
        if inputKey == ord('q'):
            self.close()
            exit()

        # if s save
        elif (inputKey == ord('s') or savePoint) and self.file and self.point2d_1[0, 0] != 0:
            # write result data
            text = ""
            for i in range(pointSize):
                text += str(self.points3d[i, 0]) + ', ' + str(self.points3d[i, 1]) + ', ' + str(self.points3d[i, 2]) + ', '
            text += '\n'
            self.data_file.write(text)

            # write input data
            text = ""
            for i in range(pointSize):       
                text += str(self.point2d_1[i,0]) + ', ' + str(self.point2d_1[i,1]) + ', '
            for i in range(pointSize):       
                text += str(self.point2d_2[i,0]) + ', ' + str(self.point2d_2[i,1]) + ', '
            text += '\n'
            self.input_file.write(text)

            print('\nSave...', '\n')
            self.count += 1

    ############################## close
    def close(self):
        cv2.destroyAllWindows()
        if(self.file):
            self.data_file.close()
            self.input_file.close()
        print("Close....")

###################################################################################
# main
###################################################################################
if __name__ == '__main__':
    gd = GetData(file=1)
    
    ###################### get data by csv
    # df = pd.read_csv("data/result/input_data_.csv", header=0)
    # point = df.to_numpy()
    # for i in range(len(point)):
    #     point2d_1 = point[i,0:8].reshape((-1,2))
    #     point2d_2 = point[i,8:16].reshape((-1,2))

    #     test = np.full((4,2),1)
    #     gd.getPoint(size=4,point2d_1,point2d_2)
    #     gd.showImage(save=0)
    #     time.sleep(0.1)
    # gd.close()

    ###################### get data by cam
    while 1:
        start_time = time.time()
        gd.getPoint()
        gd.showImage(savePoint=1)
        print("\n--- total %s seconds ---" % (time.time() - start_time))
