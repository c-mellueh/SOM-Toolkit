from PySide6.QtWidgets import QMainWindow, QComboBox
from PySide6.QtGui import QPaintEvent
from som_gui.resources.icons import get_icon
from . import trigger
from PySide6.QtCore import Qt


class AggregationWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        from .qt.ui_Window import Ui_Aggregation
        super().__init__(*args, **kwargs)
        self.ui = Ui_Aggregation()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon())

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        trigger.window_paint_event()


class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.currentIndexChanged.connect(trigger.combo_box_changed)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        trigger.update_combo_box()
