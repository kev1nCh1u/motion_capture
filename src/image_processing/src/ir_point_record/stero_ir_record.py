import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

# kevin import ros
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point32
from cv_bridge import CvBridge

import ir_track
import threading
import math
import pandas as pd

print('\n opencv version:', cv2.__version__)

########################################################################################
# steroIrTrack
########################################################################################
class steroIrTrack:

    ########################################################################################
    # __init__
    ########################################################################################
    def __init__(self):
        # kevin args
        parser = argparse.ArgumentParser()
        parser.add_argument("-cs", "--cv_show", default=0, help="0,1")
        parser.add_argument("-r", "--camera_right", default=0, help="0,1,2...")
        parser.add_argument("-l", "--camera_left", default=1, help="0,1,2...")
        args = parser.parse_args()

        # define
        self.showFlag = args.cv_show
        self.frame = np.zeros((2,480,640,3), np.uint8)

        # define camera
        fs = cv2.FileStorage("param/matlab_stereo_param.yaml", cv2.FILE_STORAGE_READ)
        self.baseline = abs(fs.getNode("TranslationOfCamera2").mat().ravel()[0])
        self.focalLength = fs.getNode("FocalLength").mat().ravel()[0]

        # Camera parameters to undistort and rectify images
        cv_file = cv2.FileStorage()
        cv_file.open('param/stereoMap.xml', cv2.FileStorage_READ)
        self.stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
        self.stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
        self.stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
        self.stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

        # record define
        self.fileName = '01' # 01 ~ 10
        self.minPoint = (120, 50, 0) # math.inf
        self.maxPoint = (527, 190, 0) # 0
        self.axis = 1 # x:0 y:1 z:2
        self.points = np.zeros((10000, 1, 3), np.int32)
        self.num = 0
        self.saveFlag = False
        self.minFlag = False
        self.maxFlag = False
        self.findMinMaxFlag = True # False
        self.saveDataPath = "data/point_path/point_path_data_" + self.fileName + ".csv"
        self.savePlotPath = 'img/result/point_path_plot/point_path_plot_' + self.fileName + '.png'
        self.finishFlag = False

        # kevin ros
        rospy.init_node('stero_ir_record', anonymous=False, disable_signals=True)
        print(rospy.get_name())
        rospy.Subscriber('/stero_ir_track/point', Point32, self.getPoint)
        self.bridge = CvBridge()
        # rospy.Timer(rospy.Duration(2), self.timer_callback)

        rospy.spin()


    ########################################################################################
    # getImage
    ########################################################################################
    def getPoint(self, data):

        point = np.zeros((3), np.int32)
        point[0] = data.x
        point[1] = data.y
        point[2] = data.z
        print('Now:', point, end='\r')

        if not self.finishFlag:
            self.finishFlag = self.savePoint(point)
            if self.finishFlag:
                print('Finish.......')
                rospy.signal_shutdown('finish')
                exit()

    ########################################################################################
    # savePoint
    ########################################################################################
    def savePoint(self, point):

        self.points[self.num][0] = point

        if self.findMinMaxFlag and not self.saveFlag:
            if point[self.axis] <= self.minPoint[self.axis]:
                self.saveFlag = True
                print('start save...', self.minPoint[self.axis], '~', self.maxPoint[self.axis])

        if self.saveFlag == True:
            self.points[self.num][0] = point
            self.num = self.num + 1
            if  point[self.axis] >= self.maxPoint[self.axis]:
                # print(self.points[:self.num])
                print('\n\nNum of point', self.num)
                print('MinMax', self.minPoint[self.axis], self.maxPoint[self.axis])

                pointsReshape = np.reshape(self.points[:self.num], (-1,3))
                # np.savetxt(self.saveDataPath, pointsReshape, delimiter=",")
                pd.DataFrame(pointsReshape).to_csv(self.saveDataPath)
                print('Save data file to:', self.saveDataPath)
                
                # show plot 2d
                # plt.clf()
                # plt.title('Points' + self.fileName)
                # plt.xlabel('x axis')
                # plt.ylabel('y axis')
                # plt.plot(pointsReshape[:,0],pointsReshape[:,1], 'o', markersize=1)
                # plt.xlim([0, 640])
                # plt.ylim([480, 0])
                # plt.savefig(self.savePlotPath)
                # print('Save plot image to:', self.savePlotPath)
                # plt.show(False)
                # plt.pause(1)
                # # plt.close()

                # show plot 3d
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                # ax.xlim([0, 640])
                # ax.ylim([480, 0])
                ax.set_xlim(0,640)
                ax.set_ylim(480,0)
                ax.set_zlim(0,2000)
                ax.scatter(pointsReshape[:,0], pointsReshape[:,1], pointsReshape[:,2], c=pointsReshape[:,self.axis], cmap='Reds', label='Point')
                ax.legend()
                plt.savefig(self.savePlotPath)
                plt.show()

                return True

            

if __name__=="__main__": 
    stero_ir_track = steroIrTrack()