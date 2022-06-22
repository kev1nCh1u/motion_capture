
# py3
import socket
import numpy as np
import struct
import time
import cv2

import os
import sys
sys.path.append(os.getcwd())
# from lib.kevin.kevincv import  *
# from lib.kevin import kevinuart
# from src.image_processing.kevinVision.get_data_3d import *
# from src.image_processing.kevinVision.point_segment import *
# from src.image_processing.kevinVision.find_body import *
from src.image_processing.kevinVision.main import *

UDP_IP = "192.168.1.71"
UDP_PORT = 8777

###########################################################################
# set point
##########################################################################
# point = np.zeros((10,7),np.float32) # px,py,pz,rx,ry,rz,v
# point[0] = [162.14,435.47,321.36,178.20,2.61,162.09,100]
# point[1] = [-157.09,435.93,317.14,179.01,2.37,162.09,100]

# for j in range(2):
#     message = b""
#     for i in range(7):
#         message += struct.pack('f', point[j][i])

#     print("UDP target IP: %s" % UDP_IP)
#     print("UDP target port: %s" % UDP_PORT)
#     print("message: %s" % message)

#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
#     sock.sendto(message, (UDP_IP, UDP_PORT))

#     time.sleep(1)

###########################################################################
# load path
##########################################################################
fs = cv2.FileStorage("src/robot_arm/robot_path.yaml", cv2.FILE_STORAGE_READ)
path = fs.getNode("path").mat()

print(path[1])
path_size = len(path)
print(path_size)

m = Main()

for j in range(path_size):
    print("===========================================")
    message = b""
    print("loop", j)
    print("point", path[j])
    for i in range(7):
        message += struct.pack('f', path[j][i])

    # print("UDP target IP: %s" % UDP_IP)
    # print("UDP target port: %s" % UDP_PORT)
    # print("message: %s" % message)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message, (UDP_IP, UDP_PORT))

    time.sleep(1)

    print("Geting data...")
    while(1):
        m.run()
        if(m.mainCounter > 5):
            m.mainCounter = 0
            break
    print("Get finish!")