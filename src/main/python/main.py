from PyQt5 import QtCore, QtGui, QtWidgets

import sys

#from terminal import *
#from terminal.TerminalAppContext import *
from terminal.Terminal import *

if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    app.setWindowIcon(QtGui.QIcon('terminal.ico'))
#    window = Terminal()
#    window.show()
#    code = app.exec_()
#    window.closePort()
#    window.commandHolder.saveToXml()
#    sys.exit(code)
#    appctxt = TerminalAppContext()
#    print('app context created')
#    window = Terminal()
#    print('TErminal created')
#    window.show()

#    exit_code = appctxt.run()
#    print('exit code: ', exit_code)
#    sys.exit(exit_code)

#    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = Terminal(appctxt)
#    window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
