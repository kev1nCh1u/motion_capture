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

    ########################################## load point_data
    path = "data/result/point_data_distance.csv"
    df = pd.read_csv(path, header=None)
    point_data = df.to_numpy()

    ########################################## open point_result
    fileErrData = open("data/result/point_result.csv", "w")
    text = "dis, relia, err0, err1, err2, err3, angle0, angle1, angle2,\n"
    fileErrData.write(text) # write

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
        points3d[1] = point_data[i,0:3]
        points3d[2] = point_data[i,3:6]
        points3d[0] = point_data[i,6:9]
        # points3d[1] = point_data[i,9:12]
        points3d[3] = [0,0,0]
        # points3d[0] = [0,0,0]
        # points3d[2] = [0,0,0]
        print("points3d:\n", points3d)

        ########################################## point
        pc = pointCount(points3d)
        pointDis = findAllDis(points3d)
        pointDisSum = arraySum(pointDis)[0]
        # print("pointCount:", pc, "\n")
        # print("points distanse:\n", pointDis, "\n")
        # print("points distanse sum:\n",pointDisSum, "\n")

        # find body in any case
        nums, reliability, error = fb.findBodySwith(pointDisSum, pc)
        print("nums:\n", nums)
        print("reliability:\n", reliability)
        print("error:\n", error)

        # numsSort
        numsSort = np.append(nums, np.arange(4).reshape((4, 1)), axis=1)
        numsSort = np.sort(numsSort.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int64)
        # print("numsSort:\n", numsSort, "\n")

        # worstPoint
        worstPoint = findWorstPoint(reliability)
        worstPointId = nums[worstPoint][1]
        print("worstPoint:", worstPoint, "id:", worstPointId)
        
        # points3dSort
        points3dSort = np.zeros((4,3))
        for i in range(4):
            points3dSort[i] = points3d[numsSort[i][2]]

        # part
        orginPointPart = np.delete(orginPoint, worstPointId-1, axis=0)
        points3dSortPart = np.delete(points3dSort, worstPointId-1, axis=0)
        basePoint2dPart = np.delete(basePoint2d, worstPointId-1, axis=0)
        # print("orginPointPart",orginPointPart)
        # print("points3dSortPart",points3dSortPart)

        # generate lost point rt
        if(pc == 3):
            ret_R, ret_t = rigid_transform_3D(np.asmatrix(orginPointPart),np.asmatrix(points3dSortPart))
            genPoint = (ret_R * np.asmatrix(orginPoint[worstPointId-1]).T) + np.tile(ret_t, (1,1))
            genPoint = genPoint.T
            points3d[worstPoint] = genPoint
            print("gen point: ", genPoint)

            # Reliability point
            prp = percentReliabilityPoint(orginDisSumTable4[0][numsSort[1][0]], points3d, numsSort[0][2])
            print("reliability: ", prp)
        
        # find axis point rt
        ret_R, ret_t = rigid_transform_3D(np.asmatrix(basePoint2dPart),np.asmatrix(points3dSortPart))
        axisPoint = (ret_R * np.asmatrix(baseAxisPoint2d).T) + np.tile(ret_t, (1,4))
        axisPoint = axisPoint.T
        print(axisPoint)

        # axisPointDis
        axisPointDis = np.zeros((3,3))
        for i in range(3):
            # axisPointDis[i] = axisPoint[i] - points3d[numsSort[0][2]]
            axisPointDis[i] = axisPoint[i+1] - axisPoint[0]
        axisPointDis = axisPointDis / 50
        print(axisPointDis)

        # find axis angle
        angle = rotationToEuler(axisPointDis)
        print("angle rad: \n", angle)
        angleDeg = np.rad2deg(angle)
        print("angle deg: \n", angleDeg)

        # write err data
        text = str(points3d[0][2]) + ", " + str(reliability[0]) + ", "
        for i in range(4):
            text += str(error[i]) + ', '
        for i in range(3):
            text += str(angleDeg[i]) + ', '
        text += '\n'
        fileErrData.write(text) # write

        # showPlot3d
        # print("points3d\n",points3d)
        # print("points3dSort\n",points3dSort)
        # showPlot3d(points3d, axisPoint, numsSort[:,2], pc, numsSort[0][2])

        # exit()

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