from PySide6.QtWidgets import QVBoxLayout, QWidget
from som_gui.icons import get_icon


class GroupingWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr(f"Gruppierung erzeugen"))
        self.setMinimumWidth(600)
