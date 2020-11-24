# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = QMainWindow()
    mainwin.setWindowTitle("Hallo")
    mainwin.show()

    sys.exit(app.exec_())
