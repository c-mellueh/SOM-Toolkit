from __future__ import annotations  # make own class referencable

from PySide6.QtWidgets import QDialog, QTableWidgetItem, QComboBox
from som_gui import icons
from som_gui.module import project

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = project.window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())

    def paintEvent(self, event):
        super().paintEvent(event)
        project.trigger.repaint_event()


class MergeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = project.window_merge.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.widget.tableWidget.setColumnCount(2)
        self.widget.tableWidget.setHorizontalHeaderLabels(["Importiert", "Bestand"])
