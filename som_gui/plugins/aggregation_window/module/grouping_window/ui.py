from PySide6.QtWidgets import QVBoxLayout, QWidget
from som_gui.icons import get_icon
from som_gui import tool
from .qt import ui_Widget

class GroupingWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = ui_Widget.Ui_Aggregation()
        self.ui.setupUi(self)
        self.setLayout(QVBoxLayout())
        self.setWindowIcon(get_icon())
