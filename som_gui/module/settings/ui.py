from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QDialog, QDialogButtonBox
from PySide6.QtCore import Qt
from som_gui.icons import get_icon
class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.layout().addWidget(self.tab_widget)
        self.button_box = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout().addWidget(self.button_box)

        self.setWindowTitle('Settings')
        self.setWindowIcon(get_icon())
