import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



df = pd.read_csv("data/result/point_main_2.csv", header=0)
point = df.to_numpy()
# print(point[0])

savePlotPath = 'data/result/point_path_plot/marker_plot_3d' + '.png'

point = point[:300,:]

point = point[(point[:,8] < 1)]

point = point[point[:,3].argsort()]

############################
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(point[:,3], point[:,7], width, label='MSE')
rects2 = ax.bar(point[:,3], point[:,8], width, label='RMSE')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
# ax.set_xticks(x, labels)
ax.legend()

# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()