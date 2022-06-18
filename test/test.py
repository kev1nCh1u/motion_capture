
import numpy as np

import numpy as np

arr = np.array([41, 42, 43, 44])

filter_arr = arr > 42

newarr = arr[filter_arr]

print(filter_arr)
print(newarr)

from scipy.spatial.transform import Rotation as R

r = R.from_rotvec([0, 0, np.pi/2])
print(r.as_euler('zxy', degrees=True))

r = R.from_rotvec([
[0, 0, np.pi/2],
[0, -np.pi/3, 0],
[np.pi/4, 0, 0]])

print(r.as_euler('zxy', degrees=True))