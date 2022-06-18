import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



df = pd.read_csv("data/result/point_main_2.csv", header=0)
point = df.to_numpy()
# print(point[0])

savePlotPath = 'data/result/point_path_plot/marker_plot_3d' + '.png'

point = point[:,:]

point = point[(point[:,8] < 1)]

point = point[point[:,3].argsort()]

x1 = point[(point[:,3] < 1000)]
x2 = point[((point[:,3] > 1000) & (point[:,3] < 1500))]
x3 = point[((point[:,3] > 1500) & (point[:,3] < 2000))]
x4 = point[((point[:,3] > 2000) & (point[:,3] < 2500))]
x5 = point[((point[:,3] > 250) & (point[:,3] < 3000))]

x1_mse = np.average(x1[:,7])
x2_mse = np.average(x2[:,7])
x3_mse = np.average(x3[:,7])
x4_mse = np.average(x4[:,7])
x5_mse = np.average(x5[:,7])

x1_rmse = np.average(x1[:,8])
x2_rmse = np.average(x2[:,8])
x3_rmse = np.average(x3[:,8])
x4_rmse = np.average(x4[:,8])
x5_rmse = np.average(x5[:,8])

############################
width = 0.15  # the width of the bars

mse = [x1_mse,x2_mse,x3_mse,x4_mse,x5_mse]
rmse = [x1_rmse,x2_rmse,x3_rmse,x4_rmse,x5_rmse]

dis = np.arange(5)*0.5+1
print(dis)

fig, ax = plt.subplots()
rects1 = ax.bar(dis-width/2, mse, width, label='MSE')
rects2 = ax.bar(dis+width/2, rmse, width, label='RMSE')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Distance (M)')
ax.set_ylabel('Error (mm)')
ax.set_title('MSE and RMSE')
# ax.set_xticks(x, labels)
ax.legend()

# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()