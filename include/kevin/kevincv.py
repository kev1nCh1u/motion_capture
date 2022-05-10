import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import time
import argparse

###################################################################################
# triangulate
###################################################################################
def triangulate(cameraMatrix1, cameraMatrix2, RotationOfCamera2, TranslationOfCamera2, point_x, point_x_):
    # p
    k = cameraMatrix1
    rt =  np.eye(3,4)
    p = np.dot(k, rt)

    # pp
    k_ = cameraMatrix2
    rt_ = np.concatenate((RotationOfCamera2, TranslationOfCamera2), axis=1)
    p_ = np.dot(k_, rt_)
    
    # point
    u = point_x[0]
    v = point_x[1]
    u_ = point_x_[0]
    v_ = point_x_[1]
    # print("uv:", u, v, u_, v_)

    # equations
    A = np.array([
        u * p[2] - p[0],
        v * p[2] - p[1],
        u_ * p_[2] - p_[0],
        v_ * p_[2] - p_[1]], dtype='float64'
    )

    # svd
    U, S, V = np.linalg.svd(A)
    X = V.transpose()[:, -1]
    # print("X:", X)
    X = X / X[3]
    # print("world_point:", X)
    return X[0:3]

###################################################################################
# euclideanDistances3d
###################################################################################
def euclideanDistances3d(world_points):
    distance = ((world_points[0, 0] - world_points[1, 0])**2 # x
        + (world_points[0, 1] - world_points[1, 1])**2 # y
        + (world_points[0, 2] - world_points[1, 2])**2)**0.5 #z
    return distance

###################################################################################
# euclideanDistances3d
###################################################################################
def euclideanDistancesTwo3d(a ,b):
    distance = ((a[0] - b[0])**2 # x
            + (a[1] - b[1])**2 # y
            + (a[2] - b[2])**2)**0.5 #z
    return distance

###################################################################################
# findPointDis
###################################################################################
def findPointDis(points3d, num):
    distance = np.zeros((4), np.float64)

    for i in range(4):
        if(i != num):
            distance[i] = euclideanDistancesTwo3d(points3d[num], points3d[i])

    return distance

###################################################################################
# findAllDis
###################################################################################
def findAllDis(points3d):
    distance = np.zeros((4,4), np.float64)

    for i in range(4):
        distance[i] = findPointDis(points3d, i)

    return distance

###################################################################################
# arraySum
###################################################################################
def arraySum(a):
    ans = np.zeros((4), np.float64)

    # for i in range(4):
    #     for j in range(4):
    #         ans[i] += a[i][j]

    for i in range(4):
        ans[i] = np.sum(a[i])

    return ans

###################################################################################
# findBodyPoint
###################################################################################
def findBodyPoint(point, orgin):
    for i in range(4):
        if(abs(point - orgin[i]) < 1):
            return i

    return -1

###################################################################################
# findBodyPointAll
###################################################################################
def findBodyPointAll(point, orgin):
    nums = np.zeros((4), np.float64)

    for i in range(4):
        for j in range(4):
            if(abs(point[i] - orgin[j]) < 1):
                nums[i] = j

    return nums



# if main
if __name__ == '__main__':
    print("welcome kevin_cv...\n")

    origin  = np.array([
                        [86.50438840372979, 0.6729383451448048, 474.92717314288876],
                        [14.414906327500171, 22.34505201771049, 449.62576160776894],
                        [96.13160683183148, 55.10663416683474, 478.5723029681971],
                        [47.43867422337718, 71.66474800800661, 461.57418427997044],
                        ])

    points3d  = np.array([
                        [44.408427247312176, 71.80456867683641, 471.56922565559825],
                        [84.0008849766173, 1.0253193717497644, 484.2133958228639],
                        [11.402377138005159, 22.452479238189188, 458.8405626214418],
                        [93.7861030447076, 55.47613355449325, 487.92861245647583],
                        ])

    orgDis = findAllDis(origin)
    print("origin distanse:\n", orgDis, "\n")
    orgSum = arraySum(orgDis)
    print("origin distanse sum:\n",orgSum, "\n")

    while 1:
        pointDis = findPointDis(points3d, 1)
        print("point distance:", pointDis)
        pointSum = np.sum(pointDis)
        print("point sum", pointSum)
        
        num = findBodyPoint(pointSum, orgSum)
        print("point num:",num)

        nums = findBodyPointAll(pointDis, orgDis[num])
        print("points num:", nums)

        exit()
   
