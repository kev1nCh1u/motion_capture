import sys
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
import scipy as sp

from scipy.optimize import fsolve
from math import *

###############################################################################################
# stereoRemap remap
###############################################################################################
def stereoRemap(stereoMapL_x, stereoMapL_y, stereoMapR_x, stereoMapR_y, frameL, frameR):
    # Undistort and rectify images
    undistortedL = cv2.remap(
        frameL, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    undistortedR = cv2.remap(
        frameR, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    return undistortedL, undistortedR

###############################################################################################
# find_depth
###############################################################################################
def find_depth(left_point, right_point, baseline, focal):
    x_left = left_point[0] # x point
    x_right = right_point[0]

    # displacement between left and right frames [pixels]
    disparity = abs(x_left - x_right)
    zDepth = (baseline * focal) / disparity # z depth in [mm]

    return zDepth

###############################################################################################
# calcu_world_point
###############################################################################################
def calcu_world_point(point, z_depth, focal):
    world_points = np.zeros((3), np.float)
    x_cam = point[0]
    y_cam = point[1]
    world_points[0] = (x_cam * z_depth) / focal
    world_points[1] = (y_cam * z_depth) / focal
    world_points[2] = z_depth
    return world_points

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
def euclideanDistances3d(a ,b):
    # distance = ((a[0] - b[0])**2 # x
    #         + (a[1] - b[1])**2 # y
    #         + (a[2] - b[2])**2)**0.5 #z
    distance = np.sqrt(np.sum((a - b) ** 2))
    return distance

###################################################################################
# pointCount
###################################################################################
def pointCount(points3d):
    res = 4
    for i in range(len(points3d)):
        if(points3d[i][0] == 0):
            res -= 1
    return res

###################################################################################
# findPointDis
###################################################################################
def findPointDis(points3d, num, flag=0):
    distance = np.zeros((len(points3d)), np.float64)

    for i in range(len(points3d)):
        if(i != num):
            if((points3d[num][0] != 0 and points3d[i][0] != 0) or flag):
                distance[i] = euclideanDistances3d(points3d[num], points3d[i])

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
    ans = np.zeros((1,4), np.float64)

    # for i in range(4):
    #     for j in range(4):
    #         ans[i] += a[i][j]

    for i in range(4):
        ans[0][i] = np.sum(a[i])

    return ans

###################################################################################
# arraySumPart3
###################################################################################
def arraySumPart3(a):
    ans = np.zeros((4,4), np.float64)

    for i in range(4):
        for j in range(4):
            for k in range(4):
                if(k != i and j != i):
                    ans[i][j] += a[j][k]

    return ans

###################################################################################
# findCloseNum
###################################################################################
def findCloseNum(num, array):
    res = 0
    error = sys.maxsize
    for i in range(len(array)):
        errorNow = abs(num - array[i])
        if(error > errorNow):
            error = errorNow
            res = i
    return res

###################################################################################
# findPoint_sumThres
###################################################################################
def findPoint_sumThres(pointDisSum, orginDisSumTable):
    for i in range(len(orginDisSumTable)):
        if(abs(pointDisSum - orginDisSumTable[i]) < 2):
            return i+1
    return 0

###################################################################################
# findPoint_sumClose
###################################################################################
def findPoint_sumClose(pointDisSum, orginDisSumTable, tableNum):
    if(pointDisSum == 0):
        return (0,0)
    res = (0,0)
    error = sys.maxsize
    # for i in range(len(orginDisSumTable)):
    #     for j in range(len(orginDisSumTable[0])):
    #         errorNow = abs(pointDisSum - orginDisSumTable[i][j])
    #         if(error > errorNow):
    #             error = errorNow
    #             res = (i,j+1)
    for i in range(len(orginDisSumTable[tableNum])):
        errorNow = abs(pointDisSum - orginDisSumTable[tableNum][i])
        if(error > errorNow):
            error = errorNow
            res = (tableNum, i+1)
    return res

###################################################################################
# findBody_sum
###################################################################################
def findBody_sum(pointDisSum, orginDisSumTable, tableNum):
    nums = np.zeros((4,2), np.int8)
    for i in range(len(pointDisSum)):
        nums[i] = findPoint_sumClose(pointDisSum[i], orginDisSumTable, tableNum)
    return nums

###################################################################################
# findBody_num
###################################################################################
def findBody_num(pointDis, pointDisSum, orginDis, orginDisSumTable, basePoint):
    num = findPoint_sumClose(pointDisSum[basePoint], orginDisSumTable)[1]
    num = num - 1

    pointDis = pointDis[basePoint]
    print(pointDis)
    nums = np.zeros((len(pointDis)), np.int8)
    if(num >= 0):
        for i in range(4):
            for j in range(4):
                if(abs(pointDis[i] - orginDis[num][j]) < 1):
                    nums[i] = j + 1
    return nums

###################################################################################
# findBody_np
###################################################################################
def findBody_np(pointDis, orginDis, basePoint):
    pointDis = pointDis[basePoint]
    nums = np.zeros((len(pointDis)), np.int8)
    point = np.zeros((4,2,2), np.int8)
    pointDisId = np.zeros((4), np.int8)

    count = 0
    for i in range(len(pointDis)):
        where = np.copy(orginDis)
        if(pointDis[i]):
            where = np.where(where < pointDis[i]+1, where, 0)
            where = np.where(where > pointDis[i]-1, where, 0)
            point[count] = np.nonzero(where)
            pointDisId[count] = i
            count += 1
    
    num = -1
    for i in range(2):
        for j in range(2):
            if(point[0][i][0] == point[1][j][0]):
                num = point[0][i][0]
                
                nums[pointDisId[0]] = point[0][i][1] + 1
                nums[pointDisId[1]] = point[1][j][1] + 1
                
                for k in range(2):
                    if(point[2][k][0] == num):
                        nums[pointDisId[2]] = point[2][k][1] + 1
                        break

                break
    nums[basePoint] = num + 1

    return nums

###################################################################################
# pointErrorArray
###################################################################################
def pointErrorArray(true, observed, pointNums, pointCount):
    res = np.zeros(4, np.float32)
    tableNum = pointNums[0][0]
    for i in range(4):
        res[i] = (true[tableNum][pointNums[i][1]-1] - observed[i]) / pointCount
    return res

###################################################################################
# percentError
###################################################################################
def percentError(true, observed):
    if(observed == 0):
        return 100
    return abs(true-observed) / true * 100

###################################################################################
# percentReliability
###################################################################################
def percentReliability(true, observed):
    # return (true/abs(true-observed))/true * 100
    return 100 - percentError(true, observed)

###################################################################################
# percentReliabilityArray
###################################################################################
def percentReliabilityArray(true, observed, pointNums, half=0):
    res = np.zeros(4, np.float32)
    tableNum = pointNums[0][0]
    for i in range(4):
        res[i] = 100 - percentError(true[tableNum][pointNums[i][1]-1], observed[i])
        if(half and res[i] > 0):
            res[i] -= 50
    return res

###################################################################################
# percentReliabilityPoint
###################################################################################
def percentReliabilityPoint(true, points3d, num):
    observed = np.sum(findPointDis(points3d, num))
    # print("observed dis:", observed)
    res = 100 - percentError(true, observed)
    return res

###################################################################################
# findBodySwith
###################################################################################
class FindBody():
    orginDis = []
    orginDisSumTable4 = []
    orginDisSumTable3 = []
    orginDisSumTableList4 = []
    orginDisSumTableList3 = []
    
    def findBodySwith(self, pointDisSum, pointCount):
        flag = 0
        tableNum = 0
        if(pointCount == 4):
            orginDisSumTable = self.orginDisSumTable4
            orginDisSumTableList = self.orginDisSumTableList4
        elif(pointCount == 3):
            orginDisSumTable = self.orginDisSumTable3
            orginDisSumTableList = self.orginDisSumTableList3
            tableNum = findCloseNum(np.sum(pointDisSum), orginDisSumTableList)
        elif(pointCount == 2):
            orginDisSumTable = self.orginDis
            flag = 1
        else:
            orginDisSumTable = self.orginDis
        print("tableNum: ", tableNum, "\n")
        # print("orginDisSumTable: \n", orginDisSumTable, "\n")

        # findBody_sum
        nums = findBody_sum(pointDisSum, orginDisSumTable, tableNum)
        print("points nums:\n", nums, "\n")

        # Reliability
        pra = percentReliabilityArray(orginDisSumTable, pointDisSum, nums, flag)
        print("percentReliabilityArray", pra, "\n")

        pea = pointErrorArray(orginDisSumTable, pointDisSum, nums, pointCount)
        print("pointError", pea, "\n")

        return nums, pra, pea
        

###################################################################################
# GenPoint
###################################################################################
class GenPoint():
    a = []
    b = []
    c = []
    dis = []

    def solve_func(self,unsolve_value):
        x,y,z = unsolve_value[0],unsolve_value[1],unsolve_value[2]

        return [
            (x-self.a[0])**2 + (y-self.a[1])**2 + (z-self.a[2])**2 - self.dis[0]**2,
            (x-self.b[0])**2 + (y-self.b[1])**2 + (z-self.b[2])**2 - self.dis[1]**2,
            (x-self.c[0])**2 + (y-self.c[1])**2 + (z-self.c[2])**2 - self.dis[2]**2,
        ]

    def solve_fsolve(self):
        return fsolve(self.solve_func,[0,0,0])

###################################################################################
# GenPoint2d
###################################################################################
class GenPoint2d():
    dis = np.array([[0., 79.41495679, 92.6760091, 60.54557344],
                    [79.41495679, 0., 55.3985338, 82.12350075],
                    [92.6760091, 55.3985338, 0., 54.1674151 ],
                    [60.54557344, 82.12350075, 54.1674151, 0.],])
    
    a = []
    b = []
    c = []
    d = []

    # gen point c
    def solve_func_c(self,unsolve_value):
        x,y = unsolve_value[0],unsolve_value[1]

        return [
            (x-self.a[0])**2 + (y-self.a[1])**2 - self.dis[0][2]**2,
            (x-self.b[0])**2 + (y-self.b[1])**2 - self.dis[1][2]**2,
        ]
    def solve_fsolve_c(self):
        return fsolve(self.solve_func_c,[0,0])

    # gen point d
    def solve_func_d(self,unsolve_value):
        x,y = unsolve_value[0],unsolve_value[1]

        return [
            (x-self.a[0])**2 + (y-self.a[1])**2 - self.dis[0][3]**2,
            (x-self.b[0])**2 + (y-self.b[1])**2 - self.dis[1][3]**2,
        ]
    def solve_fsolve_d(self):
        return fsolve(self.solve_func_d,[0,0])

    # genBodyPoint
    def genBodyPoint(self):
        self.a = np.array([0.,0.,0.])
        self.b = np.array([0.,self.dis[0][1],0.])
        self.c = np.append(self.solve_fsolve_c(), np.zeros(1), axis=0)
        self.d = np.append(self.solve_fsolve_d(), np.zeros(1), axis=0)

###################################################################################
# findAxisDis
###################################################################################
def findAxisDis(point3d, inputAxisPoint=0):
    axisLen = 50
    axisPoint = np.array([[axisLen,0.,0.],[0.,axisLen,0.],[0.,0.,axisLen]])
    if(np.size(inputAxisPoint) == 9):
        axisPoint = inputAxisPoint
    axisDis = np.zeros((3,4))
    for i in range(4):
        axisDis[0][i] = euclideanDistances3d(axisPoint[0],point3d[i])
        axisDis[1][i] = euclideanDistances3d(axisPoint[1],point3d[i])
        axisDis[2][i] = euclideanDistances3d(axisPoint[2],point3d[i])
    return axisDis

###################################################################################
# rotationToEuler
###################################################################################
def rotationToEuler(R):
    sy = sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
    singular = sy < 1e-6

    if not singular:
        x = atan2(R[2,1], R[2,2])
        y = atan2(-R[2,0], sy)
        z = atan2(R[1,0], R[0,0])
    else:
        x = atan2(-R[1,2], R[1,1])
        y = atan2(-R[2,0], sy)
        z = 0

    return np.array([x,y,z])


###################################################################################
# show plot 3d
###################################################################################
def showPlot3d(points3d, axisPoint, order, pointCount, baseNum=0):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # ax.set_xlim(-100,100)
    # ax.set_ylim(-100,100)
    # ax.set_zlim(400,500)
    ax.scatter(points3d[:,0], points3d[:,1], points3d[:,2], label='points')
    if(pointCount >= 3):
        ax.scatter(axisPoint[0,0], axisPoint[0,1], axisPoint[0,2], label='x', c="red")
        ax.scatter(axisPoint[1,0], axisPoint[1,1], axisPoint[1,2], label='y', c="green")
        ax.scatter(axisPoint[2,0], axisPoint[2,1], axisPoint[2,2], label='z', c="blue")
        xline = np.array([points3d[order[0],0], points3d[order[2],0]])
        yline = np.array([points3d[order[0],1], points3d[order[2],1]])
        zline = np.array([points3d[order[0],2], points3d[order[2],2]])
        ax.plot3D(xline, yline, zline, 'gray')
        xline = np.array([points3d[order[1],0], points3d[order[3],0]])
        yline = np.array([points3d[order[1],1], points3d[order[3],1]])
        zline = np.array([points3d[order[1],2], points3d[order[3],2]])
        ax.plot3D(xline, yline, zline, 'gray')
        xline = np.array([points3d[baseNum,0], axisPoint[0,0]])
        yline = np.array([points3d[baseNum,1], axisPoint[0,1]])
        zline = np.array([points3d[baseNum,2], axisPoint[0,2]])
        ax.plot3D(xline, yline, zline, 'red')
        xline = np.array([points3d[baseNum,0], axisPoint[1,0]])
        yline = np.array([points3d[baseNum,1], axisPoint[1,1]])
        zline = np.array([points3d[baseNum,2], axisPoint[1,2]])
        ax.plot3D(xline, yline, zline, 'green')
        xline = np.array([points3d[baseNum,0], axisPoint[2,0]])
        yline = np.array([points3d[baseNum,1], axisPoint[2,1]])
        zline = np.array([points3d[baseNum,2], axisPoint[2,2]])
        ax.plot3D(xline, yline, zline, 'blue')
    ax.legend()
    plt.show()

###################################################################################
# findWorstPoint
###################################################################################
def findWorstPoint(percentReliabilityArray, numSize=4):
    res = 0
    min = 100
    for i in range(numSize):
        if(percentReliabilityArray[i] < min):
            min = percentReliabilityArray[i]
            res = i
    return res

###################################################################################
# if main
###################################################################################
if __name__ == '__main__':

    print("welcome kevin_cv...\n")

    



   
