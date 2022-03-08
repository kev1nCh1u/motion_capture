import serial
import numpy as np


class UartControl():
    point_x = 0
    point_y = 0
    def __init__(self, port='/dev/ttyUSB0', rate=115200) -> None:
        pass
        print("Start UartControl...")

        self.status = 0

        self.data = np.empty([10], dtype='bytes')
        self.point_x_bytes = b''
        self.point_y_bytes = b''
        
        COM_PORT = port
        BAUD_RATES = rate
        self.ser = serial.Serial(COM_PORT, BAUD_RATES, bytesize=8,
                            stopbits=1, timeout=0.01)

    def uart_ser(self):
        try:
            while self.ser.in_waiting:
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
                elif(self.status == 2):
                    self.data[1] = self.ser.read(1)
                    self.data[2] = self.ser.read(1)
                    self.point_x_bytes = self.data[1] + self.data[2]

                    self.data[3] = self.ser.read(1)
                    self.data[4] = self.ser.read(1)
                    self.point_y_bytes = self.data[3] + self.data[4]

                    self.status += 1
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
                        self.point_x = int.from_bytes(self.point_x_bytes, "big")
                        self.point_y = int.from_bytes(self.point_y_bytes, "big")
                        # print(self.point_x, self.point_y)
                    else:
                        self.status = 0
                # self.ser_write()

        except KeyboardInterrupt:
            self.ser.close()
            print('close...')


    def ser_write(self, flag=0):
        self.ser.write(b'\x53') #S
        self.ser.write(b'\x54') #T

        if(flag == 1):
            self.ser.write(b'\x01')
        elif(flag == 0):
            self.ser.write(b'\x00')

        self.ser.write(b'\x45') #E
        self.ser.write(b'\x4E') #N
        self.ser.write(b'\x44') #D



if __name__ == "__main__":
    uc = UartControl()
    while 1:
        uc.uart_ser()
        print(uc.point_x,uc.point_y)
        uc.ser_write(0)
        exit()