import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic


qtCreatorFile = "TerminalWin.ui"
Ui_TerminalWin, QtBaseClass = uic.loadUiType(qtCreatorFile)


class CommandGroup:
    def __init__(self, textEdit, sendButton, commandLabel):
        self.commandTextEdit = textEdit
        self.sendButton = sendButton
        self.commandLabel = commandLabel


class TerminalWin(QtWidgets.QMainWindow, Ui_TerminalWin):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_TerminalWin.__init__(self)
        self.setupUi(self)
        self.commandGroups = [
            CommandGroup(self.plainTextEdit_0, self.sendButton_0, self.label_0),
            CommandGroup(self.plainTextEdit_1, self.sendButton_1, self.label_1),
            CommandGroup(self.plainTextEdit_2, self.sendButton_2, self.label_2),
            CommandGroup(self.plainTextEdit_3, self.sendButton_3, self.label_3),
            CommandGroup(self.plainTextEdit_4, self.sendButton_4, self.label_4),
        ]
        self.sendButton_0.clicked.connect(lambda: self.send(0))
        self.sendButton_1.clicked.connect(lambda: self.send(1))
        self.sendButton_2.clicked.connect(lambda: self.send(2))
        self.sendButton_3.clicked.connect(lambda: self.send(3))
        self.sendButton_4.clicked.connect(lambda: self.send(4))


    def send(self, commandNum: int):
        if self.commandGroups[commandNum].commandTextEdit.toPlainText() != "":
            self.commandGroups[commandNum].commandLabel.setText(self.commandGroups[commandNum].commandTextEdit.toPlainText())
        else:
            self.commandGroups[commandNum].commandLabel.setText("Nothing is there!")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TerminalWin()
    window.show()
    sys.exit(app.exec_())
