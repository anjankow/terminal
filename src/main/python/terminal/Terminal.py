from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtCore import QObject, pyqtSignal

from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys
import os
import serial
from threading import Lock
from enum import Enum

from .Ui_TerminalWin import Ui_TerminalWin
from .constants import *
from .serialport import *
from .TerminalDisplay import *
from .CommandHolder import *
from .PortConfig import *
from .SaveCmdDialog import *
from .CommandHolder import *
from .SyncCharsDialog import *


class ThreadEvent(QObject):
    # events coming from another thread
    bytesRead = pyqtSignal(str)

class CommandGroup:
    def __init__(self, textEdit, sendButton, commandLabel):
        self.commandTextEdit = textEdit
        self.sendButton = sendButton
        self.commandLabel = commandLabel


class Terminal(QtWidgets.QMainWindow, Ui_TerminalWin):
    def __init__(self, appcntxt: ApplicationContext):
        print('Terminal init start')
        QtWidgets.QMainWindow.__init__(self)
        Ui_TerminalWin.__init__(self)
        self.setupUi(self)
        self.appcntxt = appcntxt
        self.terminalDisplay = TerminalDisplay(self.terminal)

        # initialize command groups
        self.commandGroups = [
            CommandGroup(self.lineEdit_0, self.sendButton_0, self.label_0),
            CommandGroup(self.lineEdit_1, self.sendButton_1, self.label_1),
            CommandGroup(self.lineEdit_2, self.sendButton_2, self.label_2),
            CommandGroup(self.lineEdit_3, self.sendButton_3, self.label_3),
            CommandGroup(self.lineEdit_4, self.sendButton_4, self.label_4),
            CommandGroup(self.lineEdit_5, self.sendButton_5, self.label_5),
        ]

        # load the commands from the config file
        self.commandHolder = CommandHolder(self.appcntxt.get_resource(CONFIG_FILE_NAME))
        activeName = self.commandHolder.getActiveCommandSet()
        self.loadCommandSet(activeName)
        self.updateCombobox()

        self.assignConnections()

        # find available COM port
        ports = findPorts()
        if len(ports) > 0:
            portName = ports[0]
        else:
            portName = ''
        self.serialPort = SerialPort(portName, self.readCallback, debug=False)

        # open the port if any or close it to set GUI to the corresponding state
        if portName != '':
            self.openPort()
        else:
            self.updateOnClosedPort()

        for commandGroup in self.commandGroups:
            commandGroup.commandTextEdit.setStyleSheet('color: ' + CMDEDITFONT_COLOR + ';')

        # connect read event with printing function
        self.threadEvent = ThreadEvent()
        self.threadEvent.bytesRead.connect(lambda readByte: self.reactOnBytesRead(readByte))
        print('Terminal init done')

    def reactOnBytesRead(self, readByte):
        self.terminalDisplay.printResponse(readByte)
        self.incomingCnt.setText(str(self.serialPort.getIncomingBytesCnt()))


    def assignConnections(self):
        # assign the action to the Send button
        self.sendButton_0.clicked.connect(lambda: self.send(0))
        self.sendButton_1.clicked.connect(lambda: self.send(1))
        self.sendButton_2.clicked.connect(lambda: self.send(2))
        self.sendButton_3.clicked.connect(lambda: self.send(3))
        self.sendButton_4.clicked.connect(lambda: self.send(4))
        self.sendButton_5.clicked.connect(lambda: self.send(5))

        # assign actions to the other buttons
        self.openButton.clicked.connect(self.closePort)
        self.saveCmdButton.clicked.connect(self.saveCommands)
        self.clearButton.clicked.connect(self.clearScreen)

        # assign actions to menu
        self.actionPort.triggered.connect(self.configurePort)
        self.actionSyncCharacters.triggered.connect(self.changeSyncChars)

        self.comboBox.currentTextChanged.connect(self.updateOnComboboxChange)


    # function called whenever a byte is read
    def readCallback(self, hexByte):
        self.threadEvent.bytesRead.emit(hexByte)

    def changeSyncChars(self):
        dialog = SyncCharsDialog()
        ret = dialog.exec_()
        # if the user pressed OK, fill text boxes with the given command set
        if ret == QtWidgets.QDialog.Accepted:
            self.terminalDisplay.updateSyncChars(dialog.lineEdit.text())

    def clearScreen(self):
        self.terminalDisplay.clear()

    def getDataFromTextBoxes(self):
        commandList = []
        for commandTextBoxes in self.commandGroups:
            commandText = (commandTextBoxes.commandTextEdit.text()).rstrip().lstrip()
            labelText = (commandTextBoxes.commandLabel.text()).rstrip().lstrip()
            if commandText != '':
                commandList.append(Command(commandText, labelText))
        # return something only is there are any commands given
        retVal = None
        if len(commandList) > 0:
            retVal = commandList
        return retVal


    def saveCommands(self):
        dialog = SaveCmdDialog(self.commandHolder)
        ret = dialog.exec_()
        # if the user pressed OK, fill text boxes with the given command set
        if ret == QtWidgets.QDialog.Accepted:
            cmdset_name = dialog.name
            if cmdset_name != None:
                # gather all the commands and labels
                commandList = self.getDataFromTextBoxes()
                # add it to CommandHolder
                self.commandHolder.add(cmdset_name, commandList)
                # save command holder
                self.commandHolder.saveToXml()
                self.updateCombobox()


    def loadCommandSet(self, commandSetName):
        # clear all the current text boxes
        for i in range(0, len(self.commandGroups)):
            self.commandGroups[i].commandTextEdit.clear()
            self.commandGroups[i].commandLabel.clear()

        if commandSetName != None and commandSetName in self.commandHolder.getAll():
            # fill the text boxes with the data from the given command set
            j = 0
            for command in self.commandHolder.getCommandSet(commandSetName):
                self.commandGroups[j].commandTextEdit.setText(command.content)
                if command.label != '':
                    self.commandGroups[j].commandLabel.setText(command.label)
                j += 1


    def updateCombobox(self):
        # update the comboBox
        self.comboBox.clear()
        self.comboBox.addItems(self.commandHolder.getAll().keys())
        active = self.commandHolder.getActiveCommandSet()
        print('Active command set: ', active)
        index = self.comboBox.findText(active, QtCore.Qt.MatchFixedString)
        if index >= 0:
             self.comboBox.setCurrentIndex(index)


    def updateOnComboboxChange(self):
        # called on combobox change
        currentName =   self.comboBox.currentText()
#        self.commandHolder.setActiveCommandSet(currentName)
        self.loadCommandSet(currentName)


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
        self.serialPort.close()
        self.updateOnClosedPort()

    def openPort(self):
        try:
            self.serialPort.open()
            self.updateOnOpenedPort()

        except serial.SerialException:
            # port can't be opened, call closePort() method to change the button back to Open functionality
            QMessageBox.information(self, 'Info', 'Port ' + self.serialPort.getPortName() + ' is closed')
            self.updateOnClosedPort()

    def send(self, commandNum: int):
        # get the command from the text editor
        command = self.commandGroups[commandNum].commandTextEdit.text()
        if command != "":
            # write from the serial port
            self.serialPort.write(command)
            print("Sending command" + str(commandNum) +': ', command)
            self.terminalDisplay.printCommand(command)

    def updateOnClosedPort(self):
        # port is open, change the button functionality to 'Open'
        self.openButton.setStyleSheet('background-color:' + PORTCLOSED_COLOR + '; color:white')
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.openPort)
        self.openButton.setText('Open')
        for command in self.commandGroups:
            command.sendButton.setDisabled(True)
        self.incomingCnt.setStyleSheet('background-color:rgb(216, 220, 240);')

    def updateOnOpenedPort(self):
        # port is open, change the button functionality to 'Close'
        self.openButton.setStyleSheet('background-color:' + PORTOPENED_COLOR + '; color:black')
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.closePort)
        self.openButton.setText('Close')
        for command in self.commandGroups:
            command.sendButton.setEnabled(True)
        self.incomingCnt.setStyleSheet('background-color:white')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('resources/terminal.ico'))
    window = Terminal()
    window.show()
    code = app.exec_()
    window.closePort()
    window.commandHolder.saveToXml()
    sys.exit(code)
