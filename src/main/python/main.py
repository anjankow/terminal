from PyQt5 import QtCore, QtGui, QtWidgets

import sys

from terminal.Terminal import Terminal

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
#    app.setWindowIcon(QtGui.QIcon('resources/terminal.ico'))
    window = Terminal()
    window.show()
    code = app.exec_()
    window.closePort()
    window.commandHolder.saveToXml()
    sys.exit(code)
