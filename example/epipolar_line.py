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
frame_left = cv2.imread(path + '2/' + fname)
frame_right = cv2.imread(path + '1/' + fname)

##################################### input point
# point2d = np.array(([479,319],[538,217],[429,248],[557,296]))
point2d = np.array(([538,100],[479,100],[429,300],[557,400]))
point2d_2 = np.array(([579,100],[619,100],[542,300],[633,400]))

##################################### sorting
print(point2d)
point2d = np.sort(point2d.view('i8,i8'), order=['f1'], axis=0).view(np.int64)
print(point2d)

for i in range(len(point2d)):
    ##################################### point read
    cv2.circle(frame_right, tuple(point2d[i]), 5, (0, 0, 255), -1)
    cv2.circle(frame_left, tuple(point2d_2[i]), 5, (0, 0, 255), -1)
    point = np.array([[point2d[i][0],point2d[i][1],1]])
    point_2 = np.array([[point2d_2[i][0],point2d_2[i][1],1]])

    ######################################## epipolar_line to left
    linePoint = epipolar_line(FundamentalMatrix, point, 640, 0, 0) # line
    cv2.line(frame_left, (0, int(linePoint[0])), (640, int(linePoint[640-1])), 
        (0, 255, 0), 1) # draw line
    epipolarPoint = epipolar_line(FundamentalMatrix, point, 0, 1, 0) # point

    ######################################## epipolar_line to right
    linePoint_2 = epipolar_line(FundamentalMatrix, point_2, 640, 0, 1) # line
    cv2.line(frame_right, (0, int(linePoint_2[0])), (640, int(linePoint_2[640-1])), 
        (0, 255, 0), 1) # draw line
    epipolarPoint_2 = epipolar_line(FundamentalMatrix, point_2, 0, 1, 1) # point

    ######################################## show result
    print(epipolarPoint, epipolarPoint_2)

    text = "p" + str(i) + " " + str(point[0][:2]) + str(round(epipolarPoint[0])) + " " + str(point_2[0][:2]) + str(round(epipolarPoint_2[0]))
    cv2.putText(frame_left, text,
            (10, 40+i*40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

######################################## epipolar_line in gap
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


######################################## image show
# mix to show on one picture
vis = np.concatenate((frame_left, frame_right), axis=1)

# Show the frames
cv2.imshow("vis SubPix" + fname, vis)

# Hit "q" to close the window
inputKey = cv2.waitKey(0) & 0xFF