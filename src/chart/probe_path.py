from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

import os
import sys
sys.path.append(os.getcwd())
from lib.kevin import kevincv

df = pd.read_csv("data/result/point_main.csv", header=0)
# df = pd.read_csv("data/result/probe/point_main_probe_calibra.csv", header=0)
# df = pd.read_csv("data/result/point_main_probe_circle_0725.csv", header=0)
# df = pd.read_csv("data/result/probe/point_main_probe_circle_0725.csv", header=0)
point = df.to_numpy()
# print(point[0])

# point = point[::50]
size = len(point)
print(size)
point = point[(point[:,8] < 1)]

size = len(point)
print(size)

######################################################################
# calibration
######################################################################
# x = np.array([[13.34559791],[201.89268775],[38.79749708]])
x = np.array([[100.58224725],[257.4466134],[13.29701482]])
print("x",x)

######################################################################
# calculate probe
######################################################################
probe = np.zeros((size,3))
for i in range(size):
    # probeMarkerPos = np.reshape(pos[i],(3,1))
    # probeMarkerRota = rota[i]

    probeMarkerPos = np.reshape(point[i,1:4],(3,1))
    probeMarkerRota = kevincv.eulerToRotation(point[i,4],point[i,5],point[i,6],"xyz")
    # probeMarkerRota = kevincv.eulerToRotation(point[i,13],point[i,14],point[i,15],"xyz")
    # probeMarkerRota = np.reshape(point[i,4:13],(3,3))

    # xr = probeMarkerPos + x
    # probeAns = np.dot(probeMarkerRota, xr)

    xr = np.dot(probeMarkerRota,x)
    probeAns = probeMarkerPos + xr
    # probeAns = np.array([probeMarkerPos[0]-xr[0],probeMarkerPos[1]+xr[1],probeMarkerPos[2]+xr[2]])
    probe[i] = np.reshape(probeAns,(1,3))
    # print("probe",probe[i])
    
    probe[i] = point[i,1:4] # test

######################################################################
# calculate probe
######################################################################
# probe = np.zeros((20,3))
# for i in range(20):
#     # probeMarkerPos = np.reshape(pos[i],(3,1))
#     # probeMarkerRota = rota[i]

#     probeMarkerPos = np.reshape(point[i,1:4],(3,1))
#     probeMarkerRota = kevincv.eulerToRotation(point[i,4],point[i,5],point[i,6],"xyz")
#     # probeMarkerRota = kevincv.eulerToRotation(point[i,13],point[i,14],point[i,15],"xyz")
#     # probeMarkerRota = np.reshape(point[i,4:13],(3,3))

#     probeAns = np.dot(np.transpose(probeMarkerRota),(x - probeMarkerPos))

#     probe[i] = np.reshape(probeAns,(1,3))
#     # print("probe",probe[i])

######################################################################
# rt
######################################################################
rota = kevincv.eulerToRotation(110,0,0,"xyz")
for i in range(size):
    probe[i,0:3] = np.dot(rota,probe[i,0:3])

######################################################################
# calculate center
######################################################################
center = np.zeros(2)
center[0] = (np.max(probe[:,0]) - np.min(probe[:,0]))/2 + np.min(probe[:,0])
center[1] = (np.max(probe[:,1]) - np.min(probe[:,1]))/2 + np.min(probe[:,1])
print("center",center)

######################################################################
# calculate error
######################################################################
dis = np.zeros((size))
for i in range(size):
    dis[i] = kevincv.euclideanDistances3d(center,probe[i,0:2])
    # print("dis",dis[i])
print("error_rmse:",kevincv.rmseFuc(50,dis))
# print("error_rmse:",kevincv.rmseFuc(65,dis))
print("error_std:",np.std(dis))

######################################################################
# show all 3d
######################################################################
# show plot 3d
fig = plt.figure()
# ax = fig.gca(projection='3d')
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('X(mm)')
ax.set_ylabel('Y(mm)')
ax.set_zlabel('Z(mm)')
# ax.set_xlim(-200,200)
# ax.set_ylim(450,600)
# ax.set_zlim(-200,200)
# sc = ax.scatter(point[:,1], point[:,2], point[:,3], s=20, label='Marker',)
sc2 = ax.scatter(probe[:,0], probe[:,1], probe[:,2], s=20, label='Probe')
ax.legend()
plt.show()

######################################################################
# show all 2d
######################################################################
# show plot
fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('X(mm)')
ax.set_ylabel('Y(mm)')

plt.gca().invert_yaxis()

ax.add_patch(plt.Circle((center),50,color='r',alpha=1,fill=False))
ax.add_patch(plt.Circle((center),65,color='r',alpha=1,fill=False))

sc_ = ax.scatter(0, 0, s=20, color='r', label='True')
sc3 = ax.scatter(center[0], center[1], s=20, label='Center')
# sc = ax.scatter(point[:,0], point[:,2], s=20, label='Marker')
sc2 = ax.scatter(probe[:,0], probe[:,1], s=20, label='Probe')
# ax.set_title('Distance '+ str(round(point[0,3]))+ "mm")
ax.legend()
plt.axis('scaled')
plt.show()
