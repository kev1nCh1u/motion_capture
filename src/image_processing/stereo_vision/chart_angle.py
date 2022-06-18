from turtle import color
from matplotlib import pyplot as plt
import pandas as pd

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

df = pd.read_csv("data/result/point_result.csv", header=0)
point = df.to_numpy()
# print(point[0])

savePlotPath = 'data/result/point_path_plot/marker_plot_3d' + '.png'

# point = point[(point[:,8] < 3)]

######################################################################
# show angle
######################################################################
num = np.arange(len(point[:,6]))
true = num * 10 + point[0,7]

fig, ax = plt.subplots()

# note that plot returns a list of lines.  The "l1, = plot" usage
# extracts the first element of the list into l1 using tuple
# unpacking.  So l1 is a Line2D instance, not a sequence of lines
ax.plot(num, true, '-.', label='True')
ax.plot(num, point[:,5], 'o-', label='Roll')
ax.plot(num, point[:,6], '--^', label='Pitch')
ax.plot(num, point[:,7], '-+', label='Yaw')

ax.legend()

ax.set_xlabel('Angle')
ax.set_ylabel('Number')
ax.set_title('Angle test')
plt.show()
