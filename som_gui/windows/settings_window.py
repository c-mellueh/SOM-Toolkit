from __future__ import annotations  # make own class referencable

import logging
from typing import TYPE_CHECKING
import re

from PySide6.QtWidgets import QDialog
from ..qt_designs import ui_project_settings
from .. import icons
from .. import __version__
from ..data.constants import  PROJECT_PHASE_COUNT
if TYPE_CHECKING:
    from ..main_window import MainWindow


class SettingsDialog(QDialog):
    def __init__(self,main_window:MainWindow):
        super(SettingsDialog, self).__init__()
        widget = ui_project_settings.Ui_Dialog()
        widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.setWindowTitle(f"SOM-Toolkit Version {__version__}")
        widget.lineEdit_project_name.setText(main_window.project.name)
        widget.lineEdit_author.setText(main_window.project.author)
        widget.lineEdit_version.setText(main_window.project.version)

        prefix = "Leistungsphase "
        widget.combo_box_project_phase.addItems([f"{prefix}{x+1}" for x in range(PROJECT_PHASE_COUNT)])
        widget.combo_box_project_phase.setCurrentText(f"{prefix}{main_window.project.current_project_phase}")

        if self.exec():
            main_window.project.name = widget.lineEdit_project_name.text()
            main_window.project.author = widget.lineEdit_author.text()
            main_window.project.version = widget.lineEdit_version.text()
            main_window.generate_window_title()
            project_phase_text = widget.combo_box_project_phase.currentText()
            match = re.match(f"{prefix}(\d+)", project_phase_text)

            project_phase = match.group(1)
            if project_phase is None:
                logging.error(f"Projectphase could not be found from '{project_phase_text}'")
            else:
                main_window.project.current_project_phase = int(project_phase)
            main_window.generate_window_title()