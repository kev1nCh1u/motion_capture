
import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *
from lib.kevin import kevinuart

from src.image_processing.kevinVision.get_data_3d import *
from src.image_processing.kevinVision.point_segment import *
from src.image_processing.kevinVision.find_body import *

import time

class Main():
    def __init__(self):

        import get_data_3d
        import point_segment
        import find_body

        print(" _  __          _        ____ _     _       ")
        print("| |/ /_____   _(_)_ __  / ___| |__ (_)_   _ ")
        print("| ' // _ \ \ / / | '_ \| |   | '_ \| | | | |")
        print("| . \  __/\ V /| | | | | |___| | | | | |_| |")
        print("|_|\_\___| \_/ |_|_| |_|\____|_| |_|_|\__,_|")
        print("Kevin vision start...")                  

        self.gd = GetData(file=0)
        self.fb = FindBody()
        self.ps = PointSegment()

        print(self.gd.cameraMatrix1)

        ######################################### load data
        self.data_file = open("data/result/point_main.csv", "w") # open point_data
        text =  "id, x, y, z, roll, pitch, yaw, mse, rmse"
        text += "\n"
        self.data_file.write(text) # write point_data

        ########################################### uart
        self.kuc = kevinuart.UartControl('/dev/ttyUSB1') # right camera
        self.kuc1 = kevinuart.UartControl('/dev/ttyUSB0') # left camera
        
        # binary thres:50 100
        self.kuc.ser_write(1, 100) 
        self.kuc1.ser_write(1, 100)

    def runData(self):
        pass
        #################### get data by csv
        df = pd.read_csv("data/result/input_data.csv", header=0)
        point = df.to_numpy()
        for i in range(len(point)):
            start_time = time.time()
            point2d_1 = point[i,0:16].reshape((-1,2))
            point2d_2 = point[i,16:32].reshape((-1,2))
            points3d = self.gd.getPoint(8,point2d_1,point2d_2)

            ####################### findBody
            # markerID, axisVector, angleDeg, msePoint, rmsePoint, pc = ps.pointSegment(points3d)

            markerID, point3dSeg, count, pc = self.ps.pointSegment(points3d)
            axisVector = np.zeros((2,4,3))
            angleDeg = np.zeros((2,3))
            msePoint = np.zeros((2))
            rmsePoint = np.zeros((2))
            for i in range(count):
                axisVector[i], angleDeg[i], msePoint[i], rmsePoint[i] = self.fb.findBody(point3dSeg[i],table=int(markerID[i]))

            ########################## end
            text =  ""
            if(axisVector[0][0][0] and msePoint[0] < 50):
            # if(1):
                pass
                # print("--- total %s seconds ---" % (time.time() - start_time))
                # print(int(markerID[0]), str(np.round(axisVector[0][0],2)), str(np.round(angleDeg[0],2)), np.round(msePoint[0],2), np.round(rmsePoint[0],2))
                
                print("id:%1d x:%08.2f y:%08.2f z:%08.2f r:%08.2f p:%08.2f y:%08.2f mse:%08.2f rmse:%08.2f pc:%d      end"
                    %(int(markerID[0]),np.round(axisVector[0][0][0],2),np.round(axisVector[0][0][1],2),np.round(axisVector[0][0][2],2)
                    ,np.round(angleDeg[0][0],2),np.round(angleDeg[0][1],2),np.round(angleDeg[0][2],2)
                    ,np.round(msePoint[0],2),np.round(rmsePoint[0],2),pc), end="\r")

                for i in range(int(pc/4)):
                    text += str(int(markerID[i]))+","+str(np.round(axisVector[i][0][0],2))+","+str(np.round(axisVector[i][0][1],2))+","+str(np.round(axisVector[i][0][2],2))+","
                    text += str(np.round(angleDeg[i][0],2))+","+str(np.round(angleDeg[i][1],2))+","+str(np.round(angleDeg[i][2],2))+","
                    text += str(np.round(msePoint[i],2))+","+str(np.round(rmsePoint[i],2))
                    text += "\n"
                self.data_file.write(text) # write point_data

            # time.sleep(0.1)
        print()

    def run(self):
        ###################### get data by cam
        while 1:
            start_time = time.time()
            self.kuc.uart_ser() # read uart right camera
            self.kuc1.uart_ser() # read uart left camera

            point2d_1 = self.kuc.point2d
            point2d_2 = self.kuc1.point2d
            points3d = self.gd.getPoint(8,point2d_1,point2d_2)
            # print(points3d)

            ####################### findBody
            # markerID, axisVector, angleDeg, msePoint, rmsePoint, pc = ps.pointSegment(points3d)

            markerID, point3dSeg, count, pc = self.ps.pointSegment(points3d)
            axisVector = np.zeros((2,4,3))
            angleDeg = np.zeros((2,3))
            msePoint = np.zeros((2))
            rmsePoint = np.zeros((2))
            for i in range(count):
                axisVector[i], angleDeg[i], msePoint[i], rmsePoint[i] = self.fb.findBody(point3dSeg[i],table=int(markerID[i]))

            ########################## end
            text =  ""
            if(axisVector[0][0][0] and msePoint[0] < 50):
            # if(1):
                pass
                # print("--- total %s seconds ---" % (time.time() - start_time))
                # print(int(markerID[0]), str(np.round(axisVector[0][0],2)), str(np.round(angleDeg[0],2)), np.round(msePoint[0],2), np.round(rmsePoint[0],2))
                
                print("id:%1d x:%08.2f y:%08.2f z:%08.2f r:%08.2f p:%08.2f y:%08.2f mse:%08.2f rmse:%08.2f pc:%d      end"
                    %(int(markerID[0]),np.round(axisVector[0][0][0],2),np.round(axisVector[0][0][1],2),np.round(axisVector[0][0][2],2)
                    ,np.round(angleDeg[0][0],2),np.round(angleDeg[0][1],2),np.round(angleDeg[0][2],2)
                    ,np.round(msePoint[0],2),np.round(rmsePoint[0],2),pc), end="\r")

                for i in range(int(pc/4)):
                    text += str(int(markerID[i]))+","+str(np.round(axisVector[i][0][0],2))+","+str(np.round(axisVector[i][0][1],2))+","+str(np.round(axisVector[i][0][2],2))+","
                    text += str(np.round(angleDeg[i][0],2))+","+str(np.round(angleDeg[i][1],2))+","+str(np.round(angleDeg[i][2],2))+","
                    text += str(np.round(msePoint[i],2))+","+str(np.round(rmsePoint[i],2))
                    text += "\n"
                self.data_file.write(text) # write point_data

            # time.sleep(0.1)
        print()

###################################################################################
# main
###################################################################################
if __name__ == '__main__':
    m = Main()
    # m.run()
    m.runData()

        
   
