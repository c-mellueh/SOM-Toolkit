from __future__ import annotations  # make own class referencable

import logging
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QDialog
from ..qt_designs import ui_project_settings
from .. import icons
from .. import __version__

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

        if self.exec():
            main_window.project.name = widget.lineEdit_project_name.text()
            main_window.project.author = widget.lineEdit_author.text()
            main_window.project.version = widget.lineEdit_version.text()
            main_window.generate_window_title()