from __future__ import annotations
from PySide6.QtWidgets import QVBoxLayout, QMainWindow
from som_gui.resources.icons import get_icon
from .qt import ui_Widget

class ModelcheckExternalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui_Widget.Ui_Modelcheck()
        self.ui.setupUi(self)
        self.vertical_layout = QVBoxLayout(self)
        self.setLayout(self.vertical_layout)
        self.setWindowIcon(get_icon())
