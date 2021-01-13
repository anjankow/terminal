# This Python file uses the following encoding: utf-8

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor

from threading import Lock

from resources import *

class TerminalDisplay:
    def __init__(self, terminalDisplay: QTextEdit):
        self.terminal = terminalDisplay
        self.terminal.setPlainText('')

        # lock for displayed communication data
        self.dataLock = Lock()

        self.syncChars = SYNC_CHARS
        self.lastCharsRead = ''

        self.firstRspAfterCmd = True
        self.charsLimit = CHARS_LIMIT

        self.setStyle();


    def setStyle(self):
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily('Consolas')
        self.terminal.setFont(font)
        self.terminal.setStyleSheet('background-color: ' + TERMINALBCKGND_COLOR + ';')


    # insert a new line if the sync sequence has been received
    def applySyncSequence(self):
        # compare not including the spaces
        lastCharsSpaceless = self.lastCharsRead.replace(' ','')
        syncCharsSpaceless = self.syncChars.replace(' ','')
        if len(lastCharsSpaceless) == len(syncCharsSpaceless):
            if lastCharsSpaceless == syncCharsSpaceless:
                with self.dataLock:
                    # subtract 2 characters, because the new chars hasn't been added yet
                    for i in range(0, len(syncCharsSpaceless) - 2, 2):
                        self.terminal.moveCursor(QTextCursor.PreviousWord)
                    self.terminal.insertHtml('<br/> ')
                    self.terminal.moveCursor(QTextCursor.End)
                # clear the stored chars
                self.lastCharsRead = ''
            else:
                # if the sequence doesn't match, delete first two chars (one hex number) from the sequence
                self.lastCharsRead = self.lastCharsRead[3:]


    # function called on bytesRead event
    def printResponse(self, text):
        text += ' '

        # check if a sync pattern is given
        if self.firstRspAfterCmd:
            self.firstRspAfterCmd = False
        else:
            self.lastCharsRead += text
            self.applySyncSequence()

        # add received text to the terminal display
        with self.dataLock:
            text = "<span style=\"  color:" + RESPONSE_COLOR + ";\" >"  + text + "</span> "
            text = text + ' '
            self.protectAgainstOverflow(text)
            self.terminal.insertHtml(text)
            self.terminal.moveCursor(QTextCursor.End)

    # delete chars from the top if the limit is reached
    def protectAgainstOverflow(self, text):
        currentLen = len(self.terminal.toPlainText())
        if currentLen + len(text) >= self.charsLimit:
            cursor = self.terminal.textCursor()
            self.terminal.setTextCursor(cursor)
            cursor.setPosition(QTextCursor.Start)
            cursor.setPosition(QTextCursor.Start + len(text), QtGui.QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            cursor.movePosition(QTextCursor.End)


    # print the command on the terminal
    def printCommand(self, text):
        self.firstRspAfterCmd = True

        with self.dataLock:
            text = "<span style=\"  color:" + COMMAND_COLOR + ";\" >"  + text + "</span> "
            # first delete some chars from the top if needed
            self.protectAgainstOverflow(text)
            self.terminal.append('')
            self.terminal.insertHtml(text)
            self.terminal.append('')


    def updateSyncChars(self, chars):
        self.syncChars = chars

    def clear(self):
        self.terminal.clear()
