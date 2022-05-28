import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *

###################################################################################
# if main
###################################################################################
# generate point
gbp = GenBasePoint()
gbp.genBodyPoint()
basePoint2d = np.array([gbp.a,gbp.b,gbp.c,gbp.d])
print("base 2d point:\n", basePoint2d, "\n")

# axisDis
axisLen = 50
axisPoint = np.array([[axisLen,0.,0.],[0.,axisLen,0.],[0.,0.,axisLen]])
axisDis = findAxisDis(basePoint2d, axisPoint)
print("axis dis:\n", axisDis, "\n")

# gen axis point
gp = GenPoint()
gp.a = basePoint2d[0]
gp.b = basePoint2d[1]
gp.c = basePoint2d[2]
axisPoint = np.zeros((4,3))
axisDisSort = np.delete(axisDis, 3, axis=1)
print("axisDisSort:\n",axisDisSort, "\n")
for i in range(3):
    gp.dis = axisDisSort[i]
    axisPoint[i+1] = gp.solve_fsolve()
print("axisPoint:\n", axisPoint, "\n")

# showPlot3d
showPlot3d(basePoint2d, axisPoint, range(4), 4, 0)