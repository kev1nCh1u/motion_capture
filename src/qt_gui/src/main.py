import imp
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys

import uart

class Ui(QtWidgets.QMainWindow):
    def __init__(self):

        super(Ui, self).__init__()
        uic.loadUi('src/qt_gui/ui/main.ui', self)

        ############################ uart
        try:
            self.uc = uart.UartControl('/dev/ttyUSB0') # kevin uart
            # self.uc = uart.UartControl('/dev/ttyUSB1') # kevin uart
            print("Connect port success...")
        except:
            print("Error cannot connect port!")
        

        self.timer = QTimer() # call QTimer 
        self.timer.timeout.connect(self.timer_callback) # if time run
        self.timer.start(10) # start Timer ms

        self.show()

        self.pushButton.clicked.connect(self.btn_callback)
        self.pushButton_2.clicked.connect(self.btn2_callback)
        # self.pushButton_3.clicked.connect(self.btn3_callback)

    def timer_callback(self):
        # print("timer_callback")
        self.uc.uart_ser()
        strVal = "x:" + str(self.uc.point_x) + " y:" + str(self.uc.point_y)
        self.label.setText(str(strVal))

    def btn_callback(self):
        strVal = "color"
        print(strVal)
        self.label_2.setText(str(strVal))
        self.uc.ser_write(0)
    def btn2_callback(self):
        strVal = "binary"
        print(strVal)
        self.label_2.setText(str(strVal))
        self.uc.ser_write(1)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()