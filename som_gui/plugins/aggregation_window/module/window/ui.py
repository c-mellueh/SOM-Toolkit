from PySide6.QtWidgets import QMainWindow, QMenuBar, QStatusBar, QVBoxLayout, QWidget, QComboBox
from PySide6.QtGui import QPaintEvent
from som_gui.icons import get_icon
from . import trigger
from PySide6.QtCore import Qt

class AggregationWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setCentralWidget(QWidget())
        self.central_layout = QVBoxLayout(self.centralWidget())
        self.setMenuBar(QMenuBar(self))
        self.setStatusBar(QStatusBar(self))
        self.resize(1245, 900)
        self.setWindowTitle(self.tr("Bauwerksstruktur"))
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
