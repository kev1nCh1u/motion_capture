from matplotlib import pyplot as plt
import pandas as pd

import numpy as np
import cv2

########################### load data
df = pd.read_csv("data/result/point_main.csv", header=0)
df = pd.read_csv("data/result/grid_point/point_main_grid_130.csv", header=0)
# df = pd.read_csv("data/result/heart_path/point_main_heart_250.csv", header=0)
# df = pd.read_csv("data/result/point_main_dis.csv", header=0)
point = df.to_numpy()
# print(point[0])
# point = point[600:]
point = point[(point[:,8] < 3)]

########################### load path
fs = cv2.FileStorage("src/robot_arm/robot_path_grid.yaml", cv2.FILE_STORAGE_READ)
path = fs.getNode("path").mat()
print(path[1])
path_size = len(path)



######################################################################
# show all
######################################################################
# show plot 3d
fig = plt.figure()
# ax = fig.gca(projection='3d')
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
# ax.set_xlim(-200,200)
# ax.set_ylim(450,600)
# ax.set_zlim(-200,200)
sc = ax.scatter(point[:,1], point[:,2], point[:,3], s=20, label='Marker', c=point[:,8], cmap='jet',vmin=0, vmax=3)
ax.scatter(path[:,0], path[:,1], path[:,2], s=20, label='True', cmap='jet',vmin=0, vmax=3)
ax.legend()
cbar = plt.colorbar(sc)
cbar.set_label('RMSE')
plt.show()

######################################################################
# show all 2d
######################################################################
# show plot 3d
fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('X')
ax.set_ylabel('Y')

# ax.set_xlim(-200,200)
# ax.set_ylim(200,-200)
plt.gca().invert_yaxis()

sc = ax.scatter(point[:,1], point[:,2], s=20, label='Marker', c=point[:,8], cmap='jet',vmin=0, vmax=3)
# ax.set_title('Distance '+ str(round(point[0,3]))+ "mm")
ax.legend()
cbar = plt.colorbar(sc)
cbar.set_label('RMSE')
plt.show()

######################################################################
# show one a time
######################################################################
# print(len(point[:]))
# for i in range(len(point[:])):
#     # show plot 3d
#     fig = plt.figure()
#     ax = fig.add_subplot(projection='3d')
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Z')
#     for j in range(4):
#         ax.scatter(point[i,0+j*3], point[i,1+j*3], point[i,2+j*3], label='Point'+str(i))
#     ax.legend()
#     plt.show()
