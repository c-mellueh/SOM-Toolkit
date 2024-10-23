from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QDialog, QDialogButtonBox
from PySide6.QtCore import Qt, QCoreApplication
from som_gui.icons import get_icon
from som_gui import tool

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        from .qt.ui_Widget import Ui_Settings
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())

