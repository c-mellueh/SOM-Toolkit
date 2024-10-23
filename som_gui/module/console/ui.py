from som_gui.resources.icons import get_icon
from pyqtconsole.console import PythonConsole
from . import trigger
from som_gui import tool


class Console(PythonConsole):
    def __init__(self, *args, **kwds):
        super(Console, self).__init__(*args, **kwds)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(f"Console | {tool.Util.get_status_text()}")

    def closeEvent(self, event):
        trigger.close_console()
        super().closeEvent(event)
