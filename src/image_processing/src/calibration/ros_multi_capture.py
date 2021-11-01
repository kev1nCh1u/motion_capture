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
            rospy.Subscriber('camera_'+ str(i+1) + '/image', Image, self.getImage, i)
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

        if(self.save_num > 21):
            self.save_num = 1


if __name__=="__main__": 
    multi_capture = MultiCapture()