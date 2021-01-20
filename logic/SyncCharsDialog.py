# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QColor

qtCreatorFile = os.path.join(os.path.dirname(__file__), '..', 'ui/SyncCharsDialog.ui')
Ui_SyncCharsDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


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
