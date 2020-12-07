import sys
import serial

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QColor
from SerialPort import SerialPort

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

        # open COM port
        self.openButton.clicked.connect(self.closePort)
        self.openButton.clicked.connect(self.openPort)
        self.portName = "COM12"
        self.serialPort = SerialPort(self.portName)
        self.openPort()

        # assign actions to menu
        self.actionPort.triggered.connect(self.configurePort)


    def configurePort(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Form()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def closePort(self):
        self.serialPort.close()
        self.openButton.setStyleSheet('background-color:' + PortClosedColor + '; color:white')


    def openPort(self):
        try:
            self.serialPort.open()
            self.openButton.setStyleSheet('background-color:' + PortOpenedColor + '; color:black')

        except serial.SerialException:
            QMessageBox.information(self, 'Info', 'Port ' + self.portName + ' is closed')
            self.closePort()



    def send(self, commandNum: int):
        # get the command from the text editor
        command = self.commandGroups[commandNum].commandTextEdit.toPlainText()
        if command != "":
            # print the command on the textEdit
            print("Sending command %i: %s", commandNum, command)
            self.textEdit.setTextColor(CommandColor)
            self.textEdit.append(command)

            # write and read from the serial port
            bytes = self.serialPort.writeRead(command)

            # print the response
            response = ""
            for byte in bytes:
                response += format(byte, 'x') + " "
            print("Response:", response)
            self.textEdit.setTextColor(ResponseColor)
            self.textEdit.append(response)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TerminalWin()
    window.show()
    sys.exit(app.exec_())
