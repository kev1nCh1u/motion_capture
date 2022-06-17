

# f = open("src/fpga/DE10_NANO_D8M_RTL/kevin/BINARY_FRAME_DATA.txt", "w")

# for i in range(100): # y
#     for j in range(200): # x
#         f.write("0 ")
#     f.write("\n")

# f.close()


# import numpy as np
# a = np.full((480,640), 0)
# # np.savetxt("src/fpga/DE10_NANO_D8M_RTL/kevin/BINARY_FRAME_DATA_2.txt", a, delimiter=" ")

# a.tofile('src/fpga/DE10_NANO_D8M_RTL/kevin/BINARY_FRAME_DATA_2.txt',sep=' ',format='%d')


import cv2
import numpy as np
from random import randrange


for j in range(1):

    data_file = open("src/fpga/DE10_NANO_D8M_RTL/kevin/img/"+ 'test_point_' + "{0:0=2d}".format(j)+ '.txt', "w") # open point_data
    img = cv2.imread('src/fpga/DE10_NANO_D8M_RTL/kevin/img/' + 'test_point_' + "{0:0=2d}".format(j)+ '.jpg', cv2.IMREAD_GRAYSCALE)
    (thresh, img) = cv2.threshold(img, 128, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    print(img[163,124])

    for y in range(0,480):
        for x in range(0,640):
            data_file.write(str(img[y,x])+ " ") # write point_data
        data_file.write("\n") # write point_data
    data_file.close()

    cv2.imshow("img", img) # Show the frames

    inputKey = cv2.waitKey(1) & 0xFF # Hit "q" to close the window