
# py3
import socket
import numpy as np
import struct
import time
import cv2

UDP_IP = "192.168.1.71"
UDP_PORT = 8777

###########################################################################
# set path
##########################################################################
path_size = 2
path = np.zeros((10,7),np.float32) # px,py,pz,rx,ry,rz,v
path[0] = [36.86,241.26,486.47,180,0,-90,100]
path[1] = [-131.85,231.03,239.22,180,0,-90,100]

###########################################################################
# send path
##########################################################################
while 1:
    for j in range(path_size):
        print("===========================================")
        message = b""
        print("point", path[j])
        for i in range(7):
            message += struct.pack('f', path[j][i])

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(message, (UDP_IP, UDP_PORT))

        time.sleep(0.1) # wait for robot
        # input()