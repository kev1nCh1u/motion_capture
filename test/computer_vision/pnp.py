# # 需要導入模塊: import cv2 [as 別名]
# # 或者: from cv2 import solvePnP [as 別名]
# import cv2
# import numpy as np
# def pnp(points_3D, points_2D, cameraMatrix):
#     try:
#         distCoeffs = pnp.distCoeffs
#     except:
#         distCoeffs = np.zeros((8, 1), dtype='float32')

#     assert points_2D.shape[0] == points_2D.shape[0], 'points 3D and points 2D must have same number of vertices'

#     _, R_exp, t = cv2.solvePnP(points_3D,
#                               # points_2D,
#                               np.ascontiguousarray(points_2D[:,:2]).reshape((-1,1,2)),
#                               cameraMatrix,
#                               distCoeffs)
#                               # , None, None, False, cv2.SOLVEPNP_UPNP)

#     R, _ = cv2.Rodrigues(R_exp)
#     return R, t 


# -*- coding: utf-8 -*-
# 測試使用opencv中的函數solvepnp
import cv2
import numpy as np
tag_size = 0.05
tag_size_half = 0.025
fx = 610.32366943
fy = 610.5026245
cx = 313.3859558
cy = 237.2507269
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0, 0, 1]], dtype=np.float64)
objPoints = np.array([[-tag_size_half, -tag_size_half, 0],
                      [tag_size_half, -tag_size_half, 0],
                      [tag_size_half, tag_size_half, 0],
                      [-tag_size_half, tag_size_half, 0]], dtype=np.float64)
imgPoints = np.array([[608, 167], [514, 167], [518, 69], [611, 71]], dtype=np.float64)
cameraMatrix = K
distCoeffs = None
retval,rvec,tvec  = cv2.solvePnP(objPoints, imgPoints, cameraMatrix, distCoeffs)
# cv2.Rodrigues()
print(retval, rvec, tvec)