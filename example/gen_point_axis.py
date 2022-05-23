import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *

###################################################################################
# if main
###################################################################################
# generate point
gp2d = GenPoint2d()
gp2d.genBodyPoint()
virtualPoint3d = np.array([gp2d.a,gp2d.b,gp2d.c,gp2d.d])
print("virtual 3d point:\n", virtualPoint3d, "\n")

# axisDis
axisLen = 50
axisPoint = np.array([[axisLen,0.,0.],[0.,axisLen,0.],[0.,0.,axisLen]])
axisDis = findAxisDis(virtualPoint3d, axisPoint)
print("axis dis:\n", axisDis, "\n")

# gen axis point
gp = GenPoint()
gp.a = virtualPoint3d[0]
gp.b = virtualPoint3d[1]
gp.c = virtualPoint3d[2]
axisPoint = np.zeros((3,3))
axisDisSort = np.delete(axisDis, 3, axis=1)
print("axisDisSort:\n",axisDisSort, "\n")
for i in range(3):
    gp.dis = axisDisSort[i]
    axisPoint[i] = gp.solve_fsolve()
print("axisPoint:\n", axisPoint, "\n")

# showPlot3d
showPlot3d(virtualPoint3d, axisPoint, range(4), 4, 0)