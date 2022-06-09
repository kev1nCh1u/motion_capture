import os
import sys
import time

from numpy import ndarray
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *

import math
import pandas as pd

# from matplotlib import pyplot as plt


class FindBody():
    def __init__(self, markerParam = "data/parameter/create_markers.yaml"):
        ########################################## load param and data
        # marker parameter
        fs = cv2.FileStorage(markerParam, cv2.FILE_STORAGE_READ)
        self.orginDis = fs.getNode("orginDistance0").mat()
        self.orginPoint = fs.getNode("orginPoint0").mat()
        # print("orginDis:",orginDis)

        # result data
        self.point_result = open("data/result/point_result.csv", "w")
        text = "dis, relia, err0, err1, err2, err3, angle0, angle1, angle2,\n"
        self.point_result.write(text) # write

        # sort data
        self.point_sdata = open("data/result/point_sdata.csv", "w")
        text = ""
        for i in range(4): text += "p" + str(i) + "x," + "p" + str(i) + "y," + "p" + str(i) + "z,"
        text += "\n"
        self.point_sdata.write(text) # write

        ########################################## orgin calculate
        self.orginDis = findAllDis(self.orginPoint)
        self.orginDisSumTable4 = arraySum(self.orginDis)
        self.orginDisSumTable3 = arraySumPart3(self.orginDis)
        self.orginDisSumTableList3 = np.zeros(4)
        for i in range(4):
            self.orginDisSumTableList3[i] = np.sum(self.orginDisSumTable3[i,:])
        
        print("orginDis",self.orginDis)
        print("orginDisSumTable4",self.orginDisSumTable4)

        #################################################### set find body
        self.fbi = FindBodyId()
        self.fbi.orginDis = self.orginDis
        self.fbi.orginDisSumTable4 = self.orginDisSumTable4
        self.fbi.orginDisSumTable3 = self.orginDisSumTable3
        self.fbi.orginDisSumTableList3 = self.orginDisSumTableList3

        ################################################### gen base point axis
        gbp = GenBasePoint()
        gbp.genBodyPoint()
        gbp.dis = self.orginDis
        self.basePoint2d = np.array([gbp.a,gbp.b,gbp.c,gbp.d])
        axisLen = 50
        self.baseAxisPoint2d = np.array([[0.,0.,0.],[axisLen,0.,0.],[0.,axisLen,0.],[0.,0.,axisLen]])

        axisDis = findAxisDis(self.basePoint2d)
        # print("axis dis:\n", axisDis, "\n")


    def findBody(self, points3d, showPlot=0):

        start_time_1 = time.time()

        print("orginDis",self.orginDis)
        print("orginDisSumTable4",self.orginDisSumTable4)

        ########################################## point calculate
        pc = pointCount(points3d)
        pointDis = findAllDis(points3d)
        pointDisSum = arraySum(pointDis)[0]
        print("pointCount:", pc, "\n")
        print("points distanse:\n", pointDis, "\n")
        print("points distanse sum:\n",pointDisSum, "\n")

        ############################# find body id
        nums, reliability, error = self.fbi.findBodyId(pointDis, pointDisSum, pc)
        print("nums:\n", nums)
        print("reliability:\n", reliability)
        print("error:\n", error)
        # exit()

        ############################## numsSort
        numsSort = np.append(nums, np.arange(4).reshape((4, 1)), axis=1)
        numsSort = np.sort(numsSort.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int64)
        # print("numsSort:\n", numsSort, "\n")

        ################################# worstPoint
        worstPoint = findWorstPoint(reliability)
        worstPointId = nums[worstPoint][1]
        print("worstPoint:", worstPoint, "id:", worstPointId)
        
        ############################## points3dSort
        points3dSort = np.zeros((4,3))
        for i in range(4):
            points3dSort[i] = points3d[numsSort[i][2]]

        ################################ error
        pointDisSort = findAllDis(points3dSort) 
        msePoint = mseFuc(pointDisSort, self.orginDis)
        print("msePoint:",msePoint)

        pointDisSort = findAllDis(points3dSort) 
        rmsePoint = rmseFuc(pointDisSort, self.orginDis)
        print("rmsePoint:",rmsePoint)

        ################################ part
        orginPointPart = np.delete(self.orginPoint, worstPointId-1, axis=0)
        points3dSortPart = np.delete(points3dSort, worstPointId-1, axis=0)
        basePoint2dPart = np.delete(self.basePoint2d, worstPointId-1, axis=0)
        # print("orginPointPart",orginPointPart)
        # print("points3dSortPart",points3dSortPart)

        ############################### generate lost point rt
        if(pc == 3):
            ret_R, ret_t = rigid_transform_3D(np.asmatrix(orginPointPart),np.asmatrix(points3dSortPart))
            genPoint = (ret_R * np.asmatrix(self.orginPoint[worstPointId-1]).T) + np.tile(ret_t, (1,1))
            genPoint = genPoint.T
            points3d[worstPoint] = genPoint
            print("gen point: ", genPoint)

            # Reliability point
            prp = percentReliabilityPoint(self.orginDisSumTable4[0][numsSort[1][0]], points3d, numsSort[0][2])
            print("reliability: ", prp)
        
        ################################### find axis point rt
        ret_R, ret_t = rigid_transform_3D(np.asmatrix(basePoint2dPart),np.asmatrix(points3dSortPart))
        axisPoint = (ret_R * np.asmatrix(self.baseAxisPoint2d).T) + np.tile(ret_t, (1,4))
        axisPoint = axisPoint.T
        # print(axisPoint)

        #################################### axisPointDis
        axisPointDis = np.zeros((3,3))
        for i in range(3):
            # axisPointDis[i] = axisPoint[i] - points3d[numsSort[0][2]]
            axisPointDis[i] = axisPoint[i+1] - axisPoint[0]
        axisPointDis = axisPointDis / 50
        # print(axisPointDis)

        ######################################## find axis angle
        angle = rotationToEuler(axisPointDis)
        print("angle rad: \n", angle)
        angleDeg = np.rad2deg(angle)
        print("angle deg: \n", angleDeg)

        ########################################### write point_result
        # if(reliability[0] > 99):
        if(abs(msePoint) < 100):
        # if(1):
            # result data
            text = ""
            text = str(points3d[0][2]) + ", " + str(reliability[0]) + ", "
            for i in range(4):
                text += str(error[i]) + ', '
            for i in range(3):
                text += str(angleDeg[i]) + ', '
            text += str(msePoint) + ', '
            text += str(rmsePoint) + ', '
            for i in range(4):
                text += str(nums[i][1]) + ', '
            text += '\n'
            self.point_result.write(text) # write

            # sort data
            text = ""
            for i in range(4):
                for j in range(3):
                    text += str(points3dSort[i][j]) + ', '
            text += '\n'
            self.point_sdata.write(text) # write

        ############################################ showPlot3d
        if(showPlot == 1):
        # if(showPlot == 0 and abs(msePoint) > 10):
            showPlot3d(points3d, axisPoint, numsSort[:,2], pc, numsSort[0][2])

        # time
        print("\n--- time 1: %s seconds ---" % (time.time() - start_time_1))

    def close(self):
        self.point_result.close()
        self.point_sdata.close()


###################################################################################
# if main
###################################################################################
if __name__ == '__main__':
    print("find body...\n")
    start_time = time.time()

    fb = FindBody()
    fb = FindBody("data/parameter/marker_body.yaml")

    ########################################## load point_data
    df = pd.read_csv("data/result/point_data.csv", header=0)
    # df = pd.read_csv("data/result/point_data_angle_2.csv", header=0)
    point_data = df.to_numpy()

    ########################################## load point data
    points3d = np.zeros((4,3))
    for i in range(len(point_data[:])):
        print("==========================================================")
        points3d[0] = point_data[i,0:3]
        points3d[1] = point_data[i,3:6]
        points3d[2] = point_data[i,6:9]
        points3d[3] = point_data[i,9:12]
        # points3d[3] = [0,0,0]
        # points3d[0] = [0,0,0]
        # points3d[2] = [0,0,0]
        print("points3d:\n", points3d)

        fb.findBody(points3d)


    print("\n--- total %s seconds ---" % (time.time() - start_time))