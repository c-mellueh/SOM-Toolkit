from __future__ import annotations  # make own class referencable

from PySide6.QtWidgets import QDialog
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
