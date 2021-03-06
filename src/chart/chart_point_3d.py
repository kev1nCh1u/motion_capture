from matplotlib import pyplot as plt
import pandas as pd

# df = pd.read_csv("data/result/point_data.csv", header=0)
df = pd.read_csv("data/result/point_find.csv", header=0)
point = df.to_numpy()
# print(point[0])
point = point[::300]

savePlotPath = 'data/result/point_path_plot/point_plot_3d' + '.png'

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
for i in range(4):
    ax.scatter(point[:,0+i*3], point[:,1+i*3], point[:,2+i*3], s=10, label='Point'+str(i))
ax.legend()
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