from PySide6.QtWidgets import QDialog

from som_gui.module.search import trigger
from som_gui.resources.icons import get_icon
from .qt import ui_Widget


class SearchWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = ui_Widget.Ui_Search()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.refresh_window()
