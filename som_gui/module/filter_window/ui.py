from __future__ import annotations
from PySide6.QtWidgets import QWidget
from . import trigger


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        from .qt import ui_Settings

        self.ui = ui_Settings.Ui_FilterWindow()
        self.ui.setupUi(self)
        trigger.settings_widget_created(self)
