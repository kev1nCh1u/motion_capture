import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import  *
from lib.kevin import kevinuart


###################################################################################
# main
###################################################################################
def main():
    ########################################### uart
    kuc = kevinuart.UartControl('/dev/ttyUSB0') # right camera
    kuc1 = kevinuart.UartControl('/dev/ttyUSB1') # left camera
    
    # binary thres:50 100
    kuc.ser_write(0, 50) 
    kuc1.ser_write(0, 50)

    while 1:
        ########################################## read_uart
        kuc.uart_ser() # right camera
        kuc1.uart_ser() # left camera

        ########################################### get_point 
        point2d_1 = kuc.point2d
        point2d_2 = kuc1.point2d
        for i in range(4):
            print("p"+str(i), point2d_1[i,0],point2d_1[i,1],point2d_2[i,0],point2d_2[i,1], end=' ')
        print()

        break


# if main
if __name__ == '__main__':
    main()
