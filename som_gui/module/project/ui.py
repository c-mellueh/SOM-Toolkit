from __future__ import annotations  # make own class referencable

from typing import TYPE_CHECKING
from som_gui import MainUi
from PySide6.QtWidgets import QDialog
import som_gui
from som_gui import icons
from som_gui.module import project


def load_triggers():
    MainUi.ui.action_settings.triggered.connect(project.trigger.menu_action_settings)

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = project.window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())

    def paintEvent(self, event):
        super().paintEvent(event)
        project.trigger.repaint_event()
