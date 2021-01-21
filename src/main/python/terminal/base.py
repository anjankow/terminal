# This Python file uses the following encoding: utf-8

from PyQt5 import uic
import os

uiDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui')

qtCreatorFile = os.path.join(uiDir, 'TerminalWin.ui')
Ui_TerminalWin, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile = os.path.join(uiDir, 'SyncCharsDialog.ui')
Ui_SyncCharsDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile = os.path.join(uiDir, 'CommandEditor.ui')
Ui_CommandEditor, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile = os.path.join(uiDir, 'PortConfig.ui')
Ui_PortConfig, QtBaseClass = uic.loadUiType(qtCreatorFile)
