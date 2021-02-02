# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtGui import QColor

from .Ui_SaveCmdDialog import Ui_Dialog as Ui_SaveCmdDialog
from .CommandHolder import CommandHolder, Command


class SaveCmdDialog(QDialog, Ui_SaveCmdDialog):
    def __init__(self, commandHolder: CommandHolder):
        QtWidgets.QDialog.__init__(self)
        Ui_SaveCmdDialog.__init__(self)
        self.setupUi(self)

        # assign actions to the GUI members
        self.buttonBox.accepted.connect(self.saveNewConfig)

        # initialize the rest of the members
        self.commandHolder = commandHolder
        self.updateComboBox()
        self.defaultConfigName = 'New commands'
        # name of command set to be saved/replaced
        self.name = None


    def updateComboBox(self):
        self.comboBox.clear()
        for key in (self.commandHolder.getAll()).keys():
            self.comboBox.addItem(key)

    def saveNewConfig(self):
        if self.radioButton_newSet.isChecked():
            name = (self.configName.text()).rstrip().lstrip()
            if name == '' or name == None:
                name = self.defaultConfigName
        elif self.radioButton_override.isChecked():
            name = self.comboBox.currentText()
            self.commandHolder.delete(name)
        else:
            name = None
        self.name = name


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    commandHolder = CommandHolder('pleple.xml')
    for i in range(0,3):
        dialog = SaveCmdDialog(commandHolder)
        ret = dialog.exec_()
    commandHolder.saveToXml()

    sys.exit(app.exec_())
