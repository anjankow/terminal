# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QColor

from .Ui_SyncCharsDialog import Ui_Dialog as Ui_SyncCharsDialog

class SyncCharsDialog(QDialog, Ui_SyncCharsDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_SyncCharsDialog.__init__(self)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = SyncCharsDialog()
    ret = dialog.exec_()
    print(ret)
    sys.exit(app.exec_())
