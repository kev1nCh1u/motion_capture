from cgi import print_arguments
import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *


########################################## load yaml param
fs = cv2.FileStorage(
    "data/parameter/matlab_stereo_param.yaml", cv2.FILE_STORAGE_READ)

FundamentalMatrix = fs.getNode("FundamentalMatrix").mat()
# print("FundamentalMatrix:",FundamentalMatrix)

##################################### imread
path = "data/stereo_calibration/new/"
fname = str(15) + ".jpg"
frame_left = cv2.imread(path + '1/' + fname)
frame_right = cv2.imread(path + '2/' + fname)

# point2d = np.array(([479,319],[538,217],[429,248],[557,296]))
point2d = np.array(([538,216],[479,217],[429,248],[557,296]))
point2d_2 = np.array(([579,225],[619,225],[542,251],[633,290]))

for i in range(len(point2d)):
    cv2.circle(frame_right, tuple(point2d[i]), 5, (0, 0, 255), -1)
    cv2.circle(frame_left, tuple(point2d_2[i]), 5, (0, 0, 255), -1)
    point = np.array([[point2d[i][0],point2d[i][1],1]])
    point_2 = np.array([[point2d_2[i][0],point2d_2[i][1],1]])

    linePoint = epipolar_line(FundamentalMatrix, point, 640, 0, 1)
    cv2.line(frame_left, (0, int(linePoint[0])), (640, int(linePoint[640-1])), 
        (0, 255, 0), 1)
    epipolarPoint = epipolar_line(FundamentalMatrix, point, 0, 1, 1)

    linePoint_2 = epipolar_line(FundamentalMatrix, point_2, 640, 0, 0)
    cv2.line(frame_right, (0, int(linePoint_2[0])), (640, int(linePoint_2[640-1])), 
        (0, 255, 0), 1)    
    epipolarPoint_2 = epipolar_line(FundamentalMatrix, point_2, 0, 1, 0)

    print(epipolarPoint, epipolarPoint_2)

    text = "p" + str(i) + " " + str(point[0][:2]) + str(round(epipolarPoint[0])) + " " + str(point_2[0][:2]) + str(round(epipolarPoint_2[0]))
    cv2.putText(frame_left, text,
            (10, 40+i*40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

# gap = 50
# for i in range(0,480,gap):
#     point = np.array([[300,i,1]])
#     linePoint = epipolar_line(FundamentalMatrix, point, 640, 1)
#     cv2.line(frame_left, (0, int(linePoint[0])), (640, int(linePoint[640-1])), 
#         (0, 255, 0), 1)
# for i in range(0,480,gap):
#     point = np.array([[300,i,1]])
#     linePoint = epipolar_line(FundamentalMatrix, point, 640, 0)
#     cv2.line(frame_right, (0, int(linePoint[0])), (640, int(linePoint[640-1])), 
#         (0, 255, 0), 1)


# mix to show on one picture
vis = np.concatenate((frame_left, frame_right), axis=1)

# Show the frames
cv2.imshow("vis SubPix" + fname, vis)

# Hit "q" to close the window
inputKey = cv2.waitKey(0) & 0xFF