from itertools import count
import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import time

import os
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *
from lib.kevin import kevinuart

from src.image_processing.stereo_vision.get_data_3d import *
from src.image_processing.stereo_vision.find_body import *

###################################################################################
# PointSegment
###################################################################################
class PointSegment():
    def __init__(self, file=0):
        self.fb = FindBody()

        ########################################### file
        self.count = 0
        if(file):
            self.data_file = open("data/result/point_segment.csv", "w") # open point_data

            text = ""
            for i in range(4): text += "p" + str(i) + "x," + "p" + str(i) + "y," + "p" + str(i) + "z,"
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
            # self.orginDis[i] = findAllDis(self.orginPoint)
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
        self.points3d = points3d
        # print("orginDisSumTableList4",self.orginDisSumTableList4)
        # print("orginDisSumTableList3",self.orginDisSumTableList3)
        # print("orginDisSumTableList4",self.orginDisSumTableList4)
        # print("points3d",points3d)

        # point calculate
        pc = pointCount(points3d,8)
        points3dCombinations = list(combinations(points3d,4))
        # points3dCombinations = list(permutations(points3d,4))
        point3dSeg = np.zeros((5,4,3))
        point3dList = np.zeros((2))
        count = 0
        for i in range(len(points3dCombinations)):
            pointDis = findAllDis(points3dCombinations[i])
            pointDisSum = arraySum(pointDis)[0]
            pointList = np.sum(pointDisSum)
            if(pointList < 1000 and pc == 8):
                # print(pointList)
                point3dList[count] = pointList
                point3dSeg[count] = points3dCombinations[i]
                count += 1
        point3dListSort = np.append(point3dList.reshape((2, 1)), np.arange(2).reshape((2, 1)), axis=1)
        point3dListSort = np.sort(point3dListSort.view('i8,i8'), order=['f0'], axis=0).view(np.float64)
        # print(point3dListSort)
        # print("pointCount:", pc)
        # print("points distanse:\n", pointDis)
        # print("points distanse sum:\n",pointDisSum)

        axisVector = np.zeros((2,4,3))
        angleDeg = np.zeros((2,3))
        msePoint = np.zeros((2))
        rmsePoint = np.zeros((2))
        for i in range(2):
            if(point3dListSort[i][0]):
                axisVector[i], angleDeg[i], msePoint[i], rmsePoint[i] = self.fb.findBody(point3dSeg[int(point3dListSort[i][1])],table=int(self.sortList[i][1]))

        return self.sortList[:,1], axisVector, angleDeg, msePoint, rmsePoint
    
    ############################## close
    def close(self):
        cv2.destroyAllWindows()


###################################################################################
# main
###################################################################################
if __name__ == '__main__':

    gd = GetData(file=0)
    ps = PointSegment()

    ##################### get data by csv
    df = pd.read_csv("data/result/input_data.csv", header=0)
    point = df.to_numpy()
    for i in range(len(point)):
        start_time = time.time()
        point2d_1 = point[i,0:16].reshape((-1,2))
        point2d_2 = point[i,16:32].reshape((-1,2))

        test = np.full((4,2),1)
        points3d = gd.getPoint(8,point2d_1,point2d_2)
        # time.sleep(0.1)

        ps.pointSegment(points3d)
        print("--- total %s seconds ---" % (time.time() - start_time)) 
        
    gd.close()
    
    ###################### get data by cam
    # while 1:
    #     points3d = gd.getPoint()
    #     ps.pointSegment(points3d)
    #     ps.showImage()