from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

import os
import sys
sys.path.append(os.getcwd())
from lib.kevin import kevincv

df = pd.read_csv("data/result/point_main.csv", header=0)
# df = pd.read_csv("data/result/probe/point_main_probe_calibra.csv", header=0)
# df = pd.read_csv("data/result/point_main_probe_calibra.csv", header=0)
point = df.to_numpy()
# print(point[0])

# point = point[::50]
print(len(point))
point = point[(point[:,8] < 1)]
point_high_accuracy = point[(point[:,8] < 0.7)]
# point = point[(point[:,17] < 1)]
# point_high_accuracy = point[(point[:,17] < 0.7)]

size = len(point)
print(size)

######################################################################
# show all
######################################################################
# # show plot 3d
# fig = plt.figure()
# # ax = fig.gca(projection='3d')
# ax = fig.add_subplot(projection='3d')
# ax.set_xlabel('X(mm)')
# ax.set_ylabel('Y(mm)')
# ax.set_zlabel('Z(mm)')
# # ax.set_xlim(-200,200)
# # ax.set_ylim(450,600)
# # ax.set_zlim(-200,200)
# sc = ax.scatter(point[:,1], point[:,2], point[:,3], s=20, label='Marker', c=point[:,8], cmap='jet',vmin=0, vmax=3)
# # sc = ax.scatter(point[:,1], point[:,2], point[:,3], s=20, label='Marker', c=point[:,17], cmap='jet',vmin=0, vmax=3)
# ax.legend()
# cbar = plt.colorbar(sc)
# cbar.set_label('RMSE(mm)')
# plt.show()

######################################################################
# show all 2d
######################################################################
# # show plot 3d
# fig = plt.figure()
# ax = fig.add_subplot()
# ax.set_xlabel('X(mm)')
# ax.set_ylabel('Y(mm)')

# # ax.set_xlim(-200,200)
# # ax.set_ylim(200,-200)
# plt.gca().invert_yaxis()

# # sc = ax.scatter(point[:,1], point[:,2], s=20, label='Marker', c=point[:,8], cmap='jet',vmin=0, vmax=3)
# sc = ax.scatter(point[:,1], point[:,2], s=20, label='Marker', c=point[:,17], cmap='jet',vmin=0, vmax=3)
# # ax.set_title('Distance '+ str(round(point[0,3]))+ "mm")
# ax.legend()
# cbar = plt.colorbar(sc)
# cbar.set_label('RMSE(mm)')
# plt.show()


######################################################################
# calibration
######################################################################
rota = np.zeros((10,3,3))
for i in range(4):
    rota[i] = kevincv.eulerToRotation(point_high_accuracy[i,4],point_high_accuracy[i,5],point_high_accuracy[i,6],"xyz")
    # rota[i] = kevincv.eulerToRotation(point_high_accuracy[i,13],point_high_accuracy[i,14],point_high_accuracy[i,15],"xyz")
    print("rota",rota[i])
    # rota[i] = np.reshape(point[i,4:13],(3,3))
    # print("rota_",rota[i])

R = np.array([rota[0]-rota[1], rota[0]-rota[2], rota[0]-rota[3]])
R = np.reshape(R,(9,3))
# print("R",R)

pos = np.zeros((10,3))
for i in range(4):
    pos[i] = np.array([point_high_accuracy[i,1],point_high_accuracy[i,2],point_high_accuracy[i,3]])
    # print("pos",pos[i])

p = np.array([pos[1]-pos[0], pos[2]-pos[0], pos[3]-pos[0]])
p = np.reshape(p,(9,1))
# print("p",p)

x = np.linalg.lstsq(R,p, rcond=None)[0]
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

######################################################################
# calculate probe
######################################################################
# probe = np.zeros((size,3))
# for i in range(size):
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
# show all
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
sc = ax.scatter(point[:,1], point[:,2], point[:,3], s=20, label='Marker',)
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

# ax.set_xlim(-200,200)
# ax.set_ylim(200,-200)
plt.gca().invert_yaxis()

sc = ax.scatter(point[:,1], point[:,2], s=20, label='Marker')
sc2 = ax.scatter(probe[:,0], probe[:,1], s=20, label='Probe')
# ax.set_title('Distance '+ str(round(point[0,3]))+ "mm")
ax.legend()
plt.axis('scaled')
plt.show()
