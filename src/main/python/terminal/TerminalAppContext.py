# This Python file uses the following encoding: utf-8
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from .Terminal import Terminal

class TerminalAppContext(ApplicationContext):

    def run(self):
        window = Terminal()
        window.show()
        code = self.app.exec_()
        window.closePort()
        window.commandHolder.saveToXml()
        return code
