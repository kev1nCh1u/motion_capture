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
point3d = np.array([gp2d.a,gp2d.b,gp2d.c,gp2d.d])
print("virtual 3d point:\n", point3d, "\n")

# axisDis
axisDis = findAxisDis(point3d)
print("axis dis:\n", axisDis, "\n")