########################################################################################
# multi_capture
# by kevin
########################################################################################
import cv2
from matplotlib.pyplot import cla
import numpy as np
import glob
import time
import threading


print('\n opencv version:', cv2.__version__)

save_path = 'data/stereo_calibration/new_triple/'

class MultiCapture():

    def __init__(self) -> None:
        pass
        ############################# Capture img
        print('videoCapture....')
        self.cap = cv2.VideoCapture(4) # left
        self.cap2 = cv2.VideoCapture(2) # mid
        self.cap3 = cv2.VideoCapture(6) # right
        # self.cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
        # self.cap2 = cv2.VideoCapture(4, cv2.CAP_DSHOW)
        # self.cap3 = cv2.VideoCapture(6, cv2.CAP_DSHOW)
        print('finish...\n')

        if not (self.cap.isOpened()):
            print("Could not open video device")
            exit()
        if not (self.cap2.isOpened()):
            print("Could not open video device 2")
            exit()
        if not (self.cap3.isOpened()):
            print("Could not open video device 3")
            exit()


    def readThread(self):
        t = threading.Thread(target = self.read)
        t.start()

    def read(self):
        ########################################################################################
        # read img
        ########################################################################################
        i = 1
        while(True):
            # catch time
            current_time = time.time()

            # 從攝影機擷取一張影像
            ret, frame = self.cap.read()
            ret2, frame2 = self.cap2.read()
            ret3, frame3 = self.cap3.read()

            # 顯示圖片
            cv2.imshow('frame', frame)
            cv2.imshow('frame2', frame2)
            cv2.imshow('frame3', frame3)
            
            inputKey = cv2.waitKey(1) & 0xFF

            # if s save image
            if inputKey == ord('s'):
                cv2.imwrite(save_path + '1/' + "{0:0=2d}".format(i)+ '.jpg', frame)
                cv2.imwrite(save_path + '2/' + "{0:0=2d}".format(i)+ '.jpg', frame2)
                cv2.imwrite(save_path + '3/' + "{0:0=2d}".format(i)+ '.jpg', frame3)

                print('save:', save_path , str(int(current_time)), "{0:0=2d}".format(i))
                i += 1

            # 若按下 q 鍵則離開迴圈
            if inputKey == ord('q'):
                break

        # 釋放攝影機
        self.cap.release()
        self.cap2.release()

        # 關閉所有 OpenCV 視窗
        cv2.destroyAllWindows()

if __name__ == "__main__":
    mc = MultiCapture()
    # mc.read()
    mc.readThread()
    print("MultiCapture...")