from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QMainWindow
from PySide6.QtGui import QStandardItemModel
from som_gui.module import modelcheck_window
from som_gui.icons import get_icon
from .window import Ui_MainWindow


class ModelcheckExternalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.widget = Ui_MainWindow()
        # self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.vertical_layout = QVBoxLayout(self)
        self.resize(1139, 720)
        self.setLayout(self.vertical_layout)
        self.setWindowTitle("Modellprüfung exportieren")
