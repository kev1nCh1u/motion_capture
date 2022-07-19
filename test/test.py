
import numpy as np

# a = [[1,0,1], [0,1,2], [0,1,2]]
a = np.random.random(27)
a = np.reshape(a,(9,3))
print("a",a)

b = np.random.random(3)
b = np.reshape(b,(3,1))
print("b",b)

# c = np.dot(a, b)
# print("c",c)

c = np.random.random(9)
c = np.reshape(c,(9,1))
print("c",c)

# bs = np.dot(a, c)
# print("bs",bs)

# ainv = np.linalg.inv(a)
# bs = np.dot(ainv,c)
# print("bs",bs)

bs = np.linalg.lstsq(a,c, rcond=None)[0]

print("bs",bs)

# (k_inferred, m0_inferred), residuals, rank, s = np.linalg.lstsq(a, c)
# print((k_inferred, m0_inferred))