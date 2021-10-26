import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import argparse

# kevin import ros
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import ir_track
import threading

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
        self.bridge = CvBridge()

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

        # kevin ros
        rospy.init_node('stero_ir_track', anonymous=False)
        print(rospy.get_name())
        rospy.Subscriber('camera_'+ str(args.camera_right) + '/image', Image, self.getImage, args.camera_right)
        rospy.Subscriber('camera_'+ str(args.camera_left) + '/image', Image, self.getImage, args.camera_left)
        # rospy.Timer(rospy.Duration(2), self.timer_callback)

        # thread
        thread = threading.Thread(target=self.loop)  #建立執行緒
        thread.start()  #執行

        rospy.spin()
    

    ###############################################################################################
    # undistortRectify remap
    ###############################################################################################
    def undistortRectify(self, stereoMapL_x, stereoMapL_y, stereoMapR_x, stereoMapR_y, frameL, frameR):

        # Undistort and rectify images
        undistortedL = cv2.remap(
            frameL, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        undistortedR = cv2.remap(
            frameR, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

        return undistortedL, undistortedR

    ###############################################################################################
    # find_depth
    ###############################################################################################
    def find_depth(self, left_point, right_point, baseline, focal):

        x_left = left_point[0] # x point
        x_right = right_point[0]

        # displacement between left and right frames [pixels]
        disparity = abs(x_left - x_right)
        zDepth = (baseline * focal) / disparity            # z depth in [mm]

        return zDepth

    ###############################################################################################
    # calcu_world_point
    ###############################################################################################
    def calcu_world_point(self,point, z_depth, focal):
        world_points = np.zeros((3), np.float)
        x_cam = point[0]
        y_cam = point[1]
        world_points[0] = (x_cam * z_depth) / focal
        world_points[1] = (y_cam * z_depth) / focal
        world_points[2] = z_depth
        return world_points

    ########################################################################################
    # getImage
    ########################################################################################
    def getImage(self, data, arg=0):
        img = self.bridge.imgmsg_to_cv2(data, desired_encoding='8UC3')
        self.frame[arg] = img

    ########################################################################################
    # loop
    ########################################################################################
    def loop(self):
        while not rospy.is_shutdown():
            # undistortRectify remap
            frame_left, frame_right  = self.undistortRectify(
            self.stereoMapL_x, self.stereoMapL_y, self.stereoMapR_x, self.stereoMapR_y, self.frame[0], self.frame[1])

            # ir track
            left_points = ir_track.ir_track(frame_left)
            right_points = ir_track.ir_track(frame_right)
            left_num = len(left_points)
            right_num = len(right_points)
            world_points = np.zeros((left_num,3), np.float)
            if(left_num > 0 and right_num > 0 and left_num == right_num):
                for i in range(left_num):
                    left_point = left_points[i].ravel()
                    right_point = right_points[i].ravel()
                    # print('left_point:', left_point)
                    # print('right_point:',  right_point)

                    # find depth
                    depth = self.find_depth(left_point, right_point, self.baseline, self.focalLength)
                    if(self.showFlag):
                        text = "Dis: " + str(round(depth, 1))
                        cv2.putText(frame_right, text,
                                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # find world point
                    world_points[i] = self.calcu_world_point(left_point, depth, self.focalLength)
                    if(self.showFlag):
                        text = "X:" + str(round(world_points[i][0], 1)) + " Y:" + str(round(world_points[i][1], 1))
                        cv2.putText(frame_left, text,
                                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # print world point
                # print('x:', x_world_point, 'y:', y_world_point, 'z:', depth)
                print('world_points:', world_points.ravel())

                if(self.showFlag):
                    # mix to show on one picture
                    vis = np.concatenate((frame_left, frame_right), axis=1)
                    cv2.imshow('vis', vis)
                    # cv2.waitKey(100)

if __name__=="__main__": 
    stero_ir_track = steroIrTrack()