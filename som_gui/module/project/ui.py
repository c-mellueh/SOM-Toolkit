from __future__ import annotations  # make own class referencable

from PySide6.QtWidgets import QDialog, QWidget

from som_gui.module import project
from .qt import ui_ProjectMerge, ui_SettingsGeneral, ui_SettingsPath
from ...resources import icons


class SettingsPath(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = ui_SettingsPath.Ui_Project()
        self.ui.setupUi(self)
        project.trigger.settings_path_created(self)


class SettingsGeneral(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = ui_SettingsGeneral.Ui_Project()
        self.ui.setupUi(self)
        project.trigger.settings_general_created(self)


class MergeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = ui_ProjectMerge.Ui_Project()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.widget.tableWidget.setColumnCount(2)
        self.widget.tableWidget.setHorizontalHeaderLabels(
            [self.tr("Imported"), self.tr("Existing")]
        )
