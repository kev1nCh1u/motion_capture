import time
from itertools import *

from matplotlib.pyplot import pause

num = range(8)
count = 0

start_time = time.time()
for i in range(4):
    for j in range(i+1,8):
        for k in range(j+1,8):
            for x in range(k+1,8):
                count += 1
                print(count,i,j,k,x)
print(count)
print("--- total %s seconds ---" % (time.time() - start_time))

start_time = time.time()
numPermutations = list(permutations(num,4))
print(len(numPermutations))
print("--- total %s seconds ---" % (time.time() - start_time))

start_time = time.time()
numCombinations = list(combinations(num,4))
print(len(numCombinations))
print("--- total %s seconds ---" % (time.time() - start_time))
