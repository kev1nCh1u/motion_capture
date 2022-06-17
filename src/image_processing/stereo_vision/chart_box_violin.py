import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

df = pd.read_csv("data/result/point_main_2.csv", header=0)
point = df.to_numpy()
# print(point[0])

savePlotPath = 'data/result/point_path_plot/chart_box' + '.png'

point = point[(point[:,8] < 10)]

point = point[point[:,3].argsort()]

x1 = point[(point[:,3] < 1000)]
x2 = point[((point[:,3] > 1000) & (point[:,3] < 1500))]
x3 = point[((point[:,3] > 1500) & (point[:,3] < 2000))]
x4 = point[((point[:,3] > 2000) & (point[:,3] < 2500))]
x5 = point[((point[:,3] > 250) & (point[:,3] < 3000))]

###################################################
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# Fixing random state for reproducibility
np.random.seed(19680801)


# generate some random test data
all_data = [np.random.normal(0, std, 100) for std in range(5, 10)]

all_data = [x1[:,8],x2[:,8],x3[:,8],x4[:,8],x5[:,8]]


# plot violin plot
bplot1 = axs[0].violinplot(all_data,
                  showmeans=False,
                  showmedians=True)
axs[0].set_title('Violin plot')

# plot box plot
bplot2 = axs[1].boxplot(all_data)
axs[1].set_title('Box plot')

# adding horizontal grid lines
for ax in axs:
    ax.yaxis.grid(True)
    ax.set_xticks([y + 1 for y in range(len(all_data))],
                  labels=['D1', 'D2', 'D3', 'D4', 'D5'])
    ax.set_xlabel('1000~3000')
    ax.set_ylabel('RMSE')

# for pc in bplot1['bodies']:
#     pc.set_facecolor('red')
#     pc.set_edgecolor('black')

# fill with colors
# colors = ['pink', 'lightblue', 'lightgreen', 'lightgreen', 'lightgreen']
# for patch, color in zip(bplot2['boxes'], colors):
#     patch.set_color(color)
#     patch.set_facecolor(color)
#     patch.set_edgecolor(color)
#     patch.set_markeredgecolor(color)

plt.show()