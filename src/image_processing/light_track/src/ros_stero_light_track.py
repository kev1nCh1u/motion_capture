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
from geometry_msgs.msg import Point32
from cv_bridge import CvBridge

import ir_track
import threading

import os
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *
from lib.kevin import kevinuart

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
        parser.add_argument("-l", "--camera_left", default=0, help="0,1,2...")
        parser.add_argument("-r", "--camera_right", default=1, help="0,1,2...")
        args = parser.parse_args()

        # define
        self.showFlag = args.cv_show
        self.frame = np.zeros((2,480,640,3), np.uint8)

        # define camera
        fs = cv2.FileStorage("data/parameter/matlab_stereo_param.yaml", cv2.FILE_STORAGE_READ)
        self.baseline = abs(fs.getNode("TranslationOfCamera2").mat().ravel()[0])
        self.focalLength = fs.getNode("FocalLength").mat().ravel()[0]

        # Camera parameters to undistort and rectify images
        cv_file = cv2.FileStorage()
        cv_file.open('data/parameter/stereoMap.xml', cv2.FileStorage_READ)
        self.stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
        self.stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
        self.stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
        self.stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

        # kevin ros
        rospy.init_node('ros_stero_light_track', anonymous=False)
        print(rospy.get_name())
        rospy.Subscriber('camera_'+ str(args.camera_left) + '/image', Image, self.getImage, args.camera_left)
        rospy.Subscriber('camera_'+ str(args.camera_right) + '/image', Image, self.getImage, args.camera_right)
        self.pub_cvimg = rospy.Publisher(rospy.get_name()+'/image', Image)
        self.pub_point = rospy.Publisher(rospy.get_name()+'/point', Point32)
        self.bridge = CvBridge()
        # rospy.Timer(rospy.Duration(2), self.timer_callback)

        # thread
        thread = threading.Thread(target=self.loop)  #建立執行緒
        thread.start()  #執行

        rospy.spin()

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
            frame_left = self.frame[0]
            frame_right = self.frame[1]

            # draw green rectangle
            # cv2.rectangle(frame_left, (0, 0), (640, 480), (255, 0, 0), 2)
            # cv2.rectangle(frame_right, (0, 0), (640, 480), (255, 0, 0), 2)

            # stereoRemap remap
            frame_left, frame_right  = stereoRemap(
            self.stereoMapL_x, self.stereoMapL_y, self.stereoMapR_x, self.stereoMapR_y, frame_left, frame_right)

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
                    depth = find_depth(left_point, right_point, self.baseline, self.focalLength)
                    if(self.showFlag):
                        text = "Dis: " + str(round(depth, 1))
                        cv2.putText(frame_right, text,
                                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # find world point
                    world_points[i] = calcu_world_point(left_point, depth, self.focalLength)
                    if(self.showFlag):
                        text = "X:" + str(round(world_points[i][0], 1)) + " Y:" + str(round(world_points[i][1], 1))
                        cv2.putText(frame_left, text,
                                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # print world point
                    # print('world_points%d:'%i, world_points[i].ravel())

                    # pub point
                    rosPoint = Point32()
                    rosPoint.x = world_points[0][0]
                    rosPoint.y = world_points[0][1]
                    rosPoint.z = world_points[0][2]
                    self.pub_point.publish(rosPoint)

            else:
                # pub point
                rosPoint = Point32()
                self.pub_point.publish(rosPoint)
                print('!!!! Cant track ', 'left_num:', left_num, 'right_num:', right_num)

            # mix to show on one picture
            vis = np.concatenate((frame_left, frame_right), axis=1)
            if(self.showFlag):
                cv2.imshow('vis', vis)
                # cv2.waitKey(100)

            # kevin ros publish
            # cvImage = bridge.cv2_to_imgmsg(cvImage, encoding='passthrough')
            cvImage = self.bridge.cv2_to_imgmsg(vis, 'bgr8')
            self.pub_cvimg.publish(cvImage)
            

if __name__=="__main__": 
    ros_stero_light_track = steroIrTrack()