from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

df = pd.read_csv("data/result/point_main_2.csv", header=0)
point = df.to_numpy()
# print(point[0])

savePlotPath = 'data/result/point_path_plot/marker_plot_3d' + '.png'

# point = point[:3000,:]

point = point[(point[:,8] < 3)]

point = point[point[:,3].argsort()]


######################################################################
# show all
######################################################################

t1 = np.arange(0.0, 2.0, 0.1)
t2 = np.arange(0.0, 2.0, 0.01)

fig, ax = plt.subplots()

# note that plot returns a list of lines.  The "l1, = plot" usage
# extracts the first element of the list into l1 using tuple
# unpacking.  So l1 is a Line2D instance, not a sequence of lines
l1 = ax.plot(point[:,3], point[:,8], 'o')
# l2 = ax.plot(point[:,3]+1, point[:,8], '--^')
# l3 = ax.plot(point[:,3]+2, point[:,8], '.')
# l4 = ax.plot(point[:,3]+3, point[:,8], 's-.')

# ax.legend((l2, l4), ('oscillatory', 'damped'), loc='upper right', shadow=True)
ax.set_xlabel('time')
ax.set_ylabel('volts')
ax.set_title('Damped oscillation')
plt.show()