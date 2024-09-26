from __future__ import annotations  # make own class referencable
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QComboBox, QWidget
from som_gui import icons
from som_gui.module import project
from .qt import settings_general, settings_path
class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = project.window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())

    def paintEvent(self, event):
        super().paintEvent(event)
        project.trigger.repaint_event()


class SettingsPath(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = settings_path.Ui_Form()
        self.ui.setupUi(self)
        project.trigger.settings_path_created(self)

class SettingsGeneral(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = settings_general.Ui_Form()
        self.ui.setupUi(self)
        project.trigger.settings_general_created(self)


class MergeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = project.window_merge.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.widget.tableWidget.setColumnCount(2)
        self.widget.tableWidget.setHorizontalHeaderLabels(["Importiert", "Bestand"])
