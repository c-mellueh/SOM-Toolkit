from PySide6.QtWidgets import QVBoxLayout, QWidget
from som_gui.icons import get_icon
from som_gui import tool


class GroupingWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr(f"Gruppierung erzeugen | {tool.Util.get_status_text()}"))
        self.setMinimumWidth(600)
