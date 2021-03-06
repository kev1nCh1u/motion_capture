import cv2
import numpy as np
import time

# cap = cv2.VideoCapture(0)
for frame in range(4):
	start_time = time.time()
	cap = cv2.imread('src/fpga/DE10_NANO_D8M_RTL/kevin/img/' + 'test_point_' + "{0:0=2d}".format(frame)+ '.jpg', cv2.IMREAD_GRAYSCALE)
	# cv2.imshow('org cap',cap)
	# cv2.waitKey(0)

	###################################################################################
	# threshold mask
	###################################################################################
	img = cap.copy()

	# convert the image to grayscale
	# gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray_image = img

	# convert the grayscale image to binary image
	ret, thresh = cv2.threshold(gray_image, 24, 255, 0)

	# cv2.imshow('gray_image', gray_image)
	# cv2.imshow('thresh', thresh)
	# cv2.waitKey(0)
	mask = thresh.copy()

	###################################################################################
	# findContours
	###################################################################################
	imgResult = cap.copy()
	contours, hierarchy = cv2.findContours(
		mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(imgResult, contours, -1, (255, 0, 0), 1)

	# cv2.imshow('contours',imgResult)
	# cv2.waitKey(0)

	###################################################################################
	# find center
	###################################################################################
	# kevin value
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

		# calculate x,y coordinate of center
		cv2.circle(imgResult, (cX, cY), 2, (0, 255, 0), -1)
		xy = 'x:' + str(cX) + ' y:' + str(cY)
		cv2.putText(imgResult, xy, (cX + 2, cY + 2),
					cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
		print(cX, cY)
	print()
	# cv2.imshow('imgResult',imgResult)
	# cv2.waitKey(0)

	###################################################################################
	# end
	###################################################################################
	print("--- total %s seconds ---" % (time.time() - start_time))
	# cv2.waitKey(0)
	cv2.destroyAllWindows()
