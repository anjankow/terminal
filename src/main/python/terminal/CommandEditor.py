# This Python file uses the following encoding: utf-8
import sys
import os
import xml.etree.ElementTree as ETree

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtGui import QColor

from .Ui_CommandEditor import Ui_Dialog as Ui_CommandEditor
from .serialport import SerialPort
from .CommandHolder import CommandHolder, Command


class CommandTextBoxes:
    def __init__(self, command: QLineEdit, label: QLineEdit):
        self.command = command
        self.label = label

class CommandEditor(QDialog, Ui_CommandEditor):
    def __init__(self, commandHolder: CommandHolder):
        QtWidgets.QDialog.__init__(self)
        Ui_CommandEditor.__init__(self)
        self.setupUi(self)

        # assign actions to the GUI members
        self.loadButton.clicked.connect(self.loadConfig)
        self.deleteButton.clicked.connect(self.deleteConfig)
        self.buttonBox.accepted.connect(self.saveNewConfig)

        # initialize the rest of the members
        self.commandHolder = commandHolder
        self.updateComboBox()
        self.textBoxes = self.getTextBoxesOnInit()
        self.defaultConfigName = 'New commands'

        # this flag informs whether any data has been dataEntered
        self.__dataEntered = False


    def getTextBoxesOnInit(self):
        # gather all the command textEdits and corresponding labels
        textBoxes = []
        for i in range(0, 10): # let's say 10 in case if there is more in the future
            command = self.findChild(QLineEdit, 'commandText_' + str(i))
            label = self.findChild(QLineEdit, 'comLabel_' + str(i))
            if command != None and label != None:
                textBoxes.append(CommandTextBoxes(command, label))
            else:
                break
        return textBoxes

    def updateComboBox(self):
        self.comboBox.clear()
        for key in (self.commandHolder.getAll()).keys():
            self.comboBox.addItem(key)

    def assignTextBoxes(self, name: str, commandSet):
        self.configName.setText(name)
        # clear all the text boxes
        for textBoxSet in self.textBoxes:
            textBoxSet.command.clear()
            textBoxSet.label.clear()
        # assign all text boxes according to commandSet configuration
        for i in range(0, len(commandSet)):
            self.textBoxes[i].command.setText(commandSet[i].content)
            self.textBoxes[i].label.setText(commandSet[i].label)

    def getDataFromTextBoxes(self):
        commandList = []
        for commandTextBoxes in self.textBoxes:
            commandText = (commandTextBoxes.command.text()).rstrip().lstrip()
            labelText = (commandTextBoxes.label.text()).rstrip().lstrip()
            if commandText != '':
                commandList.append(Command(commandText, labelText))
        # return something only is there are any commands given
        retVal = None
        if len(commandList) > 0:
            retVal = commandList
        return retVal

    def saveNewConfig(self):
        name = self.configName.text()
        if name == '':
            name = self.defaultConfigName
        commandList = self.getDataFromTextBoxes()
        if commandList:
            self.__dataEntered = True
            self.commandHolder.add(name, commandList)
            self.commandHolder.setActiveCommandSet(name)

    def loadConfig(self):
        name = self.comboBox.currentText()
        if name != '':
            commandSet = self.commandHolder.getCommandSet(name)
            self.assignTextBoxes(name, commandSet)

    def deleteConfig(self):
        name = self.comboBox.currentText()
        self.commandHolder.delete(name)
        self.updateComboBox()

    def dataEntered(self):
        return self.__dataEntered

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    commandHolder = CommandHolder('pleple.xml')
    for i in range(0,3):
        dialog = CommandEditor(commandHolder)
        ret = dialog.exec_()
    commandHolder.saveToXml()

    sys.exit(app.exec_())
