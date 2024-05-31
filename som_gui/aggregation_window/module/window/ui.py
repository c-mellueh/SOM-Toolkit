from PySide6.QtWidgets import QMainWindow, QMenuBar, QStatusBar, QVBoxLayout, QWidget, QComboBox
from som_gui.icons import get_icon

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


class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
