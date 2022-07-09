from matplotlib import pyplot as plt
import matplotlib.animation as animation
import pandas as pd

import numpy as np

# df = pd.read_csv("data/result/point_main.csv", header=0)
# df = pd.read_csv("data/result/point_main_robot_rom_2.csv", header=0)
df = pd.read_csv("data/result/point_main_human_rom_30.csv", header=0)
point = df.to_numpy()
# print(point[0])

savePlotPath = 'data/result/point_path_plot/marker_plot_3d' + '.png'

# point = point[600:]
print(len(point), point[0,:])
# point = point[::10]
point = point[(point[:,8] < 3)]
point = point[(point[:,19] < 3)]
# point = point[(point[:,0] == 0)]
# point = point[(point[:,11] == 1)]
point = point[(point[:,0] == 1)]
point = point[(point[:,11] == 0)]

point0 = point[:,0:11]
minYaw0 = np.min(point0[:,6])
maxYaw0 = np.max(point0[:,6])
print("minYaw0:",minYaw0,"maxYaw0:",maxYaw0)

point1 = point[:,11:]
minYaw1 = np.min(point1[:,6])
maxYaw1 = np.max(point1[:,6])
print("minYaw1:",minYaw1,"maxYaw1:",maxYaw1)

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
sc = ax.scatter(point0[:,1], point0[:,2], point0[:,3], s=20, label='Marker0', c=point0[:,8], cmap='jet',vmin=0, vmax=3)
sc = ax.scatter(point1[:,1], point1[:,2], point1[:,3], s=20, label='Marker1', c=point1[:,8], cmap='jet',vmin=0, vmax=3)

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

sc = ax.scatter(point0[:,1], point0[:,2], s=20, label='Marker'+str(int(point0[0,0])),vmin=0, vmax=3)
sc = ax.scatter(point1[:,1], point1[:,2], s=20, label='Marker'+str(int(point1[0,0])),vmin=0, vmax=3)
# ax.set_title('Distance '+ str(round(point[0,3]))+ "mm")
ax.legend()
# cbar = plt.colorbar(sc)
# cbar.set_label('RMSE(mm)')
plt.axis('scaled')
plt.show()


######################################################################
# animation
######################################################################

fig = plt.figure()
#creating a subplot 
ax = fig.add_subplot()
xs0 = []
ys0 = []
xs1 = []
ys1 = []

def animate(i):
    xs0.append(point0[i+1000,1])
    ys0.append(point0[i+1000,2])
    xs1.append(point1[i+1000,1])
    ys1.append(point1[i+1000,2])

    
    ax.clear()
    # ax.plot(xs, ys)

    sc = ax.scatter(xs0, ys0, s=20, label='Marker'+str(int(point0[0,0])),vmin=0, vmax=3)
    sc = ax.scatter(xs1, ys1, s=20, label='Marker'+str(int(point1[0,0])),vmin=0, vmax=3)
    ax.legend()

    plt.gca().invert_yaxis()
    plt.xlabel('X(mm)')
    plt.ylabel('Y(mm)')
    # plt.title('ROM')
	
    
ani = animation.FuncAnimation(fig, animate, interval=0.0001) 
plt.axis('scaled')
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


# plt.savefig(savePlotPath)
