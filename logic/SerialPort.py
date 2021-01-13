# This Python file uses the following encoding: utf-8
import serial
import re
import time
from serial.tools import list_ports
from threading import Thread, Lock


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
    def __init__(self, portName: str, callback, debug=True):
        self.readCallback = callback

        self.__serialCom = serial.Serial()
        self.__serialCom.baudrate = 460800
        self.__serialCom.port = portName

        # prepare reading thread
        self.__continueReading = False
        self.__readingThread = None

        self.debug = debug
        self.__incomingBytesCnt = 0

        # lock to update number of read bytes
        self.dataLock = Lock()


    def __del__(self):
        self.close()


    def setPortName(self, name: str):
        if self.__serialCom.is_open:
            self.close()
        self.__serialCom.port = name

    def getPortName(self):
        return self.__serialCom.port

    def close(self):
        if self.__continueReading:
            self.stopReading()
        self.__serialCom.close()

    # open by deafult starts reading from the port
    def open(self):
        self.__serialCom.open()
        if not self.__serialCom.is_open:
            raise SerialException('Port can not be open')
        self.DEBUG_LOG('Port is now open')
        self.startReading()

    def write(self, data: str):
        self.__serialCom.write(str.encode(data))
        self.DEBUG_LOG('Written: ', data)

    def startReading(self):
        self.__incomingBytesCnt = 0
        self.__continueReading = True
        self.__readingThread = Thread(target=self.__readFromPort, daemon=False)
        self.__readingThread.start()
        self.DEBUG_LOG('Reading started')

    def stopReading(self):
        self.DEBUG_LOG('Stop reading requested')
        self.__continueReading = False
        # cancel reading from another thread
        self.__serialCom.cancel_read()
        if self.__readingThread.is_alive():
            self.__readingThread.join()
            self.DEBUG_LOG('Reading thread joined')


    def __readFromPort(self):
        # read with no timeout - wait indefinitely
        self.__serialCom.timeout = None

        while self.__continueReading:
            byte = self.__serialCom.read(size=1)
            hexByte = str(byte.hex())
            if hexByte != '':
                with self.dataLock:
                    self.__incomingBytesCnt += 1
                # something has been read, call the callback function
                self.DEBUG_LOG('Read! Data = 0x', hexByte)
                self.readCallback(hexByte)

    def getIncomingBytesCnt(self):
        with self.dataLock:
            num = self.__incomingBytesCnt
        return num


    def DEBUG_LOG(self, *args):
        if self.debug:
            print(*args)



if __name__ == "__main__":
    DEBUG = True
    ser = SerialPort("COM3", lambda x: self.DEBUG_LOG('callback called'))
    ser.open()

    ser.write('UCI(0x20,0x02,0x00,0x00);')
    time.sleep(2)
    ser.write('UCI(0x20,0x02,0x00,0x00);')
    time.sleep(2)
    ser.close()
