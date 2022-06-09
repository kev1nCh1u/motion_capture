
import numpy as np

a = np.random.rand(10,4,3)
print(a)

b = np.median(a,axis=0)
print(b)