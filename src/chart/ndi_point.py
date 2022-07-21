from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

import os
import sys
sys.path.append(os.getcwd())
from lib.kevin import kevincv

######################################################################
# load data
######################################################################
df = pd.read_csv("data/result/ndi/ndi_probe.csv", header=0)
point = df.to_numpy()
# print(point[0])

# point = point[600:]
size = len(point)
print("size:",size)
print("point0:",point[0,:])
# point = point[(point[:,8] < 3)]

######################################################################
# rt
######################################################################
rota = kevincv.eulerToRotation(0,110,0,"xyz")
for i in range(size):
    point[i,8:11] = np.dot(rota,point[i,8:11])

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
sc = ax.scatter(point[:,8], point[:,9], point[:,10], s=20, label='Marker', c=point[:,11], cmap='jet',vmin=0, vmax=3)
ax.legend()
cbar = plt.colorbar(sc)
cbar.set_label('RMSE(mm)')
plt.show()

######################################################################
# show all 2d
######################################################################
# show plot 3d
fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('X(mm)')
ax.set_ylabel('Y(mm)')

# ax.set_xlim(-200,200)
# ax.set_ylim(200,-200)
plt.gca().invert_yaxis()

sc = ax.scatter(point[:,8], point[:,9], s=20, label='Marker', c=point[:,11], cmap='jet',vmin=0, vmax=3)
# ax.set_title('Distance '+ str(round(point[0,3]))+ "mm")
ax.legend()
cbar = plt.colorbar(sc)
cbar.set_label('RMSE(mm)')
plt.axis('scaled')
plt.show()
