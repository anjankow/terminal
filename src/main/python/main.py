from PyQt5 import QtCore, QtGui, QtWidgets

import sys

from terminal.TerminalAppContext import TerminalAppContext

if __name__ == "__main__":
    appctxt = TerminalAppContext()
    code = appctxt.run()
    sys.exit(code)
