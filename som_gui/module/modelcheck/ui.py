from PySide6.QtWidgets import QWidget, QVBoxLayout
from .widget_object_check import Ui_Form
from som_gui.icons import get_icon


class ModelcheckWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(get_icon())
        self.vertical_layout = QVBoxLayout(self)


class ObjectCheckWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
