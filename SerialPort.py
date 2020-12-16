# This Python file uses the following encoding: utf-8
import serial
import re
import time
from serial.tools import list_ports
from threading import Thread


def findPorts():
    ''' Returns a list of ports, for example ['COM1', 'COM2'] '''
    ports = list(list_ports.comports())

    ret = []
    for port in ports:
        matchObj = re.match('COM[0-9]+', str(port))
        name = matchObj.group(0)
        ret.append(name)
    return ret

class SerialPort:
    def __init__(self, portName: str, callback):
        self.readCallback = callback

        self.__serialCom = serial.Serial()
        self.__serialCom.baudrate = 460800
        self.__serialCom.port = portName

        # prepare reading thread
        self.__continueReading = False
        self.__readingThread = Thread(target=self.__readFromPort, daemon=False)

    def setPortName(self, name: str):
        if self.__serialCom.is_open:
            self.close()
        self.__serialCom.port = name

    def getPortName(self):
        return self.__serialCom.port

    def close(self):
        self.stopReading()
        self.__serialCom.close()

    # open by deafult starts reading from the port
    def open(self):
        self.__serialCom.open()
        if not self.__serialCom.is_open:
            raise SerialException('Port can not be open')
        DEBUG_LOG('Port is now open')
        self.startReading()

    def write(self, data: str):
        self.__serialCom.write(str.encode(data))
        DEBUG_LOG('Written: ', data)

    def startReading(self):
        self.__continueReading = True
        self.__readingThread.start()
        DEBUG_LOG('Reading started')

    def stopReading(self):
        DEBUG_LOG('Stop reading requested')
        self.__continueReading = False
        # cancel reading from another thread
        self.__serialCom.cancel_read()
        if self.__readingThread.is_alive():
            self.__readingThread.join()
            DEBUG_LOG('Reading thread joined')


    def __readFromPort(self):
        # read with no timeout - wait indefinitely
        self.__serialCom.timeout = None

        numOfBytes = 0
        while self.__continueReading:
            byte = self.__serialCom.read(size=1)
            hexByte = str(byte.hex())
            if hexByte != '':
                numOfBytes += 1
                # something has been read, call the callback function
                DEBUG_LOG('Read!', numOfBytes, 'Data = 0x', hexByte)
                self.readCallback(byte)


def DEBUG_LOG(*args):
    global DEBUG
    if DEBUG:
        print(*args)


if __name__ == "__main__":
    DEBUG = True
    ser = SerialPort("COM3", lambda x: DEBUG_LOG('callback called'))
    ser.open()

    ser.write('UCI(0x20,0x02,0x00,0x00);')
    time.sleep(2)
    ser.write('UCI(0x20,0x02,0x00,0x00);')
    time.sleep(2)
    ser.close()
