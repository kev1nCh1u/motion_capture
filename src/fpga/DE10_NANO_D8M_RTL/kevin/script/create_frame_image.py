import cv2
import numpy as np
from random import randrange

data_file = open("src/fpga/DE10_NANO_D8M_RTL/kevin/img/point_data.txt", "w") # open point_data
data_file.write("x y \n") # write point_data

for j in range(4):

    img = np.full((480,640,1), 0, np.uint8) # create image

    for i in range(4):
        x = randrange(10,630)
        y = randrange(10,470)
        cv2.circle(img,(x, y), 2, 255, -1) # gen point
        data_file.write(str(x) + " " + str(y) + "\n") # write point_data

    data_file.write("\n") # write point_data

    cv2.imshow("img", img) # Show the frames

    cv2.imwrite("src/fpga/DE10_NANO_D8M_RTL/kevin/img/" + 'test_point_' + "{0:0=2d}".format(j)+ '.jpg', img)
    
    inputKey = cv2.waitKey(1) & 0xFF # Hit "q" to close the window