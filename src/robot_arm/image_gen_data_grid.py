from socket import AF_IPX
import cv2  
import numpy as np
from matplotlib import pyplot as plt


import pandas as pd

############################################
# data
#############################################
df = pd.read_csv("data/result/point_main_2.csv", header=0)
point = df.to_numpy()
# print(point[0])

savePlotPath = 'data/result/point_path_plot/chart_box' + '.png'

point = point[(point[:,8] < 10)]

point = point[point[:,3].argsort()]

x1 = point[((point[:,3] > 1000) & (point[:,3] <= 1500))]
x2 = point[((point[:,3] > 1500) & (point[:,3] <= 2000))]
x3 = point[((point[:,3] > 2000) & (point[:,3] <= 2500))]
x4 = point[((point[:,3] > 250) & (point[:,3] <= 3000))]

############################################
# chart
#############################################
contours = np.zeros((100,2))
count = 0
for i in range(10):
    for j in range(10):
        contours[count] = [i*50,j*50]
        count += 1

print(contours)

contoursNp = np.array(contours).reshape(-1,2)
# size = len(contoursNp)
print("contoursNp size:",len(contoursNp))
# contoursNp = contoursNp[::8] # down_sample
print("contoursNp size:",len(contoursNp))
error = np.random.normal(0, 2, (len(contoursNp),2))
contoursNp = contoursNp + error

NewMin = np.array([-100,50]) # x,y
NewMax = np.array([300,-200])
OldRange = (np.array([640,480]) - np.array([0,0]))  # (OldMax - OldMin)
NewRange = (NewMax - NewMin)  # (NewMax - NewMin)
path = (((contoursNp - [0,0]) * NewRange) / OldRange) + NewMin # (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

# path = (contoursNp / [640,480]) * [-92,6] + [208,456]
# print(path[-3])

# show all 2d
fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_xlim(NewMin[0]-50,NewMax[0]+50)
ax.set_ylim(NewMax[1]-50,NewMin[1]+50)

# gen rmse
rmse = x1[:len(contoursNp),8]
np.random.shuffle(rmse)
print("rmse size:", len(rmse))
# exit()

sc = ax.scatter(path[:,0], path[:,1], s=20, label='Path', c=rmse, cmap='jet')
# sc = ax.scatter(path[:,0], path[:,1], s=20, label='Path')
ax.legend()
cbar = plt.colorbar(sc)
cbar.set_label('X')

robotNp = np.zeros((len(contoursNp),7))
robotNp[:,0] = path[:,0]
robotNp[:,1] = 456
robotNp[:,2] = path[:,1]
robotNp[:,3] = -180
robotNp[:,4] = 0
robotNp[:,5] = 180
robotNp[:,6] = 100000

print(robotNp[1])

fs = cv2.FileStorage("src/robot_arm/robot_path.yaml", cv2.FILE_STORAGE_WRITE)
fs.write('path', robotNp)

plt.show()