from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

import os
import sys
sys.path.append(os.getcwd())
from lib.kevin import kevincv


######################################################################
# load kevin data
######################################################################
df = pd.read_csv("data/result/point_main.csv", header=0)
# df = pd.read_csv("data/result/probe/point_main_probe_calibra.csv", header=0)
# df = pd.read_csv("data/result/point_main_probe_circle.csv", header=0)
# df = pd.read_csv("data/result/probe/point_main_probe_circle_0725.csv", header=0)
point = df.to_numpy()

point = point[(point[:,8] < 1)]
point_high_accuracy = point[(point[:,8] < 0.7)]

size = len(point)
print("size",size)

######################################################################
# load ndi data
######################################################################
df = pd.read_csv("data/result/ndi/ndi_probe.csv", header=0)
point_ndi = df.to_numpy()

# point_ndi = point_ndi[(point_ndi[:,8] < 3)]

size_ndi = len(point_ndi)
print("size_ndi",size_ndi)
# print("point_ndi0:",point_ndi[0,:])


######################################################################
# calibration
######################################################################
# x = np.array([[13.34559791],[201.89268775],[38.79749708]])
x = np.array([[100.58224725],[257.4466134 ],[ 13.29701482]])

print("x",x)

######################################################################
# calculate probe
######################################################################
probe = np.zeros((size,3))
for i in range(size):
    probeMarkerPos = np.reshape(point[i,1:4],(3,1))
    probeMarkerRota = kevincv.eulerToRotation(point[i,4],point[i,5],point[i,6],"xyz")

    xr = np.dot(probeMarkerRota,x)
    probeAns = probeMarkerPos + xr
    probe[i] = np.reshape(probeAns,(1,3))
    # print("probe",probe[i])

    probe[i] = point[i,1:4] # test

######################################################################
# rt
######################################################################
# rota = kevincv.eulerToRotation(130,-5,0,"xyz")
rota = kevincv.eulerToRotation(110,0,0,"xyz")
for i in range(size):
    probe[i,0:3] = np.dot(rota,probe[i,0:3])

rota = kevincv.eulerToRotation(0,110,0,"xyz")
for i in range(size_ndi):
    # rota = np.dot(3,rota)
    # rota = 3*rota
    # rota = np.cross(3,rota)
    point_ndi[i,8:11] = np.dot(rota,point_ndi[i,8:11])

######################################################################
# calculate center
######################################################################
center = np.zeros(2)
center[0] = (np.max(probe[:,0]) - np.min(probe[:,0]))/2 + np.min(probe[:,0])
center[1] = (np.max(probe[:,1]) - np.min(probe[:,1]))/2 + np.min(probe[:,1])
print("center",center)

center_ndi = np.zeros(2)
center_ndi[0] = (np.max(point_ndi[:,8]) - np.min(point_ndi[:,8]))/2 + np.min(point_ndi[:,8])
center_ndi[1] = (np.max(point_ndi[:,9]) - np.min(point_ndi[:,9]))/2 + np.min(point_ndi[:,9])
print("center_ndi",center_ndi)

center_t = center_ndi - center
print("center_t",center_t)

point_ndi[:,8] = point_ndi[:,8]-center_t[0]
point_ndi[:,9] = point_ndi[:,9]-center_t[1]

######################################################################
# show all 3d
######################################################################
# fig = plt.figure()
# # ax = fig.gca(projection='3d')
# ax = fig.add_subplot(projection='3d')
# ax.set_xlabel('X(mm)')
# ax.set_ylabel('Y(mm)')
# ax.set_zlabel('Z(mm)')
# # sc = ax.scatter(point[:,1], point[:,2], point[:,3], s=20, label='Marker',)
# sc2 = ax.scatter(probe[:,0], probe[:,1], probe[:,2], s=20, label='Probe')
# # sc3 = ax.scatter(point_ndi[:,8]-center_t[0], point_ndi[:,9]-center_t[1], point_ndi[:,10], s=20, label='NDI', c=point_ndi[:,11], cmap='jet',vmin=0, vmax=3)
# ax.legend()
# plt.show()

######################################################################
# calculate error
######################################################################
dis = np.zeros((size))
for i in range(size):
    dis[i] = kevincv.euclideanDistances3d(center,probe[i,0:2])
    # print("dis",dis[i])
print("error_rmse:",kevincv.rmseFuc(50,dis))
print("error_std:",np.std(dis))

dis = np.zeros((size_ndi))
for i in range(size_ndi):
    dis[i] = kevincv.euclideanDistances3d(center,point_ndi[i,8:10])
    # print("dis",dis[i])
print("ndi_error_rmse:",kevincv.rmseFuc(65,dis))
print("ndi_error_std:",np.std(dis))

######################################################################
# show all 2d
######################################################################
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
sc2 = ax.scatter(probe[:,0], probe[:,1], s=20, label='Our')
sc4 = ax.scatter(point_ndi[:,8], point_ndi[:,9], s=20, label='NDI', c=point_ndi[:,11], cmap='jet',vmin=0, vmax=3)
ax.set_title('Probe circle test ')
# ax.text(2.0,9.5,"qqqqqq",fontsize=14)
ax.legend()
plt.axis('scaled')
plt.show()
