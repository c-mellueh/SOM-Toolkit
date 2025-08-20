from PySide6.QtWidgets import QWidget

from . import qt


class IfcImportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = qt.Ui_IfcImporter()
        self.ui.setupUi(self)
