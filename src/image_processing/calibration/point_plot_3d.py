from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd


path = "data/point_data_02171745.csv"
savePlotPath = 'img/result/point_path_plot/point_path_plot_' + '02171745' + '.png'

df = pd.read_csv(path, header=None)
world_points = df.to_numpy()

# show plot 3d
axis = 2 # x:0 y:1 z:2
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_zlabel('Y')
ax.set_xlim(-200,200)
ax.set_ylim(300,500)
ax.set_zlim(-200,200)
ax.scatter(world_points[:,0], world_points[:,2], world_points[:,1], label='Point')
ax.legend()
plt.savefig(savePlotPath)
plt.show()