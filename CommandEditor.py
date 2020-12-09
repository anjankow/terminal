# This Python file uses the following encoding: utf-8
import sys
import xml.etree.ElementTree as ET

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtGui import QColor
from SerialPort import SerialPort

from CommandHolder import *

qtCreatorFile = "CommandEditor.ui"
Ui_CommandEditor, QtBaseClass = uic.loadUiType(qtCreatorFile)

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
        self.textBoxes = []
        # gather all the command textEdits and corresponding labels
        for i in range(0, 10): # let's say 10 in case if there is more in the future
            command = self.findChild(QLineEdit, 'commandText_' + str(i))
            label = self.findChild(QLineEdit, 'comLabel_' + str(i))
            if command != None and label != None:
                self.textBoxes.append(CommandTextBoxes(command, label))
            else:
                break

    def updateComboBox(self):
        for commandSet in self.commandHolder.getAll():
            self.comboBox.addItem(commandSet.name)

    def assignTextBoxes(self, commandSet: CommandSet):
        self.configName.setText(commandSet.name)
        # assign all text boxes according to commandSet configuration
        for i in range(0, len(commandSet.commandList)):
            self.textBoxes[i].command.setText(commandSet.commandList[i].content)
            self.textBoxes[i].label.setText(commandSet.commandList[i].label)

    def getDataFromTextBoxes(self):
        name = self.configName.text()
        if name == '':
            name = 'New commands'

        commandList = []
        for commandTextBoxes in self.textBoxes:
            commandText = (commandTextBoxes.command.text()).rstrip().lstrip()
            labelText = (commandTextBoxes.label.text()).rstrip().lstrip()
            if commandText != '':
                commandList.append(Command(commandText, labelText))

        # return something only is there are any commands given
        retVal = None
        if len(commandList) > 0:
            retVal = CommandSet(name, commandList)
        return retVal

    def saveNewConfig(self):
        commandSet = self.getDataFromTextBoxes()
        if commandSet:
            self.commandHolder.add(commandSet)

    def loadConfig(self):
        name = self.comboBox.currentText()
        if name != '':
            commandSet = self.commandHolder.getCommandSet(name)
            self.assignTextBoxes(commandSet)

    def deleteConfig(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    commandHolder = CommandHolder()
    for i in range(0,4):
        dialog = CommandEditor(commandHolder)
        ret = dialog.exec_()

    sys.exit(app.exec_())
