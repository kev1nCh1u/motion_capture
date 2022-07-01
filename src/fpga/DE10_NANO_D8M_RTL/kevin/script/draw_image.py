

import cv2
import numpy as np

for j in range(4):
    img = cv2.imread('src/fpga/DE10_NANO_D8M_RTL/kevin/img/' + 'test_point_' + "{0:0=2d}".format(j)+ '.jpg', cv2.IMREAD_GRAYSCALE)

    gray_image = img
    ret, thresh = cv2.threshold(gray_image, 24, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (255, 0, 0), 1)

    points = np.zeros((4, 1, 2), np.int32)
    i = 0

    for c in contours:
		# calculate moments for each contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

		# kevin save point
        point = np.array([cX, cY], np.int32)
        points[i][0] = point
        i += 1

        cv2.line(img, tuple((cX-10, cY-10)), tuple((cX+10, cY+10)), (255, 255, 255), 2)
        cv2.line(img, tuple((cX-10, cY+10)), tuple((cX+10, cY-10)), (255, 255, 255), 2)

    cv2.imwrite("src/fpga/DE10_NANO_D8M_RTL/kevin/img/" + 'mark_point_' + "{0:0=2d}".format(j)+ '.jpg', img)
    cv2.imshow('img',img)
    cv2.waitKey(0)

cv2.destroyAllWindows()