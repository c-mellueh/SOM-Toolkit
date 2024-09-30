from .widget import Ui_Form
from som_gui.icons import get_icon
from PySide6.QtWidgets import QWidget, QStatusBar
from . import trigger
from som_gui import __version__ as version
from som_gui import tool
class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(f"bsDD erzeugen | {tool.Util.get_status_text()}")
        self.setWindowIcon(get_icon())

class DictionaryWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.paint_dictionary()
