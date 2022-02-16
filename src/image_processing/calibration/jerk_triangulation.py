import numpy as np
import cv2
import glob

# Left Camera K (3x3)
LeftK = np.array([[1886.09907114703, 0, 740.881371463211],
                  [0.000000, 1883.73310107344, 573.348765257187],
                  [0.000000, 0.000000, 1.000000]])

# Left Camera RT (3x4)
LeftRT = np.array([[1.0, 0.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0, 0.0],
                   [0.0, 0.0, 1.0, 0.0]])

# Right Camera K (3x3)
RightK = np.array([[1899.97164211750, 0, 700.462865085791],
                   [0.000000, 1902.74841018126, 526.845770717539],
                   [0.000000, 0.000000, 1.000000]])

# Right Camera RT (3x4)
RightRT = np.array([[0.907699508606132, 0.00171054178168099, 0.419617297216165, -173.236661190924],
                    [-0.0106806044772735, 0.999761894031322,
                        0.0190283980120372, -0.834681394841576],
                    [-0.419484834963299, -0.0217538339084765, 0.907501649555579, 31.8693000200963]])

# Fundamental Matrix (3x3)
F21 = np.array([[5.69344155142857e-06, -1.76202603713881e-05, -0.00825032550164457],
                [-6.24154857112544e-05, -5.21356657784729e-06, 0.237597781705927],
                [0.0426277461462529, -0.205980375034528, -6.84003651282110]])

# 透過兩張照片的像素點以及投影矩陣 就能透過這三角化函數求出三維座標點


def Triangulation(x1, x2, P1, P2):
    # 將公式中的各個項目填入矩陣A中
    u1 = x1[0]
    v1 = x1[1]
    u2 = x2[0]
    v2 = x2[1]
    A = np.array([u1*P1[2]-P1[0],
                  v1*P1[2]-P1[1],
                  u2*P2[2]-P2[0],
                  v2*P2[2]-P2[1]], dtype='float32')

    # SVD求解後取V的最後一行為最小二乘解
    U, sigma, VT = np.linalg.svd(A)
    V = VT.transpose()
    X = V[:, -1]
    X = X / X[3]
    return X


img1 = cv2.imread('./left2.jpg', 0)
img2 = cv2.imread('./right2.jpg', 0)

pts1 = np.array([[731, 432]])
pts2 = np.array([[1112, 415]])

P1 = np.dot(LeftK, LeftRT)
P2 = np.dot(RightK, RightRT)
x1 = pts1[0]
x2 = pts2[0]

X = Triangulation(x1, x2, P1, P2)
print(X)

# x = np.dot(P1, X)
# x = x / x[2]
# print(x)
# x = np.dot(P2, X)
# x = x / x[2]
# print(x)

# points = cv2.triangulatePoints(P1,P2,x1,x2)
# print(points)
# print((points[0:3,:]/points[3,:]))

# cv2.imshow("img3", img3)
# cv2.imshow("img4", img4)
# cv2.imshow("img5", img5)
# cv2.imshow("img6", img6)
# cv2.waitKey(0)
