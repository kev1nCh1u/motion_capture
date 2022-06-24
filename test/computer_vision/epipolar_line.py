import cv2
import numpy as np
from pyparsing import line


def main():
    ########################################## load yaml param
    fs = cv2.FileStorage(
        "data/parameter/matlab_stereo_param.yaml", cv2.FILE_STORAGE_READ)

    FundamentalMatrix = fs.getNode("FundamentalMatrix").mat()
    print("FundamentalMatrix:",FundamentalMatrix)
    
    ##################################### a point
    point = np.array([[600,600,1]])
    print("point", point)
    print("point.T", point.T)

    ###################################### line equation
    lineEq = np.dot(FundamentalMatrix, point.T)
    print("lineEq", lineEq)

    a = lineEq[0]
    b = lineEq[1]
    c = lineEq[2]

    ####################################### find y ax+by+c=0
    frameSize = 10
    x = np.array(range(frameSize))
    print("x", x)
    y = -(a*x+c)/b
    print("y", y)
    # for x in range(frameSize):
    #     y = -(a*x-c)/b
    #     print(y)


# if main
if __name__ == '__main__':
    main()