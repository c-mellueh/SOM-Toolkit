from __future__ import annotations

import re
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget, QListWidgetItem
from SOMcreator import classes, constants

from .. import icons
from ..qt_designs import ui_project_phase_window
from ..windows import popups

if TYPE_CHECKING:
    from ..main_window import MainWindow


class ProjectPhaseWindow(QWidget):
    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            pass

        super().__init__()
        self.widget = ui_project_phase_window.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.main_window = main_window
        connect()
