from __future__ import annotations

import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFileDialog

if TYPE_CHECKING:
    from desiteRuleCreator.main_window import MainWindow


def get_path(main_window: MainWindow, file_format: str) -> str:
    """ File Open Dialog with modifiable file_format"""
    if main_window.export_path is not None:
        basename = os.path.basename(main_window.export_path)
        split = os.path.splitext(basename)[0]
        filename_without_extension = os.path.splitext(split)[0]
        dirname = os.path.dirname(main_window.export_path)
        proposal = os.path.join(dirname, filename_without_extension)
        path = \
            QFileDialog.getSaveFileName(main_window, f"Save {file_format}", proposal,
                                        f"{file_format} Files (*.{file_format})")[0]
    else:
        path = \
            QFileDialog.getSaveFileName(main_window, f"Save {file_format}", "",
                                        f"{file_format} Files (*.{file_format})")[0]

    return path
