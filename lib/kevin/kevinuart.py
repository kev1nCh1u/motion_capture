import serial
import numpy as np


class UartControl():
    def __init__(self, port='/dev/ttyUSB0', rate=115200) -> None:
        pass
        print("Start UartControl...")

        self.status = 0
        self.error = 0

        self.data = np.empty([10], dtype='bytes')
        self.point_x_bytes_0 = b''
        self.point_y_bytes_0 = b''
        self.point_x_bytes_1 = b''
        self.point_y_bytes_1 = b''
        self.point_x_bytes_2 = b''
        self.point_y_bytes_2 = b''
        self.point_x_bytes_3 = b''
        self.point_y_bytes_3 = b''

        self.point2d = np.zeros((4, 2),np.unsignedinteger)
        
        COM_PORT = port
        BAUD_RATES = rate
        try:
            self.ser = serial.Serial(COM_PORT, BAUD_RATES, bytesize=8,
                                stopbits=1, timeout=0.01)
        except:
            self.error = 1
            print(COM_PORT,"error")

    def uart_ser(self):
        try:
            while self.ser.in_waiting:
                ###################### start
                if(self.status == 0):
                    if(self.ser.read(1) ==  b'S'):
                        self.status += 1
                    else:
                        self.status = 0
                elif(self.status == 1):
                    if(self.ser.read(1) ==  b'T'):
                        self.status += 1
                    else:
                        self.status = 0
                ###################### point 0
                elif(self.status == 2):
                    self.data[1] = self.ser.read(1)
                    self.data[2] = self.ser.read(1)
                    self.point_x_bytes_0 = self.data[1] + self.data[2]

                    self.data[3] = self.ser.read(1)
                    self.data[4] = self.ser.read(1)
                    self.point_y_bytes_0 = self.data[3] + self.data[4]
                ###################### point 1
                    self.data[1] = self.ser.read(1)
                    self.data[2] = self.ser.read(1)
                    self.point_x_bytes_1 = self.data[1] + self.data[2]

                    self.data[3] = self.ser.read(1)
                    self.data[4] = self.ser.read(1)
                    self.point_y_bytes_1 = self.data[3] + self.data[4]
                ####################### point 2
                    self.data[1] = self.ser.read(1)
                    self.data[2] = self.ser.read(1)
                    self.point_x_bytes_2 = self.data[1] + self.data[2]

                    self.data[3] = self.ser.read(1)
                    self.data[4] = self.ser.read(1)
                    self.point_y_bytes_2 = self.data[3] + self.data[4]
                ####################### point 3
                    self.data[1] = self.ser.read(1)
                    self.data[2] = self.ser.read(1)
                    self.point_x_bytes_3 = self.data[1] + self.data[2]

                    self.data[3] = self.ser.read(1)
                    self.data[4] = self.ser.read(1)
                    self.point_y_bytes_3 = self.data[3] + self.data[4]

                    self.status += 1
                ######################### end
                elif(self.status == 3):
                    if(self.ser.read(1) ==  b'E'):
                        self.status += 1
                    else:
                        self.status = 0
                elif(self.status == 4):
                    if(self.ser.read(1) ==  b'N'):
                        self.status += 1
                    else:
                        self.status = 0
                elif(self.status == 5):
                    if(self.ser.read(1) ==  b'D'):
                        self.status = 0
                        self.point2d[0,0] = int.from_bytes(self.point_x_bytes_0, "big")
                        self.point2d[0,1] = int.from_bytes(self.point_y_bytes_0, "big")
                        self.point2d[1,0] = int.from_bytes(self.point_x_bytes_1, "big")
                        self.point2d[1,1] = int.from_bytes(self.point_y_bytes_1, "big")
                        self.point2d[2,0] = int.from_bytes(self.point_x_bytes_2, "big")
                        self.point2d[2,1] = int.from_bytes(self.point_y_bytes_2, "big")
                        self.point2d[3,0] = int.from_bytes(self.point_x_bytes_3, "big")
                        self.point2d[3,1] = int.from_bytes(self.point_y_bytes_3, "big")
                        # print(self.point2d[0,0], self.point2d[0,1])

                        for i in range(4):
                            if self.point2d[i,0] == 65535 : self.point2d[i,0] = 0
                            if self.point2d[i,1] == 65535 : self.point2d[i,1] = 0
                    else:
                        self.status = 0
                # self.ser_write()

        except KeyboardInterrupt:
            self.ser.close()
            print('close...')


    def ser_write(self, colorFlag=0, binaryThreshold=150):
        self.ser.write(b'\x53') #S
        self.ser.write(b'\x54') #T

        if(colorFlag == 1):
            self.ser.write(b'\x01') # binary
        elif(colorFlag == 0):
            self.ser.write(b'\x00') # RGB

        self.ser.write((binaryThreshold).to_bytes(1, byteorder='little')) #binaryThreshold

        self.ser.write(b'\x45') #E
        self.ser.write(b'\x4E') #N
        self.ser.write(b'\x44') #D


###################################################################################
# test main
###################################################################################
if __name__ == "__main__":
    uc = UartControl()
    while 1:
        uc.uart_ser()

        uc.ser_write(1)

        for i in range(4):
            print("p"+str(i), uc.point2d[i,0],uc.point2d[i,1], end='\t')
        print()
        
        # exit()