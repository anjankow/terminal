import sys
import serial
from threading import Lock
from threading import Thread

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QColor

from SerialPort import SerialPort, findPorts
from PortConfig import PortConfig

qtCreatorFile = "TerminalWin.ui"
Ui_TerminalWin, QtBaseClass = uic.loadUiType(qtCreatorFile)

CommandColor = QColor('#c6ffee')
ResponseColor = QColor('#fcfed4')
PortOpenedColor = 'rgb(199, 255, 147)'
PortClosedColor = 'rgb(177, 43, 43)'


class CommandGroup:
    def __init__(self, textEdit, sendButton, commandLabel):
        self.commandTextEdit = textEdit
        self.sendButton = sendButton
        self.commandLabel = commandLabel


class TerminalWin(QtWidgets.QMainWindow, Ui_TerminalWin):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_TerminalWin.__init__(self)
        self.setupUi(self)

        # initialize command groups
        self.commandGroups = [
            CommandGroup(self.plainTextEdit_0, self.sendButton_0, self.label_0),
            CommandGroup(self.plainTextEdit_1, self.sendButton_1, self.label_1),
            CommandGroup(self.plainTextEdit_2, self.sendButton_2, self.label_2),
            CommandGroup(self.plainTextEdit_3, self.sendButton_3, self.label_3),
            CommandGroup(self.plainTextEdit_4, self.sendButton_4, self.label_4),
        ]
        # assign the action to the Send button
        self.sendButton_0.clicked.connect(lambda: self.send(0))
        self.sendButton_1.clicked.connect(lambda: self.send(1))
        self.sendButton_2.clicked.connect(lambda: self.send(2))
        self.sendButton_3.clicked.connect(lambda: self.send(3))
        self.sendButton_4.clicked.connect(lambda: self.send(4))

        # set style of the console window
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily('Consolas')
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet('background-color: rgb(53, 43, 65);')
        self.textEdit.setPlainText('')

        # find available COM port
        ports = findPorts()
        if len(ports) > 0:
            portName = ports[0]
        else:
            portName = ''
        self.serialPort = SerialPort(portName)
        # open the port if any or close it to set GUI to the corresponding state
        self.openButton.clicked.connect(self.closePort)
        if portName != '':
            self.openPort()
        else:
            self.closePort()

        # start reading thread
        self.continueRead = False
        self.dataLock = Lock()
        self.readingThread = Thread(target=self.readFromPort, daemon=True)

        # assign actions to menu
        self.actionPort.triggered.connect(self.configurePort)


    def configurePort(self):
        dialog = PortConfig()
        ret = dialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            newPortName = dialog.comboBox.currentText()
            if newPortName != self.serialPort.getPortName():
                self.serialPort.close()
                self.serialPort.setPortName(dialog.comboBox.currentText())
                self.openPort()
                print('Port ' + self.serialPort.getPortName() + ' is now open')

    def closePort(self):
        self.serialPort.close()
        self.openButton.setStyleSheet('background-color:' + PortClosedColor + '; color:white')
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.openPort)
        self.openButton.setText('Open')
        for command in self.commandGroups:
            command.sendButton.setDisabled(True)

    def openPort(self):
        try:
            self.serialPort.open()
            self.continueRead = True
            # port is successfully open, change the button functionality to 'Close'
            self.openButton.setStyleSheet('background-color:' + PortOpenedColor + '; color:black')
            self.openButton.clicked.disconnect()
            self.openButton.clicked.connect(self.closePort)
            self.openButton.setText('Close')
            for command in self.commandGroups:
                command.sendButton.setEnabled(True)


        except serial.SerialException:
            # port can't be opened, call closePort() method to change the button back to Open functionality
            QMessageBox.information(self, 'Info', 'Port ' + self.serialPort.getPortName() + ' is closed')
            self.closePort()

    def send(self, commandNum: int):
        # get the command from the text editor
        command = self.commandGroups[commandNum].commandTextEdit.toPlainText()
        if command != "":
            # write and read from the serial port
            bytes = self.serialPort.write(command)
            with self.dataLock:
                # print the command on the textEdit
                print("Sending command %i: %s", commandNum, command)
                self.textEdit.setTextColor(CommandColor)
                self.textEdit.append(command)

#            # print the response
#            response = ""
#            for byte in bytes:
#                response += format(byte, 'x') + " "
#            print("Response:", response)
#            self.textEdit.setTextColor(ResponseColor)
#            self.textEdit.append(response)


    def readFromPort(self):
        while True:
            if self.continueRead:
                readData = self.serialPort.read(size=1)
                data = format(readData, 'x') + " "
                with self.dataLock:
                    print("Response:", response)
                    self.textEdit.setTextColor(ResponseColor)
                    self.textEdit.append(response)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TerminalWin()
    window.show()
    sys.exit(app.exec_())
