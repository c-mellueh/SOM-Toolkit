from PySide6.QtWidgets import QWidget
from .widget import Ui_Form


class IfcImportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = Ui_Form()
        self.widget.setupUi(self)
