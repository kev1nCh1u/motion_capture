import imp
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys

import os
import importlib
sys.path.append(os.getcwd())
from lib.kevin import kevinuart

from time import sleep
import numpy as np

class Ui(QtWidgets.QMainWindow):
    def __init__(self):

        super(Ui, self).__init__()
        uic.loadUi('src/gui/qt_gui/ui/main.ui', self)

        ############################ uart
        try:
            self.uc = kevinuart.UartControl('/dev/ttyUSB0') # kevin uart
            self.uc1 = kevinuart.UartControl('/dev/ttyUSB1') # kevin uart
            print("Connect port success...")
        except:
            print('\033[91m'+"Error cannot connect port!!!"+'\033[0m')
        

        self.timer = QTimer() # call QTimer 
        self.timer.timeout.connect(self.timer_callback) # if time run
        self.timer.start(10) # start Timer ms

        # sleep(3)

        self.show()

        self.pushButton.clicked.connect(self.btn_callback)
        self.pushButton_2.clicked.connect(self.btn2_callback)
        # self.pushButton_3.clicked.connect(self.btn3_callback)

    def timer_callback(self):
        # print("timer_callback")
        self.uc.uart_ser() # right
        self.uc1.uart_ser() # left
        strVal_3d = "x:" + "y:" + "z:"

        self.label.setText(str(strVal_3d))
        self.label_12.setText("x:" + str(self.uc.point2d[0,0]) + " y:" + str(self.uc.point2d[0,1]))
        self.label_13.setText("x:" + str(self.uc.point2d[1,0]) + " y:" + str(self.uc.point2d[1,1]))
        self.label_14.setText("x:" + str(self.uc.point2d[2,0]) + " y:" + str(self.uc.point2d[2,1]))
        self.label_15.setText("x:" + str(self.uc.point2d[3,0]) + " y:" + str(self.uc.point2d[3,1]))
        self.label_16.setText("x:" + str(self.uc1.point2d[0,0]) + " y:" + str(self.uc1.point2d[0,1]))
        self.label_17.setText("x:" + str(self.uc1.point2d[1,0]) + " y:" + str(self.uc1.point2d[1,1]))
        self.label_18.setText("x:" + str(self.uc1.point2d[2,0]) + " y:" + str(self.uc1.point2d[2,1]))
        self.label_19.setText("x:" + str(self.uc1.point2d[3,0]) + " y:" + str(self.uc1.point2d[3,1]))
        self.label_4.setText(str(self.horizontalSlider.value()))

        self.graphicsView = QtWidgets.QGraphicsView()
        

    def btn_callback(self):
        strVal = "color"
        print(strVal)
        self.label_2.setText(str(strVal))
        self.uc.ser_write(0)
        self.uc1.ser_write(0)
    def btn2_callback(self):
        strVal = "binary"
        print(strVal)
        self.label_2.setText(str(strVal))
        binaryThreshold = self.horizontalSlider.value()
        self.uc.ser_write(1, binaryThreshold)
        self.uc1.ser_write(1, binaryThreshold)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()