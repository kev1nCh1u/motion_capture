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

gd = GetData()

###################################################################################
# main
###################################################################################
def main():

    ########################################### init value
    fs = cv2.FileStorage("data/parameter/create_markers.yaml", cv2.FILE_STORAGE_WRITE)
    count = 0
    num = 0

    while 1:
        points3d = gd.getPoint()

        #################################### cv draw picture
        output_image = np.full((480,640*2,3), 255, np.uint8) # create image

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
            break

        # if c capture
        elif inputKey == ord('s'):
            orginPoint_data = np.zeros((5,4,3))
            orginDistance_data = np.zeros((5,4,4))

            orginPoint_data[count] = points3d
            orginDistance_data[count] = findAllDis(points3d)

            orginPoint = np.median(orginPoint_data,axis=0)
            orginDistance = np.median(orginDistance_data,axis=0)
            
            count += 1

            if(count == 5):
                fs.write('orginDistance'+str(num), orginDistance)
                fs.write('orginPoint'+str(num), orginPoint)
                count = 0
                num += 1

    ############################## close
    cv2.destroyAllWindows()
    fs.release()


# if main
if __name__ == '__main__':
    main()