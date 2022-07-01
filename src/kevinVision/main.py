
import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *
from lib.kevin import kevinuart

from src.kevinVision.get_data_3d import *
from src.kevinVision.point_segment import *
from src.kevinVision.find_body import *

import time

class Main():
    def __init__(self):

        print(" _              _    __     ___     _             ")
        print("| | _______   _(_)_ _\ \   / (_)___(_) ___  _ __  ")
        print("| |/ / _ \ \ / / | '_ \ \ / /| / __| |/ _ \| '_ \ ")
        print("|   <  __/\ V /| | | | \ V / | \__ \ | (_) | | | |")
        print("|_|\_\___| \_/ |_|_| |_|\_/  |_|___/_|\___/|_| |_|")
        print("Kevin vision start...")                  

        self.gd = GetData(file=0)
        self.fb = FindBody()
        self.ps = PointSegment()

        # print(self.gd.cameraMatrix1)
        self.mainCounter = 0

        ######################################### load data
        self.data_file = open("data/result/point_main.csv", "w") # open point_data
        text =  "id, x, y, z, roll, pitch, yaw, mse, rmse, mae, mape"
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
            # markerID, axisVector, angle, msePoint, rmsePoint, pc = ps.pointSegment(points3d)

            markerID, point3dSeg, count, pc = self.ps.pointSegment(points3d)
            axisVector = np.zeros((2,4,3))
            angle = np.zeros((2,3))
            msePoint = np.zeros((2))
            rmsePoint = np.zeros((2))
            maePoint = np.zeros((2))
            mapePoint = np.zeros((2))
            for i in range(count):
                axisVector[i], angle[i], msePoint[i], rmsePoint[i], maePoint[i], mapePoint[i] = self.fb.findBody(point3dSeg[i],table=int(markerID[i]))

            ########################## end
            text =  ""
            if(axisVector[0][0][0] and msePoint[0] < 50):
            # if(1):
                pass
                # print("--- total %s seconds ---" % (time.time() - start_time))
                # print(int(markerID[0]), str(np.round(axisVector[0][0],2)), str(np.round(angle[0],2)), np.round(msePoint[0],2), np.round(rmsePoint[0],2))
                
                print("id:%1d x:%08.2f y:%08.2f z:%08.2f r:%08.2f p:%08.2f y:%08.2f mse:%08.2f rmse:%08.2f mae:%08.2f mape:%08.2f pc:%d      end"
                    %(int(markerID[0]),np.round(axisVector[0][0][0],2),np.round(axisVector[0][0][1],2),np.round(axisVector[0][0][2],2)
                    ,np.round(angle[0][0],2),np.round(angle[0][1],2),np.round(angle[0][2],2)
                    ,np.round(msePoint[0],2),np.round(rmsePoint[0],2),np.round(maePoint[0],2),np.round(mapePoint[0],2),pc), end="\r")

                for i in range(int(pc/4)):
                    text += str(int(markerID[i]))+","+str(np.round(axisVector[i][0][0],2))+","+str(np.round(axisVector[i][0][1],2))+","+str(np.round(axisVector[i][0][2],2))+","
                    text += str(np.round(angle[i][0],2))+","+str(np.round(angle[i][1],2))+","+str(np.round(angle[i][2],2))+","
                    text += str(np.round(msePoint[i],2))+","+str(np.round(rmsePoint[i],2))+","+str(np.round(maePoint[i],2))+","+str(np.round(mapePoint[i],2))
                    text += "\n"
                self.data_file.write(text) # write point_data

            # time.sleep(0.1)
        print()

    def run(self):
        ###################### get data by cam
        start_time = time.time()
        self.kuc.uart_ser() # read uart right camera
        self.kuc1.uart_ser() # read uart left camera

        point2d_1 = self.kuc.point2d
        point2d_2 = self.kuc1.point2d
        points3d = self.gd.getPoint(8,point2d_1,point2d_2)
        # print(points3d)

        ####################### findBody
        # markerID, axisVector, angle, msePoint, rmsePoint, pc = ps.pointSegment(points3d)

        markerID, point3dSeg, count, pc = self.ps.pointSegment(points3d)
        axisVector = np.zeros((2,4,3))
        angle = np.zeros((2,3))
        msePoint = np.zeros((2))
        rmsePoint = np.zeros((2))
        maePoint = np.zeros((2))
        mapePoint = np.zeros((2))
        for i in range(count):
            axisVector[i], angle[i], msePoint[i], rmsePoint[i], maePoint[i], mapePoint[i] = self.fb.findBody(point3dSeg[i],table=int(markerID[i]))

        ########################## end
        text =  ""
        if(axisVector[0][0][0] and msePoint[0] < 50):
        # if(1):
            pass
            # print("--- total %s seconds ---" % (time.time() - start_time))
            # print(int(markerID[0]), str(np.round(axisVector[0][0],2)), str(np.round(angle[0],2)), np.round(msePoint[0],2), np.round(rmsePoint[0],2))
            
            # print("id:%1d x:%08.2f y:%08.2f z:%08.2f r:%06.2f p:%06.2f y:%06.2f rmse:%06.2f pc:%d      end"
            #     %(int(markerID[0]),np.round(axisVector[0][0][0],2),np.round(axisVector[0][0][1],2),np.round(axisVector[0][0][2],2)
            #     ,np.round(angle[0][0],2),np.round(angle[0][1],2),np.round(angle[0][2],2)
            #     ,np.round(rmsePoint[0],2),pc), end="\r")

            print("id:%1d x:%08.2f y:%08.2f z:%08.2f rmse:%06.2f ; id:%1d x:%08.2f y:%08.2f z:%08.2f rmse:%06.2f    end"
                %(int(markerID[0]),np.round(axisVector[0][0][0],2),np.round(axisVector[0][0][1],2),np.round(axisVector[0][0][2],2),np.round(rmsePoint[0],2),
                int(markerID[1]),np.round(axisVector[1][0][0],2),np.round(axisVector[1][0][1],2),np.round(axisVector[1][0][2],2),np.round(rmsePoint[1],2)), end="\r")

            # print("get", np.round(axisVector[0][0][2],2))

            for i in range(int(pc/4)):
                text += str(int(markerID[i]))+","+str(np.round(axisVector[i][0][0],2))+","+str(np.round(axisVector[i][0][1],2))+","+str(np.round(axisVector[i][0][2],2))+","
                text += str(np.round(angle[i][0],2))+","+str(np.round(angle[i][1],2))+","+str(np.round(angle[i][2],2))+","
                text += str(np.round(msePoint[i],2))+","+str(np.round(rmsePoint[i],2))+","+str(np.round(maePoint[i],2))+","+str(np.round(mapePoint[i],2))
                text += "\n"
            self.data_file.write(text) # write point_data

            self.mainCounter += 1

        # time.sleep(0.1)
    # print()

###################################################################################
# main
###################################################################################
if __name__ == '__main__':
    m = Main()

    # m.runData()

    while 1:
        m.run()

    # while(1):
    #     print("===========")
    #     while(1):
    #         m.run()
    #         if(m.mainCounter > 20):
    #             m.mainCounter = 0
    #             break 
    #     print("Get finish! press key...")
    #     input()
    
    print()

        
   
