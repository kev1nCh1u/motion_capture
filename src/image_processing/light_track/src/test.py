
# kevin import outside path
import sys, os
print(os.getcwd())
sys.path.append(os.getcwd())

from src.image_processing.ir_track.build import hello_ext
print(hello_ext.greet())


###################################################################################
# ir_track.so test
###################################################################################

import cv2
import numpy as np
from src.image_processing.ir_track.build import ir_track_boostpy

capFlag = 0

def main():

	if capFlag:
		# cap = cv2.VideoCapture(0)
		cap = cv2.VideoCapture('/home/kevin/MVviewer/videos/A5031CU815_4H05A85PAK641B0/Video_2021_10_08_165027_10.avi')

	while 1:
		if capFlag:
			ret, frame = cap.read()

		if not capFlag:
			# frame = cv2.imread("img/ir/Pic_2021_10_09_104654_1.bmp")
			frame = cv2.imread("img/ir/ir_led_4.bmp")
			ret = True

		if ret == True:
			# start_time = time.time()
			# print('cap get frame')
			print(type(frame))
			points = ir_track_boostpy.ir_track(frame, False, False)
			print(points[0][0])
			# print("--- %s seconds ---" % (time.time() - start_time))
		else:
			print('error no cap frame')
			cv2.destroyAllWindows()
			exit()
		
if __name__ == '__main__':
	main()