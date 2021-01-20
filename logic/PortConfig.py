# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QColor

from .SerialPort import *

qtCreatorFile = os.path.join(os.path.dirname(__file__), '..', 'ui/PortConfig.ui')
Ui_PortConfig, QtBaseClass = uic.loadUiType(qtCreatorFile)


class PortConfig(QDialog, Ui_PortConfig):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_PortConfig.__init__(self)
        self.setupUi(self)

        # show the list of ports
        ports = findPorts()
        for port in ports:
            self.comboBox.addItem(port)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = PortConfig()
    ret = dialog.exec_()
    print(ret)
    sys.exit(app.exec_())
