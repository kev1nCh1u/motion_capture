
# py3
import socket
import numpy as np
import struct
import time
import cv2

import os
import sys
sys.path.append(os.getcwd())
from src.image_processing.kevinVision.main import *

UDP_IP = "192.168.1.71"
UDP_PORT = 8777

# load path
fs = cv2.FileStorage("src/robot_arm/robot_path.yaml", cv2.FILE_STORAGE_READ)
path = fs.getNode("path").mat()
print(path[1])
path_size = len(path)
print(path_size)

m = Main() # kevinVision

# send path to robot
for j in range(path_size):
    print("===========================================")
    message = b""
    print("loop", j)
    print("point", path[j])
    for i in range(7):
        message += struct.pack('f', path[j][i])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message, (UDP_IP, UDP_PORT))

    time.sleep(1) # wait robot move

    print("Geting data...")
    while(1):
        m.run() # get point
        if(m.mainCounter > 5): # get 5 point
            m.mainCounter = 0
            break
    print("Get finish!")