from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

df = pd.read_csv("data/result/ndi/walk_50.csv", header=0)
# df = pd.read_csv("data/result/point_main_robot_rom_2.csv", header=0)
# df = pd.read_csv("data/result/point_main_human_rom_30.csv", header=0)
point = df.to_numpy()
# print(point[0])

point = point[3:200]

point0 = point[:,0:29]
minYaw0 = np.min(point0[:,6])
maxYaw0 = np.max(point0[:,6])
print("minYaw0:",minYaw0,"maxYaw0:",maxYaw0)

point1 = point[:,29:]
minYaw1 = np.min(point1[:,6])
maxYaw1 = np.max(point1[:,6])
print("minYaw1:",minYaw1,"maxYaw1:",maxYaw1)

romAngle = np.abs(point0[:,6]) - np.abs(point1[:,6])
minYawRom = np.min(romAngle)
maxYawRom = np.max(romAngle)
print("minYawRom",minYawRom,"maxYawRom",maxYawRom)

robotAngle = 23.81

######################################################################
# show angle
######################################################################
num = np.arange(len(point0[:,6]))
true = num * 10 + point0[0,7]

fig, ax = plt.subplots()

# ax.plot(num, true, '-.', label='True')
# ax.plot(num, point0[:,4], '-', label='Roll0')
# ax.plot(num, point0[:,5], '-', label='Pitch0')
# ax.plot(num, point0[:,6], '-', label='Yaw0')
# ax.plot(num, point1[:,4], '-', label='Roll1')
# ax.plot(num, point1[:,5], '-', label='Pitch1')
# ax.plot(num, point1[:,6], '-', label='Yaw1')
ax.plot(num/20, romAngle, '-', label='ROM')

ax.legend()

ax.set_xlabel('Times(s)')
ax.set_ylabel('Angle(deg)')
ax.set_title('Angle ROM')


x1, y1 = [0, num[-1]/20], [minYawRom, minYawRom]
x2, y2 = [0, num[-1]/20], [maxYawRom, maxYawRom]
x3, y3 = [0, num[-1]/20], [minYawRom+robotAngle, minYawRom+robotAngle]
plt.plot(x1, y1, '--', label='Base')
plt.plot(x2, y2, '--', label='Max')
# plt.plot(x3, y3, '--', label='True')
plt.legend()

plt.show()
