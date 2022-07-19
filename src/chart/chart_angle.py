from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

df = pd.read_csv("data/result/point_main.csv", header=0)
# df = pd.read_csv("data/result/angle/point_main_angle_yaw.csv", header=0)
point = df.to_numpy()
# print(point[0])

# point = point[3:-7]
# point = point[::10]

print(len(point))
print(point.shape)
x = np.zeros((20,10,22))
for i in range(20):
    x[i] = point[i*10:i*10+10]

for j in range(20):
    # for i in range(8,11): print(np.average(x[j][:,i]))
    # print(np.std(x[j][:,8]))
    # print()

    print(round(np.average(x[j][:,4]),4))
    print(round(np.average(x[j][:,5]),4))
    print(round(np.average(x[j][:,6]),4))
    print(round(np.std(x[j][:,6]),4))
    print()


######################################################################
# show angle
######################################################################
num = np.arange(len(point[:,6]))
true = point[0,6] - num * 10
for i in range(len(true)):
    if(true[i] <= -179):
        true[i] = true[i] + 360

fig, ax = plt.subplots()

# ax.plot(num, true, '-.', label='True')
ax.plot(num, point[:,4], 'o-', label='Roll')
ax.plot(num, point[:,5], '--^', label='Pitch')
ax.plot(num, point[:,6], '-+', label='Yaw')

ax.legend()

ax.set_xlabel('Number')
ax.set_ylabel('Angle(deg)')
ax.set_title('Angle test')
plt.show()
