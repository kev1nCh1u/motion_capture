from matplotlib import projections
import numpy as np
from math import sqrt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import cv2
import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from lib.kevin import  kevincv

if __name__ == '__main__':

	# load path
	fs = cv2.FileStorage("src/robot_arm/robot_path.yaml", cv2.FILE_STORAGE_READ)
	path = fs.getNode("path").mat()
	path = path[:,0:3]
	print(path[0],path[1],path[3])
	path_size = len(path)

	# load data
	df = pd.read_csv("data/result/grid_point/point_main_grid_150.csv", header=0)
	point = df.to_numpy()
	# print(point[0])
	point = point[1:,1:4]
	point = point[::6]
	print(point[0], point[1], point[3])

	A = np.array((path[0],path[1],path[3]))
	# B = np.array((path[10],path[11],path[13]))
	B = np.array((point[1],point[2],point[4]))

	A = A*0.46
	# B = B*0.8

	ret_R, ret_t = kevincv.rigid_transform_3D(np.asmatrix(A),np.asmatrix(B))
	print("rt:\n",ret_R,ret_t)
	k = 0.1
	A2 = (ret_R * A.T) + np.tile(ret_t, (1,1))
	A2 = A2.T

	err = A2 - B
	err = np.multiply(err,err)
	err = np.sum(err)
	rmse = np.sqrt(err/1)

	print("point A2\n", A2, "\n")
	print("point B\n", B, "\n")
	print("rmse", rmse)

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	ax.scatter(A[:,0],A[:,1],A[:,2],label='A')
	ax.scatter(B[:,0],B[:,1],B[:,2],marker='x',label='B')
	ax.scatter(A2[:,0],A2[:,1],A2[:,2],marker='o',label='A2')
	ax.legend()
	plt.show()