from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

df = pd.read_csv("data/result/point_main_robot_rom_2.csv", header=0)
point = df.to_numpy()
# print(point[0])

# point = point[3:-7]
point = point[::10]
point = point[(point[:,0] == 0)]
point = point[(point[:,11] == 1)]

point0 = point[:,0:11]
minYaw0 = np.min(point0[:,6])
maxYaw0 = np.max(point0[:,6])
print(minYaw0, maxYaw0)

point1 = point[:,11:]
minYaw1 = np.min(point1[:,6])
maxYaw1 = np.max(point1[:,6])
print(minYaw1, maxYaw1)

romAngle = np.abs(point0[:,6]) + np.abs(point1[:,6])
minYawRom = np.min(romAngle)
maxYawRom = np.max(romAngle)
print(minYawRom, maxYawRom)

robotAngle = 23.81

######################################################################
# show angle
######################################################################
num = np.arange(len(point0[:,6]))
true = num * 10 + point0[0,7]

fig, ax = plt.subplots()

# ax.plot(num, true, '-.', label='True')
# ax.plot(num, point[:,4], '-', label='Roll')
# ax.plot(num, point[:,5], '-', label='Pitch')
ax.plot(num, point0[:,6], '-', label='Yaw0')
ax.plot(num, point1[:,6], '-', label='Yaw1')
ax.plot(num, romAngle, '-', label='ROM')

ax.legend()

ax.set_xlabel('Number')
ax.set_ylabel('Angle(deg)')
ax.set_title('Angle ROM')


x1, y1 = [0, 200], [minYawRom, minYawRom]
x2, y2 = [0, 200], [maxYawRom, maxYawRom]
x3, y3 = [0, 200], [minYawRom+robotAngle, minYawRom+robotAngle]
plt.plot(x1, y1, '--', label='Base')
plt.plot(x2, y2, '--', label='Max')
plt.plot(x3, y3, '--', label='True')
plt.legend()

plt.show()
