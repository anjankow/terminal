# This Python file uses the following encoding: utf-8
import serial


class SerialPort:
    def __init__(self, portName: str):
        self.serialCom = serial.Serial()
        self.serialCom.baudrate = 460800
        self.serialCom.port = portName
        self.serialCom.timeout = 0.5

    def close(self):
        self.serialCom.close()

    def open(self):
        self.serialCom.open()
        if not self.serialCom.is_open:
            raise SerialException('Port can not be open')

    def read(self):
        return self.serialCom.read_until()

    def write(self, data: str):
        self.serialCom.write(data)



if __name__ == "__main__":
    ser = SerialPort("COM12")
    ser.open()

    ser.write(str.encode('UCI(0x20,0x02,0x00,0x00);'))
    print('written, reading...')
    bytes = ser.read()
    for byte in bytes:
        print("This is byte: 0x", format(byte, 'x'))
