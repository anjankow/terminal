# This Python file uses the following encoding: utf-8

from .TerminalAppContext import *


app_cntxt = TerminalAppContext()

qtCreatorFile = app_cntxt.get_resource('ui/TerminalWin.ui')
Ui_TerminalWin, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile = app_cntxt.get_resource('ui/SyncCharsDialog.ui')
Ui_SyncCharsDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile = app_cntxt.get_resource('ui/CommandEditor.ui')
Ui_CommandEditor, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile = app_cntxt.get_resource('ui/PortConfig.ui')
Ui_PortConfig, QtBaseClass = uic.loadUiType(qtCreatorFile)
