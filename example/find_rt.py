from matplotlib import projections
from numpy import *
from math import sqrt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *

if __name__ == '__main__':
        R = mat(random.rand(3,3))
        t = mat(random.rand(3,1))
        print("rt:\n",R,t)

        U,S,Vt = linalg.svd(R)
        R = U * Vt
        if linalg.det(R) < 0:
                Vt[2, :] *= -1
                R = U * Vt
        
        n = 5

        A = mat(random.rand(n,3))
        print("point A\n", A, "\n")
        B = R * A.T + tile(t,(1,n))
        B = B.T

        ret_R, ret_t = rigid_transform_3D(A,B)
        print("rt:\n",ret_R,ret_t)
        A2 = (ret_R * A.T) + tile(ret_t, (1,n))
        A2 = A2.T

        err = A2 - B
        err = multiply(err,err)
        err = sum(err)
        rmse = sqrt(err/n)
        
        print("point A2\n", A2, "\n")
        print("point B\n", B, "\n")
        print("rmse", rmse)

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(A[:,0],A[:,1],A[:,2])
        ax.scatter(B[:,0],B[:,1],B[:,2],s=100,marker='x')
        ax.scatter(A2[:,0],A2[:,1],A2[:,2],s=100,marker='o')
        # ax.legend()
        plt.show()