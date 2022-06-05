from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
import sys
import cv2

import os
import importlib
sys.path.append(os.getcwd())
from lib.kevin import kevinuart

from time import sleep
import numpy as np

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        
        ##################### init value
        self.image_path = 'data/stereo_calibration/test/'
        self.image_count = 1

        super(Ui, self).__init__()
        uic.loadUi('src/gui/qt_gui/main.ui', self)

        ############################ uart
        try:
            self.uc = kevinuart.UartControl('/dev/ttyUSB0') # kevin uart
            self.uc1 = kevinuart.UartControl('/dev/ttyUSB1') # kevin uart
            print("Connect port success...")
        except:
            print('\033[91m'+"Error cannot connect port!!!"+'\033[0m')

        ################################### camera
        self.cap = cv2.VideoCapture(4) # init camera
        self.cap2 = cv2.VideoCapture(2)
        
        ######################################## qt
        self.timer = QTimer() # call QTimer 
        self.timer.timeout.connect(self.timer_callback) # if time run
        self.timer.start(10) # start Timer ms

        self.pushButton.clicked.connect(self.btn_callback)
        self.pushButton_2.clicked.connect(self.btn2_callback)
        self.pushButton_3.clicked.connect(self.btn3_callback)

        # sleep(3)
        self.show()

    def timer_callback(self):
        # print("timer_callback")

        ################################## uart
        self.uc.uart_ser() # right
        self.uc1.uart_ser() # left

        self.label.setText("x:" + "y:" + "z:")
        self.label_12.setText("x:" + str(self.uc.point2d[0,0]) + " y:" + str(self.uc.point2d[0,1]))
        self.label_13.setText("x:" + str(self.uc.point2d[1,0]) + " y:" + str(self.uc.point2d[1,1]))
        self.label_14.setText("x:" + str(self.uc.point2d[2,0]) + " y:" + str(self.uc.point2d[2,1]))
        self.label_15.setText("x:" + str(self.uc.point2d[3,0]) + " y:" + str(self.uc.point2d[3,1]))
        self.label_16.setText("x:" + str(self.uc1.point2d[0,0]) + " y:" + str(self.uc1.point2d[0,1]))
        self.label_17.setText("x:" + str(self.uc1.point2d[1,0]) + " y:" + str(self.uc1.point2d[1,1]))
        self.label_18.setText("x:" + str(self.uc1.point2d[2,0]) + " y:" + str(self.uc1.point2d[2,1]))
        self.label_19.setText("x:" + str(self.uc1.point2d[3,0]) + " y:" + str(self.uc1.point2d[3,1]))
        
        #################################### camera
        camFlag, self.image = self.cap.read()
        if(camFlag):
            show = cv2.resize(self.image,(320,240))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
            self.label_6.setPixmap(QPixmap.fromImage(showImage))
        else:
            self.label_6.setText("No signal")

        camFlag2, self.image2 = self.cap2.read()
        if(camFlag2):
            show2 = cv2.resize(self.image2,(320,240))
            show2 = cv2.cvtColor(show2, cv2.COLOR_BGR2RGB)
            showImage2 = QImage(show2.data, show2.shape[1],show2.shape[0],QImage.Format_RGB888)
            self.label_22.setPixmap(QPixmap.fromImage(showImage2))
        else:
            self.label_22.setText("No signal")
        

    def btn_callback(self):
        self.label_2.setText(self.comboBox.currentText())
        self.label_4.setText(str(self.spinBox.value()))
        binaryThreshold = self.spinBox.value()
        if(self.comboBox.currentText() == "binary"): color = 1
        else: color = 0
        self.uc.ser_write(color, binaryThreshold)
        self.uc1.ser_write(color, binaryThreshold)
    def btn2_callback(self):
        cv2.imwrite(self.image_path + '1/' + "{0:0=2d}".format(self.image_count)+ '.jpg', self.image)
        cv2.imwrite(self.image_path + '2/' + "{0:0=2d}".format(self.image_count)+ '.jpg', self.image2)
        self.label_23.setText("save:"+self.image_path + str(self.image_count))
        self.image_count += 1
    def btn3_callback(self):
        self.image_count = 1
        self.label_23.setText("save:"+self.image_path + str(self.image_count))

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()