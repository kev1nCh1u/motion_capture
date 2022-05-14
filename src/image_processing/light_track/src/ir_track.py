import cv2
import numpy as np
import time
import imutils

###################################################################################
# define
###################################################################################
capFlag = 0

###################################################################################
# ir_track
###################################################################################
def ir_track(frame, capFlag=1, showFlag=0):
	if showFlag:
		cv2.imshow('original frame',frame)
		cv2.waitKey(0)

	###################################################################################
	# threshold mask
	###################################################################################

	# convert the image to grayscale
	gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# convert the grayscale image to binary image
	ret,thresh = cv2.threshold(gray_image,80,255,0)
	# ret,thresh = cv2.threshold(gray_image,24,255,0)

	if showFlag:
		cv2.imshow('gray_image',gray_image)
		cv2.imshow('thresh',thresh)
		cv2.waitKey(0)

	###################################################################################
	# findContours
	###################################################################################
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if showFlag:
		cv2.drawContours(frame,contours,-1,(0,0,255),1)  
		cv2.imshow('imgResult',frame)
		# cv2.waitKey(0)

	###################################################################################
	# find center
	###################################################################################
	missCount = 0
	pointsNum = len(contours)
	points = np.zeros((pointsNum, 1, 2), np.int32)

	for i in range(pointsNum):
		# calculate moments for each contour
		M = cv2.moments(contours[i])
		if M["m00"] > 0:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])

			# kevin save point
			point = np.array([cX, cY], np.int32)
			points[i][0] = point

			# calculate x,y coordinate of center
			if showFlag:
				cv2.circle(frame, (cX, cY), 2, (0, 0, 255), -1)
				cv2.putText(frame, 'x:'+str(cX)+' y:'+str(cY), (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
		else:
			missCount = missCount + 1

	if missCount == len(contours):
		# print('miss point')
		if showFlag:
			cv2.putText(frame, 'miss point' , (10,10),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
			cv2.imshow('imgResult xy',frame)
			cv2.waitKey(1)
		return points
	else:
		if showFlag:
			cv2.imshow('imgResult xy',frame)
			if capFlag:
				cv2.waitKey(1)
			if not capFlag:
				cv2.waitKey(0)
				cv2.destroyAllWindows()
				exit()
		return points

###################################################################################
# main
###################################################################################
def main():

	if capFlag:
		# cap = cv2.VideoCapture(0)
		cap = cv2.VideoCapture('/home/kevin/MVviewer/videos/A5031CU815_4H05A85PAK641B0/Video_2021_10_08_165027_10.avi')

	while 1:
		if capFlag:
			ret, frame = cap.read()

		if not capFlag:
			# frame = cv2.imread("data/ir/Pic_2021_10_09_104654_1.bmp")
			frame = cv2.imread("data/ir/ir_led_4.bmp")
			ret = True

		if ret == True:
			# start_time = time.time()
			# print('cap get frame')
			points = ir_track(frame, capFlag, showFlag=0)
			print(points[0][0])
			# print("--- %s seconds ---" % (time.time() - start_time))
		else:
			print('error no cap frame')
			cv2.destroyAllWindows()
			exit()
		
if __name__ == '__main__':
	main()