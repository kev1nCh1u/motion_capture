from matplotlib import pyplot as plt
import pandas as pd

import numpy as np

df = pd.read_csv("data/result/point_main.csv", header=0)
point = df.to_numpy()
# print(point[0])

# point = point[3:-7]
point = point[::100]

######################################################################
# show angle
######################################################################
num = np.arange(len(point[:,6]))
true = num * 10 + point[0,7]

fig, ax = plt.subplots()

# ax.plot(num, true, '-.', label='True')
ax.plot(num, point[:,4], 'o-', label='Roll')
ax.plot(num, point[:,5], '--^', label='Pitch')
ax.plot(num, point[:,6], '-+', label='Yaw')

ax.legend()

ax.set_xlabel('Number')
ax.set_ylabel('Angle')
ax.set_title('Angle test')
plt.show()
