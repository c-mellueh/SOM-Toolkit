from .widget import Ui_Form
from som_gui.icons import get_icon
from PySide6.QtWidgets import QWidget


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("bsDD erzeugen")
        self.setWindowIcon(get_icon())
