import numpy as np 
import cv2

yy = 1
qq = np.zeros((3,480,640,3), np.uint8)
print(qq)
cv2.imshow('qq', qq[0])
cv2.waitKey(0)