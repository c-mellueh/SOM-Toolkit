from som_gui.icons import get_icon
from pyqtconsole.console import PythonConsole
from . import trigger


class Console(PythonConsole):
    def __init__(self, *args, **kwds):
        super(Console, self).__init__(*args, **kwds)
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Console")

    def closeEvent(self, event):
        trigger.close_console()
        super().closeEvent(event)
