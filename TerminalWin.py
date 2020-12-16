import sys
import serial
from threading import Lock


from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QColor

from SerialPort import SerialPort, findPorts
from PortConfig import PortConfig
from CommandHolder import CommandHolder
from CommandEditor import CommandEditor

qtCreatorFile = "TerminalWin.ui"
Ui_TerminalWin, QtBaseClass = uic.loadUiType(qtCreatorFile)

CommandColor = QColor('#c6ffee')
ResponseColor = QColor('#fcfed4')
PortOpenedColor = 'rgb(199, 255, 147)'
PortClosedColor = 'rgb(177, 43, 43)'

commandConfigFile = 'commandConfig.xml'

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
            CommandGroup(self.lineEdit_0, self.sendButton_0, self.label_0),
            CommandGroup(self.lineEdit_1, self.sendButton_1, self.label_1),
            CommandGroup(self.lineEdit_2, self.sendButton_2, self.label_2),
            CommandGroup(self.lineEdit_3, self.sendButton_3, self.label_3),
            CommandGroup(self.lineEdit_4, self.sendButton_4, self.label_4),
        ]
        # assign the action to the Send button
        self.sendButton_0.clicked.connect(lambda: self.send(0))
        self.sendButton_1.clicked.connect(lambda: self.send(1))
        self.sendButton_2.clicked.connect(lambda: self.send(2))
        self.sendButton_3.clicked.connect(lambda: self.send(3))
        self.sendButton_4.clicked.connect(lambda: self.send(4))

        # assign actions to the other buttons
        self.openButton.clicked.connect(self.closePort)
        self.editButton.clicked.connect(self.editCommands)

        # assign actions to menu
        self.actionPort.triggered.connect(self.configurePort)

        # set style of the console window
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily('Consolas')
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet('background-color: rgb(53, 43, 65);')
        self.textEdit.setPlainText('')

        # lock for displayed communication data
        self.dataLock = Lock()

        # find available COM port
        ports = findPorts()
        if len(ports) > 0:
            portName = ports[0]
        else:
            portName = ''
        self.serialPort = SerialPort(portName, self.readCallback)

        # open the port if any or close it to set GUI to the corresponding state
        if portName != '':
            self.openPort()
        else:
            self.updateGuiOnClosedPort()

        # load the commands from the config file
        self.commandHolder = CommandHolder(commandConfigFile)


    # function called whenever a byte is read
    def readCallback(self, hexByte):
        with self.dataLock:
            self.textEdit.setTextColor(ResponseColor)
            self.textEdit.append(hexByte)


    def editCommands(self):
        dialog = CommandEditor(self.commandHolder)
        ret = dialog.exec_()
        # if the user pressed OK, fill text boxes with the given command set
        if ret == QtWidgets.QDialog.Accepted:
            # clear all the current text boxes
            for i in range(0, len(self.commandGroups)):
                self.commandGroups[i].commandTextEdit.clear()
                self.commandGroups[i].commandLabel.setText('Command ' + str(i))

            # get the current commands from the dialog
            currentName = dialog.configName.text()
            if currentName == '':
                currentName = dialog.defaultConfigName

            i = 0
            for command in self.commandHolder.getCommandSet(currentName):
                self.commandGroups[i].commandTextEdit.setText(command.content)
                self.commandGroups[i].commandLabel.setText(command.label)
                i += 1


    def configurePort(self):
        dialog = PortConfig()
        ret = dialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            newPortName = dialog.comboBox.currentText()
            if newPortName != self.serialPort.getPortName():
                self.closePort()
                self.serialPort.setPortName(dialog.comboBox.currentText())
                self.openPort()
                print('Port ' + self.serialPort.getPortName() + ' is now open')

    def closePort(self):
        self.stopReading()
        self.serialPort.close()
        self.updateGuiOnClosedPort()

    def openPort(self):
        try:
            self.serialPort.open()
            self.updateGuiOnOpenedPort()

        except serial.SerialException:
            # port can't be opened, call closePort() method to change the button back to Open functionality
            QMessageBox.information(self, 'Info', 'Port ' + self.serialPort.getPortName() + ' is closed')
            self.updateGuiOnClosedPort()

    def send(self, commandNum: int):
        # get the command from the text editor
        command = self.commandGroups[commandNum].commandTextEdit.text()
        if command != "":
            # write from the serial port
            bytes = self.serialPort.write(command)
            with self.dataLock:
                # print the command on the textEdit
                print("Sending command" + str(commandNum) +': ', command)
                self.textEdit.setTextColor(CommandColor)
                self.textEdit.append(command)

    def updateGuiOnClosedPort(self):
        # port is open, change the button functionality to 'Open'
        self.openButton.setStyleSheet('background-color:' + PortClosedColor + '; color:white')
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.openPort)
        self.openButton.setText('Open')
        for command in self.commandGroups:
            command.sendButton.setDisabled(True)

    def updateGuiOnOpenedPort(self):
        # port is open, change the button functionality to 'Close'
        self.openButton.setStyleSheet('background-color:' + PortOpenedColor + '; color:black')
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.closePort)
        self.openButton.setText('Close')
        for command in self.commandGroups:
            command.sendButton.setEnabled(True)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TerminalWin()
    window.show()
    sys.exit(app.exec_())
