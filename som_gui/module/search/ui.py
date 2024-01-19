from som_gui.icons import get_icon
from PySide6.QtWidgets import QDialog
from . import window
from som_gui.module.search import trigger


class SearchWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.refresh_window()
