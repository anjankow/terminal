from PyQt5 import QtCore, QtGui, QtWidgets

import sys

from terminal.TerminalAppContext import TerminalAppContext
from terminal.uihelper import generate_ui

if __name__ == "__main__":
    appctxt = TerminalAppContext()
    generate_ui(appctxt.get_ui_path())

    code = appctxt.run()
    sys.exit(code)
