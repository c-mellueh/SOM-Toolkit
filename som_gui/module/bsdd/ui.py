from som_gui.module.bsdd.qt.ui_widget import Ui_BSDD
from som_gui.resources.icons import get_icon
from PySide6.QtWidgets import QWidget
from . import trigger


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_BSDD()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())

class DictionaryWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.paint_dictionary()
