
import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *
from lib.kevin import kevinuart

from src.image_processing.stereo_vision.get_data_3d import *
from src.image_processing.stereo_vision.point_segment import *
from src.image_processing.stereo_vision.find_body import *

import time


###################################################################################
# main
###################################################################################
if __name__ == '__main__':

    gd = GetData(file=0)
    ps = PointSegment()

    ######################################### load data
    data_file = open("data/result/point_main.csv", "w") # open point_data
    text =  "id, x, y, z, roll, pitch, yaw, mse, rmse"
    text += "\n"
    data_file.write(text) # write point_data

    ########################################### uart
    kuc = kevinuart.UartControl('/dev/ttyUSB1') # right camera
    kuc1 = kevinuart.UartControl('/dev/ttyUSB0') # left camera
    
    # binary thres:50 100
    kuc.ser_write(1, 100) 
    kuc1.ser_write(1, 100)

    ##################### get data by csv
    # df = pd.read_csv("data/result/input_data.csv", header=0)
    # point = df.to_numpy()
    # for i in range(len(point)):
    #     start_time = time.time()
    #     point2d_1 = point[i,0:16].reshape((-1,2))
    #     point2d_2 = point[i,16:32].reshape((-1,2))
    #     points3d = gd.getPoint(8,point2d_1,point2d_2)
    #     sortList, axisVector, angleDeg, msePoint, rmsePoint = ps.pointSegment(points3d)
        
    ###################### get data by cam
    while 1:
        start_time = time.time()
        kuc.uart_ser() # read uart right camera
        kuc1.uart_ser() # read uart left camera

        point2d_1 = kuc.point2d
        point2d_2 = kuc1.point2d
        points3d = gd.getPoint(8,point2d_1,point2d_2)
        # print(points3d)
        sortList, axisVector, angleDeg, msePoint, rmsePoint, pc = ps.pointSegment(points3d)

        ########################## end
        text =  ""
        if(axisVector[0][0][0]):
        # if(1):
            pass
            # print("--- total %s seconds ---" % (time.time() - start_time))
            # print(int(sortList[0]), str(np.round(axisVector[0][0],2)), str(np.round(angleDeg[0],2)), np.round(msePoint[0],2), np.round(rmsePoint[0],2))
            
            print("id:%1d x:%003.2f y:%03.2f z:%03.2f r:%03.2f p:%03.2f y:%03.2f mse:%03.2f rmse:%03.2f pc:%d      end"
                %(int(sortList[0]),np.round(axisVector[0][0][0],2),np.round(axisVector[0][0][1],2),np.round(axisVector[0][0][2],2)
                ,np.round(angleDeg[0][0],2),np.round(angleDeg[0][1],2),np.round(angleDeg[0][2],2)
                ,np.round(msePoint[0],2),np.round(rmsePoint[0],2),pc), end="\r")

            for i in range(2):
                text += str(int(sortList[i]))+","+str(np.round(axisVector[i][0][0],2))+","+str(np.round(axisVector[i][0][1],2))+","+str(np.round(axisVector[i][0][2],2))+","
                text += str(np.round(angleDeg[i][0],2))+","+str(np.round(angleDeg[i][1],2))+","+str(np.round(angleDeg[i][2],2))+","
                text += str(np.round(msePoint[i],2))+","+str(np.round(rmsePoint[i],2))
                text += "\n"
            data_file.write(text) # write point_data

        # time.sleep(0.1)
