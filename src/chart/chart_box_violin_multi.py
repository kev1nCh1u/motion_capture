import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

# df = pd.read_csv("data/result/point_main.csv", header=0)
# df1 = pd.read_csv("data/result/grid_point/point_main_grid_130.csv", header=0)
# df2 = pd.read_csv("data/result/grid_point/point_main_grid_150.csv", header=0)
# df3 = pd.read_csv("data/result/grid_point/point_main_grid_200.csv", header=0)
# df4 = pd.read_csv("data/result/grid_point/point_main_grid_250.csv", header=0)
# df5 = pd.read_csv("data/result/grid_point/point_main_grid_300.csv", header=0)
df1 = pd.read_csv("data/result/heart_path/point_main_heart_130.csv", header=0)
df2 = pd.read_csv("data/result/heart_path/point_main_heart_150.csv", header=0)
df3 = pd.read_csv("data/result/heart_path/point_main_heart_200.csv", header=0)
df4 = pd.read_csv("data/result/heart_path/point_main_heart_250.csv", header=0)
df5 = pd.read_csv("data/result/heart_path/point_main_heart_300.csv", header=0)
point1 = df1.to_numpy()
point2 = df2.to_numpy()
point3 = df3.to_numpy()
point4 = df4.to_numpy()
point5 = df5.to_numpy()
# print(point[0])

savePlotPath = 'data/result/point_path_plot/chart_box' + '.png'

point1 = point1[(point1[:,8] < 3)]
point2 = point2[(point2[:,8] < 3)]
point3 = point3[(point3[:,8] < 3)]
point4 = point4[(point4[:,8] < 3)]
point5 = point5[(point5[:,8] < 3)]

for i in range(8,11): print(np.average(point1[:,i]))
print(np.std(point1[:,8]))
print()
for i in range(8,11): print(np.average(point2[:,i]))
print(np.std(point2[:,8]))
print()
for i in range(8,11): print(np.average(point3[:,i]))
print(np.std(point3[:,8]))
print()
for i in range(8,11): print(np.average(point4[:,i]))
print(np.std(point4[:,8]))
print()
for i in range(8,11): print(np.average(point5[:,i]))
print(np.std(point5[:,8]))
print()

x1 = point1
x2 = point2
x3 = point3
x4 = point4
x5 = point5

###################################################
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# Fixing random state for reproducibility
np.random.seed(19680801)


# generate some random test data
all_data = [np.random.normal(0, std, 100) for std in range(5, 10)]

all_data = [x1[:,8],x2[:,8],x3[:,8],x4[:,8],x5[:,8]]
# print(np.average(all_data,axis=0))

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
    ax.set_xlabel('1000~3000 (mm)')
    ax.set_ylabel('RMSE (mm)')

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