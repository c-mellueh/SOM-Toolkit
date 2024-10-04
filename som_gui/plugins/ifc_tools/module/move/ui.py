from .qt import widget
from PySide6.QtWidgets import QWidget
import som_gui


class MoveWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = widget.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(f"IFC Verschieben {som_gui.tool.Util.get_status_text()}")
        self.setWindowIcon(som_gui.get_icon())
