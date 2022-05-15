from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd


path = "data/result/point_data.csv"
savePlotPath = 'data/result/point_path_plot/point_path_plot' + '.png'

df = pd.read_csv(path, header=None)
point = df.to_numpy()

# show plot 3d
axis = 2 # x:0 y:1 z:2
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_zlabel('Y')
ax.set_xlim(-200,200)
ax.set_ylim(450,600)
ax.set_zlim(-200,200)
for i in range(4):
    ax.scatter(point[:,0+i*3], point[:,2+i*3], point[:,1+i*3], label='Point'+str(i))
ax.legend()
plt.savefig(savePlotPath)
plt.show()