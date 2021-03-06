import serial
import numpy as np
import time

class UartControl():
    def __init__(self, port='/dev/ttyUSB0', rate=115200) -> None:
        print("Start UartControl...", port)
        self.port = port

        self.status = 0
        self.error = 0
        self.pointSize = 8
        self.count = 0

        self.data = np.empty([10], dtype='bytes')

        self.pointx_bytes = np.full(self.pointSize, b'\xffff')
        self.pointy_bytes = np.full(self.pointSize, b'\xffff')

        self.point2d = np.zeros((self.pointSize, 2),np.double)
        
        COM_PORT = port
        BAUD_RATES = rate
        try:
            self.ser = serial.Serial(COM_PORT, BAUD_RATES, bytesize=8,
                                stopbits=1, timeout=0.0001)
        except:
            self.error = 1
            print(COM_PORT,"error")

    def uart_ser(self):
        try:
            if(self.error == 0):
                while self.ser.in_waiting:
                    ###################### start
                    if(self.status == 0):
                        if(self.ser.read(1) ==  b'S'):
                            self.status += 1
                        else:
                            self.status = 0

                    # ####################### point
                    elif(self.status == 1):
                        for i in range(self.pointSize):
                            self.data[1] = self.ser.read(1)
                            self.data[2] = self.ser.read(1)
                            self.pointx_bytes[i] = self.data[1] + self.data[2]

                            self.data[3] = self.ser.read(1)
                            self.data[4] = self.ser.read(1)
                            self.pointy_bytes[i] = self.data[3] + self.data[4]

                        self.status += 1
                    ######################### end
                    elif(self.status == 2):
                        if(self.ser.read(1) ==  b'E'):
                            self.status += 1
                            self.status = 0

                            for i in range(self.pointSize):
                                self.point2d[i,0] = int.from_bytes(self.pointx_bytes[i], "big") / 10.
                                self.point2d[i,1] = int.from_bytes(self.pointy_bytes[i], "big") / 10.

                            self.count = 0
                            for i in range(self.pointSize):
                                if self.point2d[i,0] >= 700 : self.point2d[i,0] = 0
                                if self.point2d[i,1] >= 700 : self.point2d[i,1] = 0
                                if self.point2d[i,0] != 0 : self.count += 1
                        else:
                            self.status = 0
                    # self.ser_write()
            else:
                # print("serial error! " + self.port)
                pass

        except KeyboardInterrupt:
            self.ser.close()
            print('close...')


    def ser_write(self, colorFlag=0, binaryThreshold=150):
        if(self.error == 0):
            self.ser.write(b'\x53') #S
            self.ser.write(b'\x54') #T

            if(colorFlag == 1):
                self.ser.write(b'\x01') # binary
            elif(colorFlag == 0):
                self.ser.write(b'\x00') # RGB

            if(binaryThreshold < 50):
                binaryThreshold = 50
            if(binaryThreshold > 250):
                binaryThreshold = 250 

            self.ser.write((binaryThreshold).to_bytes(1, byteorder='little')) #binaryThreshold

            self.ser.write(b'\x45') #E
            self.ser.write(b'\x4E') #N
            self.ser.write(b'\x44') #D
        else:
            print("serial error")


###################################################################################
# test main
###################################################################################
if __name__ == "__main__":
    uc = UartControl()
    while 1:
        start_time = time.time()
        uc.uart_ser()

        # uc.ser_write(0)

        print("c:"+str(uc.count), end=' ')
        for i in range(4):
            print("p"+str(i), uc.point2d[i,0],uc.point2d[i,1], end=' ')
        print()

        print("\n--- total %s seconds ---" % (time.time() - start_time))
        
        # exit()