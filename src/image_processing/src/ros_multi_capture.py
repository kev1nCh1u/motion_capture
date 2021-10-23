########################################################################################
# multi_capture
# by kevin
########################################################################################
import cv2
import numpy as np
import yaml
import glob
import time
import argparse

# kevin import ros
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

print('\n opencv version:', cv2.__version__)

########################################################################################
# define
########################################################################################
save_path = 'img/stereo_calibration/new/'
capture_num = 0
camera_num = 0
frame = np.zeros((camera_num,480,640,3), np.uint8)
bridge = CvBridge()

########################################################################################
# getImage
########################################################################################
def getImage(data, arg=0):
    img = bridge.imgmsg_to_cv2(data.data, desired_encoding='passthrough')
    cv2.imshow('img', img)
    cv2.waitKey(1)

    # print(frame[arg])

########################################################################################
# saveImage
########################################################################################
def saveImage(data):
    current_time = time.time()
    
    for i in range(camera_num):
        cv2.imwrite(save_path + '1/' + "{0:0=2d}".format(capture_num)+ '.jpg', frame[i])

    print('save:', save_path , str(int(current_time)), "{0:0=2d}".format(i))
    capture_num += 1

########################################################################################
# main
########################################################################################
def main():
    global frame

    # kevin args
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--camera_num", default=2, help="1,2,...")
    args = parser.parse_args()
    camera_num = args.camera_num
    frame = np.zeros((camera_num,480,640,3), np.uint8)

    # kevin ros
    rospy.init_node('multi_capture', anonymous=False)
    print(rospy.get_name())
    pub = rospy.Publisher(rospy.get_name()+'/image', Image)
    for i in range(camera_num):
        rospy.Subscriber('camera_'+ str(i) + '/image', Image, getImage, i)
    rospy.Subscriber('/trigger', Bool, saveImage)

    rospy.spin()

########################################################################################
# MultiCapture
########################################################################################
class MultiCapture:

    camera_num = 0
    frame = np.zeros((camera_num,480,640,3), np.uint8)
    save_path = 'img/stereo_calibration/new/'
    save_num = 1
    bridge = CvBridge()

    ########################################################################################
    # __init__
    ########################################################################################
    def __init__(self):
        # kevin args
        parser = argparse.ArgumentParser()
        parser.add_argument("-n", "--camera_num", default=2, help="1,2,...")
        args = parser.parse_args()

        # set value
        self.camera_num = args.camera_num
        self.frame = np.zeros((self.camera_num,480,640,3), np.uint8)

        # kevin ros
        rospy.init_node('multi_capture', anonymous=False)
        print(rospy.get_name())
        for i in range(self.camera_num):
            rospy.Subscriber('camera_'+ str(i) + '/image', Image, self.getImage, i)
        rospy.Subscriber('/trigger', Bool, self.saveImage)

        rospy.spin()

    ########################################################################################
    # getImage
    ########################################################################################
    def getImage(self, data, arg=0):
        img = self.bridge.imgmsg_to_cv2(data, desired_encoding='8UC3')
        self.frame[arg] = img


    ########################################################################################
    # saveImage
    ########################################################################################
    def saveImage(self, data):
        current_time = time.time()
        
        for i in range(self.camera_num):
            cv2.imwrite(self.save_path + str(i+1) + '/' + "{0:0=2d}".format(self.save_num)+ '.jpg', self.frame[i])
            print('save:', self.save_path + str(i+1) , str(int(current_time)), "{0:0=2d}".format(self.save_num))
        self.save_num += 1


if __name__=="__main__": 
    multi_capture = MultiCapture()