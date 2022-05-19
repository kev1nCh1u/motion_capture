import sys
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
import time
import scipy as sp

from scipy.optimize import fsolve

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
def findPointDis(points3d, num):
    distance = np.zeros((len(points3d)), np.float64)

    for i in range(4):
        if(i != num and points3d[num][0] != 0 and points3d[i][0] != 0):
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
# findPoint_sumThres
###################################################################################
def findPoint_sum(pointDisSum, orginDisSumTable):
    for i in range(len(orginDisSumTable)):
        if(abs(pointDisSum - orginDisSumTable[i]) < 2):
            return i+1
    return 0

###################################################################################
# findPoint_sumClose
###################################################################################
def findPoint_sum(pointDisSum, orginDisSumTable):
    if(pointDisSum == 0):
        return 0
    res = 0
    error = sys.maxsize
    for i in range(len(orginDisSumTable)):
        for j in range(len(orginDisSumTable[0])):
            errorNow = abs(pointDisSum - orginDisSumTable[i][j])
            if(error > errorNow):
                error = errorNow
                res = (i,j+1)
    return res

###################################################################################
# findBody_sum
###################################################################################
def findBody_sum(pointDisSum, orginDisSumTable):
    nums = np.zeros((4,2), np.int8)
    for i in range(len(pointDisSum)):
        nums[i] = findPoint_sum(pointDisSum[i], orginDisSumTable)
    return nums

###################################################################################
# findBody_num
###################################################################################
# def findBody_num(pointDis, orginDis, num):
def findBody_num(pointDis, pointDisSum, orginDis, orginDisSumTable, basePoint):
    num = findPoint_sum(pointDisSum[basePoint], orginDisSumTable)[1]
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
# findBodySwith
###################################################################################
class FindBody():
    orginDis = []
    orginDisSumTable4 = []
    orginDisSumTable3 = []
    
    def findBodySwith(self, pointDisSum, pointCount):
        flag = 0
        if(pointCount == 4):
            orginDisSumTable = self.orginDisSumTable4
        elif(pointCount == 3):
            orginDisSumTable = self.orginDisSumTable3
        elif(pointCount == 2):
            orginDisSumTable = self.orginDis
            flag = 1
        else:
            orginDisSumTable = self.orginDis

        # findBody_sum
        nums = findBody_sum(pointDisSum, orginDisSumTable)
        print("points nums:\n", nums, "\n")

        # Reliability
        pra = percentReliabilityArray(orginDisSumTable, pointDisSum, nums, flag)
        print("percentReliabilityArray", pra, "\n")

        return nums
        
###################################################################################
# percentError
###################################################################################
def percentError(true, observed):
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
# SolvePoint
###################################################################################
class SolvePoint():
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
# test main
###################################################################################
def main():
    print("welcome kevin_cv...\n")

    origin  = np.array([
                        [14.414906327500171, 22.34505201771049, 449.62576160776894],
                        [86.50438840372979, 0.6729383451448048, 474.92717314288876],
                        [96.13160683183148, 55.10663416683474, 478.5723029681971],
                        [47.43867422337718, 71.66474800800661, 461.57418427997044],
                        ])

    orginDis  = np.array([
                        [0.,    79.,    93.,    61.],
                        [79.,   0.,     57.,    82.],
                        [93.,   57.,    0.,     54.],
                        [61.,   82.,    54.,    0.],      
                        ])

    points3d  = np.array([
                        [44.408427247312176, 71.80456867683641, 471.56922565559825],
                        [0, 0, 0],
                        [11.402377138005159, 22.452479238189188, 458.8405626214418],
                        [84.0008849766173, 1.0253193717497644, 484.2133958228639],
                        # [93.7861030447076, 55.47613355449325, 487.92861245647583],
                        # [0, 0, 0],
                        # [0, 0, 0],
                        # [0, 0, 0],
                        ])

    orginDis = findAllDis(origin)
    print("origin distanse:\n", orginDis, "\n")
    orginDisSumTable4 = arraySum(orginDis)
    print("orginDisSumTable4:\n",orginDisSumTable4, "\n")
    orginDisSumTable3 = arraySumPart3(orginDis)
    print("orginDisSumTable3:\n",orginDisSumTable3, "\n")

    FB = FindBody()
    FB.orginDis = orginDis
    FB.orginDisSumTable4 = orginDisSumTable4
    FB.orginDisSumTable3 = orginDisSumTable3

    for i in range(60):
        start_time_1 = time.time()

        pc = pointCount(points3d)
        # print("pointCount:\n", pc, "\n")

        basePoint = 3 - 1

        pointDis = findAllDis(points3d)
        # print("points distanse:\n", pointDis, "\n")
        pointDisSum = arraySum(pointDis)[0]
        print("points distanse sum:\n",pointDisSum, "\n")
        
        # # findBody_num
        # nums = findBody_num(pointDis, pointDisSum, orginDis, orginDisSumTable4, basePoint)
        # print("points nums:", nums, "\n")

        # # findBody_np
        # nums = findBody_np(pointDis, orginDis, basePoint)
        # print("points nums:", nums, "\n")

        # # findBody_sum
        # nums = findBody_sum(pointDisSum, orginDisSumTable3)
        # print("points nums:\n", nums, "\n")

        # # Reliability
        # pra = percentReliabilityArray(orginDisSumTable3, pointDisSum, nums)
        # print("percentReliabilityArray", pra, "\n")

        # find body in any case
        nums = FB.findBodySwith(pointDisSum, pc)

        # generate lost point
        SP = SolvePoint()
        numsSort = np.append(nums, np.arange(4).reshape((4, 1)), axis=1)
        numsSort = np.sort(numsSort.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int64)
        SP.a = points3d[numsSort[1][2]]
        SP.b = points3d[numsSort[2][2]]
        SP.c = points3d[numsSort[3][2]]
        SP.dis = np.delete(orginDis[nums[0][0]], nums[0][0], None)
        lp = SP.solve_fsolve()
        print("generate lost point:\n", lp, "\n")
        points3d[nums[0][0]-1] = lp
        print("new 3d points:\n", points3d, "\n")

        # Reliability
        observed = np.sum(findPointDis(points3d, nums[0][0]-1))
        pra = 100 - percentError(orginDisSumTable4[0][nums[0][0]-1], observed)
        print("Reliability: ", pra, "\n")

        # time
        print("--- 1: %s seconds ---" % (time.time() - start_time_1))

        break

###################################################################################
# if main
###################################################################################
if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("--- total %s seconds ---" % (time.time() - start_time))


   
