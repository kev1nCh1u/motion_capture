import time
from itertools import *
import numpy as np

num = range(8)
count = 0

start_time = time.time()
for i in range(8):
    for j in range(i+1,8):
        for k in range(j+1,8):
            for x in range(k+1,8):
                count += 1
                # print(count,i,j,k,x)
print(count)
print("--- total %s seconds ---" % (time.time() - start_time))

start_time = time.time()
numPermutations = list(permutations(num,4))
print(len(numPermutations))
print("--- total %s seconds ---" % (time.time() - start_time))

start_time = time.time()
numCombinations = list(combinations(num,4))
print(len(numCombinations))

# print(np.sum(numCombinations[0]))
# print(np.sum(numCombinations,1))

print("--- total %s seconds ---" % (time.time() - start_time)) 