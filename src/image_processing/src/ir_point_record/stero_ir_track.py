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
        parser.add_argument("-cf", "--cap_flag", default=2, help="0 or 1")
        parser.add_argument("-r", "--camera_right", default=0, help="0,1,2...")
        parser.add_argument("-l", "--camera_left", default=1, help="0,1,2...")
        args = parser.parse_args()

        # define
        self.capFlag = args.cap_flag
        self.frame = np.zeros((2,480,640,3), np.uint8)
        self.baseline = 138.596414801303  # Distance between the cameras [mm]
        self.focalLength = 811.060887393561  # Camera lense's focal length [mm]
        self.bridge = CvBridge()

        # kevin ros
        rospy.init_node('stero_ir_track', anonymous=False)
        print(rospy.get_name())
        rospy.Subscriber('camera_'+ str(args.camera_right) + '/image', Image, self.getImage, args.camera_right)
        rospy.Subscriber('camera_'+ str(args.camera_left) + '/image', Image, self.getImage, args.camera_left)
        # rospy.Timer(rospy.Duration(2), self.timer_callback)

        # Camera parameters to undistort and rectify images
        cv_file = cv2.FileStorage()
        cv_file.open('param/stereoMap.xml', cv2.FileStorage_READ)
        self.stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
        self.stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
        self.stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
        self.stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

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
    def find_depth(self, left_point, right_point, frame_left, frame_right, baseline, f):

        height_right, width_right, depth_right = frame_right.shape
        height_left, width_left, depth_left = frame_left.shape

        if width_right == width_left:
            f_pixel = f
        else:
            print('Left and right camera frames do not have the same pixel width')

        x_left = left_point[0]
        x_right = right_point[0]

        # displacement between left and right frames [pixels]
        disparity = abs(x_left - x_right)
        zDepth = (baseline * f_pixel) / disparity            # z depth in [mm]

        return zDepth

    ###############################################################################################
    # calcu_world_point
    ###############################################################################################
    def calcu_world_point(self, x_cam, y_cam, z_depth, focal):

        # x_world = focal * x_cam / z_depth
        # y_world = focal * y_cam / z_depth

        x_world = (x_cam * z_depth) / focal
        y_world = (y_cam * z_depth) / focal

        return x_world, y_world

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
            left_point = ir_track.ir_track(frame_left, ).ravel()
            right_point = ir_track.ir_track(frame_right).ravel()
            # print('left_point:',left_point, 'right_point',right_point)

            # find depth and world point
            depth = self.find_depth(left_point, right_point, frame_left, frame_right, self.baseline, self.focalLength)
            depth = round(depth, 1)
            # print("Depth:", depth)
            text = "Dis: " + str(round(depth, 1))
            cv2.putText(frame_right, text,
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame_left, text,
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            x_world, y_world = self.calcu_world_point(left_point[0], left_point[1], depth, self.focalLength)
            x_world = round(x_world, 1)
            y_world = round(y_world, 1)
            # print('x_world, y_world :' , x_world, y_world)
            text = "X:" + str(round(x_world, 1)) + " Y:" + str(round(y_world, 1))
            cv2.putText(frame_left, text,
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame_right, text,
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            print('x:', x_world, 'y:', y_world, 'z:', depth)

            # # draw green line
            # imageSize = (np.shape(self.stereoMapL_x)[1], np.shape(self.stereoMapL_x)[0])
            # gap = 27
            # for i in range(1, int(imageSize[1] / gap) + 1):
            #     y = gap * i
            #     cv2.line(frame_left, (0, y), (imageSize[0], y), (0, 255, 0), 1)
            #     cv2.line(frame_right, (0, y), (imageSize[0], y), (0, 255, 0), 1)

            # # mix to show on one picture
            # vis = np.concatenate((frame_left, frame_right), axis=1)
            # cv2.imshow('vis', vis)
            # # cv2.waitKey(100)





if __name__=="__main__": 
    stero_ir_track = steroIrTrack()