import numpy as np

a = np.random.uniform(size=(5,5))
print(a)
b = np.rot90(np.fliplr(a))
print(b)