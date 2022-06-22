from itertools import count
from socket import AF_IPX
import cv2  
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("data/example/red-heart.png")  

 
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
ret, binary = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)  
cv2.imshow("gray", gray)  
cv2.imshow("binary", binary)  
 
# contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
contours, hierarchy = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  
cv2.drawContours(img,contours,-1,(0,255,255),3)  
print(contours[0][-3])
print("size:", len(contours[0]))

cv2.imshow("img", img)  
cv2.waitKey(1)  

contoursNp = np.array(contours).reshape(-1,2)
print(len(contoursNp))
contoursNp = contoursNp[::30] # down_sample
print(contoursNp)

NewMin = np.array([-92,372]) # x,z
NewMax = np.array([208,72])
OldRange = (np.array([640,480]) - np.array([0,0]))  # (OldMax - OldMin)
NewRange = (NewMax - NewMin)  # (NewMax - NewMin)
path = (((contoursNp - [0,0]) * NewRange) / OldRange) + NewMin # (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

# path = (contoursNp / [640,480]) * [-92,6] + [208,456]
# print(path[-3])

# show all 2d
fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_xlim(NewMin[0]-50,NewMax[0]+50)
ax.set_ylim(NewMax[1]-50,NewMin[1]+50)

# sc = ax.scatter(path[:,0], path[:,1], s=20, label='Path', c=path[:,0], cmap='jet')
sc = ax.scatter(path[:,0], path[:,1], s=20, label='Path')
ax.legend()
# cbar = plt.colorbar(sc)
# cbar.set_label('X')

robotNp = np.zeros((len(contoursNp),7))
robotNp[:,0] = path[:,0]
robotNp[:,1] = 456
robotNp[:,2] = path[:,1]
robotNp[:,3] = -180
robotNp[:,4] = 0
robotNp[:,5] = -90
robotNp[:,6] = 100000

print(robotNp[1])

fs = cv2.FileStorage("src/robot_arm/robot_path.yaml", cv2.FILE_STORAGE_WRITE)
fs.write('path', robotNp)

plt.show()