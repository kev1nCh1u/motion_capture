import os
import sys

from numpy import ndarray
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *

import math
import pandas as pd

# from matplotlib import pyplot as plt

###################################################################################
# main
###################################################################################
def main():
    print("find body...\n")

    ########################################## load yaml param
    fs = cv2.FileStorage(
    "data/parameter/marker_body.yaml", cv2.FILE_STORAGE_READ)
    orginDis = fs.getNode("orginDistance").mat()
    orginPoint = fs.getNode("orginPoint").mat()
    points3d = fs.getNode("testPoint").mat()
    # print("orginDis:",orginDis)

    ########################################## load point data
    path = "data/result/point_data.csv"
    df = pd.read_csv(path, header=None)
    point_data = df.to_numpy()

    ########################################## open point error data
    fileErrData = open("data/result/point_error_data.csv", "w")

    ########################################## orgin
    orginDis = findAllDis(orginPoint)
    orginDisSumTable4 = arraySum(orginDis)
    orginDisSumTable3 = arraySumPart3(orginDis)
    orginDisSumTableList3 = np.zeros(4)
    for i in range(4):
        orginDisSumTableList3[i] = np.sum(orginDisSumTable3[i,:])

    # set find body
    fb = FindBody()
    fb.orginDis = orginDis
    fb.orginDisSumTable4 = orginDisSumTable4
    fb.orginDisSumTable3 = orginDisSumTable3
    fb.orginDisSumTableList3 = orginDisSumTableList3

    # gen base point
    gbp = GenBasePoint()
    gbp.genBodyPoint()
    gbp.dis = orginDis
    basePoint2d = np.array([gbp.a,gbp.b,gbp.c,gbp.d])
    axisLen = 50
    baseAxisPoint2d = np.array([[0.,0.,0.],[axisLen,0.,0.],[0.,axisLen,0.],[0.,0.,axisLen]])

    # axisDis
    axisDis = findAxisDis(basePoint2d)
    print("axis dis:\n", axisDis, "\n")

    start_time_1 = time.time()
    for i in range(len(point_data[:])):
        print("==========================================================================================")

        ########################################## load point data
        points3d[2] = point_data[i,0:3]
        points3d[1] = point_data[i,3:6]
        points3d[3] = point_data[i,6:9]
        # points3d[0] = point_data[i,9:12]
        points3d[0] = [0,0,0]
        print("points3d:\n", points3d)

        ########################################## point
        pc = pointCount(points3d)
        pointDis = findAllDis(points3d)
        pointDisSum = arraySum(pointDis)[0]
        print("pointCount:", pc, "\n")
        # print("points distanse:\n", pointDis, "\n")
        # print("points distanse sum:\n",pointDisSum, "\n")

        # find body in any case
        nums, pra, pea = fb.findBodySwith(pointDisSum, pc)
        print("nums:\n", nums, "\n")

        # write err data
        text = ""
        for i in range(4):
            text += str(pea[i]) + ', '
        text += '\n'
        fileErrData.write(text) # write

        # numsSort
        numsSort = np.append(nums, np.arange(4).reshape((4, 1)), axis=1)
        numsSort = np.sort(numsSort.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int64)
        print("numsSort:\n", numsSort, "\n")

        # worstPoint
        worstPoint = 0
        if(pc == 4):
            worstPoint = findWorstPoint(pra)

        # generate lost point
        if(pc == 3):
            worstPoint = numsSort[1][0]
            gp = GenPoint()
            gp.a = points3d[numsSort[1][2]]
            gp.b = points3d[numsSort[2][2]]
            gp.c = points3d[numsSort[3][2]]
            gp.dis = np.delete(orginDis[nums[0][0]], nums[0][0], None)
            lp = gp.solve_fsolve()
            print("generate lost point:\n", lp, "\n")
            points3d[numsSort[0][2]] = lp
            print("new 3d points:\n", points3d, "\n")

            # Reliability point
            prp = percentReliabilityPoint(orginDisSumTable4[0][numsSort[1][0]], points3d, numsSort[0][2])
            print("Reliability: ", prp, "\n")

            # new numsSort
            numsSort[0][1] = numsSort[1][0] + 1
            numsSort = np.sort(numsSort.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int64)
            print("new numsSort:\n", numsSort, "\n")

        # worstPoint
        print("worstPoint", worstPoint, "\n")

        # create gen axis point
        numList = [i for i in range(4) if i != worstPoint]
        gp = GenPoint()
        gp.a = points3d[numsSort[numList[0]][2]]
        gp.b = points3d[numsSort[numList[1]][2]]
        gp.c = points3d[numsSort[numList[2]][2]]

        # points3dSort
        points3dSort = np.zeros((4,3))
        for i in range(4):
            points3dSort[i] = points3d[numsSort[i][2]]
        
        # part
        basePoint2dPart = np.delete(basePoint2d, worstPoint, axis=0)
        points3dSortPart = np.delete(points3dSort, worstPoint, axis=0)
        print("basePoint2dPart",basePoint2dPart)
        print("points3dSortPart",points3dSortPart)

        # find axis point rt
        ret_R, ret_t = rigid_transform_3D(np.asmatrix(basePoint2dPart),np.asmatrix(points3dSortPart))
        axisPoint = (ret_R * np.asmatrix(baseAxisPoint2d).T) + np.tile(ret_t, (1,4))
        axisPoint = axisPoint.T

        # axisPointDis
        axisPointDis = np.zeros((3,3))
        for i in range(3):
            axisPointDis[i] = axisPoint[i] - points3d[numsSort[0][2]]
        axisPointDis = axisPointDis / 50

        # find axis angle
        angle = rotationToEuler(axisPointDis)
        print("angle rad: \n", angle)
        print("angle deg: \n", np.rad2deg(angle))

        # showPlot3d
        showPlot3d(points3d, axisPoint, numsSort[:,2], pc, numsSort[0][2])

    fileErrData.close()

    # time
    print("\n--- 1: %s seconds ---" % (time.time() - start_time_1))

###################################################################################
# if main
###################################################################################
if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("\n--- total %s seconds ---" % (time.time() - start_time))