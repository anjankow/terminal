# This Python file uses the following encoding: utf-8
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5 import uic


class TerminalAppContext(ApplicationContext):
    def __init__(self):
        print('ApCx: init')
        pass

    def run(self):

#        app = QtWidgets.QApplication(sys.argv)
#        self.app.setWindowIcon(QtGui.QIcon('resources/terminal.ico'))
#        self.app.setWindowIcon(self.app_icon))
#        window = Terminal()
#        print('ApCx: terminal init')
#        window.show()
#        print('ApCx: win show')
        code = self.app.exec_()
        print('ApCx: exec done')
#        window.closePort()
#        print('ApCx: port closed')
#        window.commandHolder.saveToXml()
        print('ApCx: saved to xml')
        return code

