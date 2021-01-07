import sys
import serial
from threading import Lock
from enum import Enum

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtCore import QObject, pyqtSignal

from SerialPort import SerialPort, findPorts
from PortConfig import PortConfig
from CommandHolder import CommandHolder
from CommandEditor import CommandEditor
from resources import *


qtCreatorFile = "TerminalWin.ui"
Ui_TerminalWin, QtBaseClass = uic.loadUiType(qtCreatorFile)


class IncomingType(Enum):
    NOTIFICATION = 0
    RESPONSE = 1

class ThreadEvent(QObject):
    # events coming from another thread
    bytesRead = pyqtSignal(str)


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

        self.terminal.setPlainText('')

        # lock for displayed communication data
        self.dataLock = Lock()

        # load the commands from the config file
        self.commandHolder = CommandHolder(CONFIG_FILE)
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
        self.serialPort = SerialPort(portName, self.readCallback)

        # open the port if any or close it to set GUI to the corresponding state
        if portName != '':
            self.openPort()
        else:
            self.updateOnClosedPort()

        self.setStyles()

        self.threadEvent = ThreadEvent()
        self.threadEvent.bytesRead.connect(lambda readByte: self.printResponse(readByte))

        self.incomingType = IncomingType.NOTIFICATION


    def assignConnections(self):
        # assign the action to the Send button
        self.sendButton_0.clicked.connect(lambda: self.send(0))
        self.sendButton_1.clicked.connect(lambda: self.send(1))
        self.sendButton_2.clicked.connect(lambda: self.send(2))
        self.sendButton_3.clicked.connect(lambda: self.send(3))
        self.sendButton_4.clicked.connect(lambda: self.send(4))

        # assign actions to the other buttons
        self.openButton.clicked.connect(self.closePort)
        self.editButton.clicked.connect(self.editCommands)
        self.clearButton.clicked.connect(self.clearScreen)

        # assign actions to menu
        self.actionPort.triggered.connect(self.configurePort)

        self.comboBox.currentTextChanged.connect(self.updateOnComboboxChange)


    # function called whenever a byte is read
    def readCallback(self, hexByte):
        with self.dataLock:
            self.threadEvent.bytesRead.emit(hexByte)


    def onIncomingBytes(self, text):
        self.interpret(text)
        if self.incomingType == IncomingType.NOTIFICATION:
            self.printNotification(text)
        elif self.incomingType == IncomingType.RESPONSE:
            self.printResponse(text)
        else:
            pass

    def interpret(self, text):
        self.lastReceived += text



    def clearScreen(self):

        self.terminal.moveCursor(QTextCursor.PreviousWord)
        self.terminal.moveCursor(QTextCursor.PreviousWord)
        self.terminal.moveCursor(QTextCursor.PreviousWord)
        responseStyle = "<span style=\"  color:" + RESPONSE_COLOR + ";\" >"
        self.terminal.insertHtml(responseStyle)
#        self.terminal.moveCursor(QTextCursor.End)
#        self.terminal.insertHtml(text + ' ')
        self.terminal.insertHtml('AAAAAA')
        self.terminal.insertHtml("</span>")
        print(self.terminal.toHtml())
        self.terminal.update()
#        print('Moving cursor from ', start)
#        self.terminal.select(
#        self.removeSelectedText()
#        self.terminal.clear()


    def editCommands(self):
        dialog = CommandEditor(self.commandHolder)
        ret = dialog.exec_()
        # if the user pressed OK, fill text boxes with the given command set
        if ret == QtWidgets.QDialog.Accepted:
            if dialog.dataEntered():
                # the given configuration is the active one now
                # update UI using the active configuration
                self.loadCommandSet(self.commandHolder.getActiveCommandSet())
        self.updateCombobox()



    def loadCommandSet(self, commandSetName):
        # clear all the current text boxes
        for i in range(0, len(self.commandGroups)):
            self.commandGroups[i].commandTextEdit.clear()
            self.commandGroups[i].commandLabel.setText('Command ' + str(i))

        if commandSetName != None and commandSetName in self.commandHolder.getAll():
            # fill the text boxes with the data from the given command set
            j = 0
            for command in self.commandHolder.getCommandSet(commandSetName):
                self.commandGroups[j].commandTextEdit.setText(command.content)
                if command.label != '':
                    self.commandGroups[j].commandLabel.setText(command.label)
                    self.commandGroups[j].commandLabel.adjustSize()
                j += 1


    def updateCombobox(self):
        # update the comboBox
        self.comboBox.clear()
        self.comboBox.addItems(self.commandHolder.getAll().keys())
        active = self.commandHolder.getActiveCommandSet()
        index = self.comboBox.findText(active, QtCore.Qt.MatchFixedString)
        if index >= 0:
             self.comboBox.setCurrentIndex(index)


    def updateOnComboboxChange(self):
        # called on combobox change
        currentName =   self.comboBox.currentText()
        self.commandHolder.setActiveCommandSet(currentName)
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
            with self.dataLock:
                # print the command on the terminal
                print("Sending command" + str(commandNum) +': ', command)
                self.printCommand(command)
                self.terminal.moveCursor(QTextCursor.End)

    # function called on bytesRead event
    def printResponse(self, text):
#        text = "<span style=\"  color:" + RESPONSE_COLOR + ";\" >"  + text + " </span>"
        with self.dataLock:
            text = text + ' '
            self.terminal.insertHtml(text)
            self.terminal.moveCursor(QTextCursor.End)

    def printCommand(self, text):
        text = "<span style=\"  color:" + COMMAND_COLOR + ";\" >"  + text + "</span><br/>"
        self.terminal.append('')
        self.terminal.insertHtml(text)
        self.terminal.append('')

    def updateOnClosedPort(self):
        # port is open, change the button functionality to 'Open'
        self.openButton.setStyleSheet('background-color:' + PORTCLOSED_COLOR + '; color:white')
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.openPort)
        self.openButton.setText('Open')
        for command in self.commandGroups:
            command.sendButton.setDisabled(True)

    def updateOnOpenedPort(self):
        # port is open, change the button functionality to 'Close'
        self.openButton.setStyleSheet('background-color:' + PORTOPENED_COLOR + '; color:black')
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.closePort)
        self.openButton.setText('Close')
        for command in self.commandGroups:
            command.sendButton.setEnabled(True)

    def setStyles(self):
        # set style of the console window
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily('Consolas')
        self.terminal.setFont(font)
        self.terminal.setStyleSheet('background-color: ' + TERMINALBCKGND_COLOR + ';')

        for commandGroup in self.commandGroups:
            commandGroup.commandTextEdit.setStyleSheet('color: ' + CMDEDITFONT_COLOR + ';')




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TerminalWin()
    window.show()
    code = app.exec_()
    window.closePort()
    window.commandHolder.saveToXml()
    sys.exit(code)
