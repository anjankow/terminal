# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QColor
from SerialPort import SerialPort

qtCreatorFile = "CommandEditor.ui"
Ui_CommandEditor, QtBaseClass = uic.loadUiType(qtCreatorFile)


class CommandEditor(QDialog, Ui_CommandEditor):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_CommandEditor.__init__(self)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = CommandEditor()
    ret = dialog.exec_()
    print(ret)
    sys.exit(app.exec_())
