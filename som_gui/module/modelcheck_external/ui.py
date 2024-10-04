from __future__ import annotations
from PySide6.QtWidgets import QVBoxLayout, QMainWindow
from som_gui.icons import get_icon
from som_gui import tool
from .qt import widget

class ModelcheckExternalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = widget.Ui_MainWindow()
        self.ui.setupUi(self)
        self.vertical_layout = QVBoxLayout(self)
        self.setLayout(self.vertical_layout)
        self.setWindowTitle(f"Modellprüfung exportieren | {tool.Util.get_status_text()}")
        self.setWindowIcon(get_icon())
