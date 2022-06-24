import sys
import cv2
import numpy as np
import time
import time

import os
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *

from src.kevinVision.get_data_3d import *
from src.kevinVision.find_body import *

###################################################################################
# PointSegment
###################################################################################
class PointSegment():
    def __init__(self, file=0):
        self.fb = FindBody()
        self.file = file

        ########################################### file
        self.count = 0
        if(file):
            self.data_file = open("data/result/point_segment.csv", "w") # open point_data

            text = ""
            for i in range(8): text += "p" + str(i) + "x," + "p" + str(i) + "y," + "p" + str(i) + "z,"
            text += "\n"
            self.data_file.write(text) # write point_data

        ########################################## load param and data
        # marker parameter
        self.orginDis = np.zeros((2,4,4))
        self.orginPoint = np.zeros((2,4,3))
        for i in range(2):
            fs = cv2.FileStorage("data/parameter/create_markers"+str(i)+".yaml", cv2.FILE_STORAGE_READ)
            self.orginDis[i] = fs.getNode("orginDistance").mat()
            self.orginPoint[i] = fs.getNode("orginPoint").mat()
        # print(self.orginDis[0])
        
        ########################################## orgin calculate
        self.orginDisSumTableList4 = np.zeros(2)
        self.orginDisSumTableList3 = np.zeros(2*4)
        for i in range(2):
            self.orginDis[i] = findAllDis(self.orginPoint[i])
            self.orginDisSumTable4 = arraySum(self.orginDis[i])
            self.orginDisSumTable3 = arraySumPart3(self.orginDis[i])
            self.orginDisSumTableList4[i] = np.sum(self.orginDisSumTable4)
            for j in range(4): self.orginDisSumTableList3[i*4+j] = np.sum(self.orginDisSumTable3[j,:])
        # print(self.orginDisSumTable4)
        # print(self.orginDisSumTable3)
        # print(self.orginDisSumTableList4)
        # print(self.orginDisSumTableList3)

        self.sortList = np.append(self.orginDisSumTableList4.reshape((2, 1)), np.arange(2).reshape((2, 1)), axis=1)
        self.sortList = np.sort(self.sortList.view('i8,i8'), order=['f0'], axis=0).view(np.float64)
        # print(self.sortList)
        

    ########################################## pointSegment
    def pointSegment(self, points3d):
        markerID = np.full((2), -1)
        # axisVector = np.zeros((2,4,3))
        # angleDeg = np.zeros((2,3))
        # msePoint = np.zeros((2))
        # rmsePoint = np.zeros((2))

        ######################## point calculate
        self.points3d = points3d
        pc = pointCount(points3d,8)
        points3dCombinations = list(combinations(points3d[:pc],4))
        # points3dCombinations = list(permutations(points3d,4))
        # print(points3dCombinations)
        point3dSeg = np.zeros((5,4,3))
        point3dList = np.zeros((2))
        count = 0

        ######################## find marker
        if(pc <= 4 and pc >= 1):
            point3dSeg[0] = points3d[0:4]
            pointDis = findAllDis(point3dSeg[0])
            pointDisSum = arraySum(pointDis)[0]
            pointList = np.sum(pointDisSum)
            markerID[0] = findCloseNum(pointList,self.orginDisSumTableList4)
            count = 1
            # axisVector[0], angleDeg[0], msePoint[0], rmsePoint[0] = self.fb.findBody(points3d[0:4],table=int(markerID[0]))
            # return markerID, axisVector, angleDeg, msePoint, rmsePoint, pc
        else:
            for i in range(len(points3dCombinations)):
                pointDis = findAllDis(points3dCombinations[i])
                pointDisSum = arraySum(pointDis)[0]
                pointList = np.sum(pointDisSum)
                if(pointList < 1000 and pc >= 4 and count < 2 and pointDisSum[0] and pointDisSum[1] and pointDisSum[2] and pointDisSum[3]):
                    # print(pointList)
                    point3dList[count] = pointList
                    point3dSeg[count] = points3dCombinations[i]
                    markerID[count] = findCloseNum(pointList,self.orginDisSumTableList4)
                    count += 1
            # print(point3dList)
            # point3dListSort = np.append(point3dList.reshape((2, 1)), np.arange(2).reshape((2, 1)), axis=1)
            # point3dListSort = np.sort(point3dListSort.view('i8,i8'), order=['f0'], axis=0).view(np.float64)

            # for i in range(count):
            #     if(point3dListSort[i][0] and point3dListSort[i][0] and point3dListSort[i][0] and point3dListSort[i][0]):
            #         axisVector[i], angleDeg[i], msePoint[i], rmsePoint[i] = self.fb.findBody(point3dSeg[int(point3dListSort[i][1])],table=int(self.sortList[i][1]))
            
            ######################## findBody
            # for i in range(count):
            #     axisVector[i], angleDeg[i], msePoint[i], rmsePoint[i] = self.fb.findBody(point3dSeg[i],table=int(markerID[i]))

        ######################## save to file
        if(self.file):
            text = ""
            for i in range(2):
                for j in range(4):
                    for k in range(3):
                        text += str(int(point3dSeg[i,j,k]))+","
            text += "\n"
            self.data_file.write(text) # write point_data

        # return self.sortList[:,1], axisVector, angleDeg, msePoint, rmsePoint, pc
        # return markerID, axisVector, angleDeg, msePoint, rmsePoint, pc
        return markerID, point3dSeg, count, pc
    
    ############################## close
    def close(self):
        cv2.destroyAllWindows()


###################################################################################
# main
###################################################################################
if __name__ == '__main__':

    gd = GetData(file=0)
    fb = FindBody()
    ps = PointSegment(file=1)

    ##################### get data by input_data
    df = pd.read_csv("data/result/input_data.csv", header=0)
    point = df.to_numpy()
    start_time = time.time()
    for i in range(len(point)):
        point2d_1 = point[i,0:16].reshape((-1,2))
        point2d_2 = point[i,16:32].reshape((-1,2))

        points3d = gd.getPoint(8,point2d_1,point2d_2)

        # markerID, axisVector, angleDeg, msePoint, rmsePoint, pc = ps.pointSegment(points3d)

        markerID, point3dSeg, count, pc = ps.pointSegment(points3d)
        axisVector = np.zeros((2,4,3))
        angleDeg = np.zeros((2,3))
        msePoint = np.zeros((2))
        rmsePoint = np.zeros((2))
        for j in range(count):
            axisVector[j], angleDeg[j], msePoint[j], rmsePoint[j] = fb.findBody(point3dSeg[j],table=int(markerID[j]))


        print(markerID)
    print("%s ms ---" % ((time.time() - start_time) / len(point) * 1000))
        
    ########################################## load point_data
    # # df = pd.read_csv("data/result/point_data.csv", header=0)
    # df = pd.read_csv("data/result/point_data/point_data_angle_yaw.csv", header=0)
    # # df = pd.read_csv("data/result/point_data/point_data_angle_45.csv", header=0)
    # point_data = df.to_numpy(float32)
    # print(len(point_data[:]))

    # points3d = np.zeros((8,3),float32)
    # start_time = time.time()
    # for i in range(len(point_data[:])):
    #     points3d[0] = point_data[i,0:3]
    #     points3d[1] = point_data[i,3:6]
    #     points3d[2] = point_data[i,6:9]
    #     points3d[3] = point_data[i,9:12]

    #     # markerID, axisVector, angleDeg, msePoint, rmsePoint, pc = ps.pointSegment(points3d)

    #     markerID, point3dSeg, count, pc = ps.pointSegment(points3d)
    #     axisVector = np.zeros((2,4,3))
    #     angleDeg = np.zeros((2,3))
    #     msePoint = np.zeros((2))
    #     rmsePoint = np.zeros((2))
    #     for j in range(count):
    #         axisVector[j], angleDeg[j], msePoint[j], rmsePoint[j] = fb.findBody(point3dSeg[j],table=int(markerID[j]))

    #     print(markerID)
    # print("%s ms ---" % ((time.time() - start_time) / len(point_data[:]) * 1000))
    
    ###################### get data by cam
    # while 1:
    #     points3d = gd.getPoint()

    #     # markerID, axisVector, angleDeg, msePoint, rmsePoint, pc = ps.pointSegment(points3d)

    #     markerID, point3dSeg, count, pc = ps.pointSegment(points3d)
    #     axisVector = np.zeros((2,4,3))
    #     angleDeg = np.zeros((2,3))
    #     msePoint = np.zeros((2))
    #     rmsePoint = np.zeros((2))
    #     for j in range(count):
    #         axisVector[j], angleDeg[j], msePoint[j], rmsePoint[j] = fb.findBody(point3dSeg[j],table=int(markerID[j]))

    #     ps.showImage()