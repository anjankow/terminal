# This Python file uses the following encoding: utf-8
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext

class TerminalAppContext(ApplicationContext):

    def run(self):
        # import only when ready to run - ui needs to be generated
        from .Terminal import Terminal

        window = Terminal(self)
        window.show()
        code = self.app.exec_()
        window.closePort()
        window.commandHolder.saveToXml()
        return code

    def get_ui_path(self):
        terminalPath = self.get_resource('ui')
        return terminalPath
