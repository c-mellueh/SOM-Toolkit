from PySide6.QtWidgets import QWidget

from . import qt


class IfcImportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = qt.Ui_IfcImporter()
        self.widget.setupUi(self)
