
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
# fs = cv2.FileStorage("src/robot_arm/robot_path_heart.yaml", cv2.FILE_STORAGE_READ)
fs = cv2.FileStorage("src/robot_arm/robot_path_grid.yaml", cv2.FILE_STORAGE_READ)

path = fs.getNode("path").mat()

print(path[1])
path_size = len(path)
print(path_size)

###########################################################################
# send path
##########################################################################
for j in range(path_size):
    print("===========================================")
    message = b""
    print("point", path[j])
    for i in range(7):
        message += struct.pack('f', path[j][i])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message, (UDP_IP, UDP_PORT))

    time.sleep(0.001) # wait for robot
    input()