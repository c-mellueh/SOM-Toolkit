from PySide6.QtWidgets import QMainWindow, QMenuBar, QStatusBar, QVBoxLayout, QWidget, QComboBox
from som_gui.icons import get_icon
from . import trigger
class AggregationWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCentralWidget(QWidget())
        self.central_layout = QVBoxLayout(self.centralWidget())
        self.setMenuBar(QMenuBar(self))
        self.setStatusBar(QStatusBar(self))
        self.resize(1245, 900)
        self.setWindowTitle(self.tr("Bauwerksstruktur"))
        self.setWindowIcon(get_icon())

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.window_paint_event()

class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentIndexChanged.connect(trigger.combo_box_changed)
    def paintEvent(self, e):
        super().paintEvent(e)
        trigger.update_combo_box()
