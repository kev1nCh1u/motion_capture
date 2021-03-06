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

from get_data_3d import *

###################################################################################
# main
###################################################################################
def main():
    gd = GetData(uart=1,file=0)
    body_num = input("Enter body num (0,1,2...): ")

    ########################################### init value
    fs = cv2.FileStorage("data/parameter/create_markers"+str(body_num)+".yaml", cv2.FILE_STORAGE_WRITE)
    count = 0
    num = body_num
    orginPoint_data = np.zeros((10,4,3))
    orginDistance_data = np.zeros((10,4,4))

    while 1:
        points3d = gd.getPoint()[0:4]

        #################################### cv draw picture
        output_image = np.full((480,640*2,3), 255, np.uint8) # create image

        for i in range(4):
            if(gd.point2d_1[i][0] and gd.point2d_2[i][0]):
                cv2.line(output_image, tuple(gd.point2d_1[i].astype(int)-(5,0)), tuple(gd.point2d_1[i].astype(int)+(5,0)), (0, 0, 255))
                cv2.line(output_image, tuple(gd.point2d_1[i].astype(int)-(0,5)), tuple(gd.point2d_1[i].astype(int)+(0,5)), (0, 0, 255))
                cv2.line(output_image, tuple(gd.point2d_2[i].astype(int)-(5,0)+(640,0)), tuple(gd.point2d_2[i].astype(int)+(5,0)+(640,0)), (0, 0, 255))
                cv2.line(output_image, tuple(gd.point2d_2[i].astype(int)-(0,5)+(640,0)), tuple(gd.point2d_2[i].astype(int)+(0,5)+(640,0)), (0, 0, 255))


        text = "press s to capture point"
        cv2.putText(output_image, text,
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        text = "Capture point: " + str(num) + " count:" + str(count)
        cv2.putText(output_image, text,
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        for i in range(4):
            text = "p" + str(i) + " X: " + str(round(points3d[i, 0], 2)) + " Y: " + str(round(points3d[i, 1], 2)) + " Z: " + str(round(points3d[i, 2], 2))
            cv2.putText(output_image, text,
                        (10, 60+i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        ############################## Show the frames
        cv2.imshow("output_image", output_image)

        # Hit "q" to close the window
        inputKey = cv2.waitKey(1) & 0xFF

        # if q exit
        if inputKey == ord('q'):
            # orginPoint = np.median(orginPoint_data,axis=0)
            # orginDistance = np.median(orginDistance_data,axis=0)
            # fs.write('orginDistance', orginDistance)
            # fs.write('orginPoint', orginPoint)
            # print("orginDistance\n",orginDistance)
            # print("orginPoint\n",orginPoint)
            break

        # if s capture
        elif inputKey == ord('s'):
            orginPoint = points3d
            orginDistance = findAllDis(points3d)
            fs.write('orginDistance', orginDistance)
            fs.write('orginPoint', orginPoint)
            print("orginDistance\n",orginDistance)
            print("orginPoint\n",orginPoint)
            break

            if(count < len(orginPoint_data)):
                orginPoint_data[count] = points3d
                orginDistance_data[count] = findAllDis(points3d)
                count += 1



    ############################## close
    cv2.destroyAllWindows()
    fs.release()


# if main
if __name__ == '__main__':
    main()