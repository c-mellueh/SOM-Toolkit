from __future__ import annotations

import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFileDialog

from .. import settings

if TYPE_CHECKING:
    from ..main_window import MainWindow


def get_path(main_window: MainWindow, file_format: str) -> str:
    """ File Open Dialog with modifiable file_format"""
    path = settings.get_export_path()
    if path:
        basename = os.path.basename(path)
        split = os.path.splitext(basename)[0]
        filename_without_extension = os.path.splitext(split)[0]
        dirname = os.path.dirname(path)
        path = os.path.join(dirname, filename_without_extension)

    path = \
        QFileDialog.getSaveFileName(main_window, f"Save {file_format}", path,
                                    f"{file_format} Files (*.{file_format})")[0]
    if path:
        settings.set_export_path(path)
    return path


def get_folder(main_window: MainWindow) -> str:
    """Folder Open Dialog"""
    path = settings.get_export_path()
    if path:
        path = os.path.basename(path)
    path = \
        QFileDialog.getExistingDirectory(parent=main_window, dir=path)
    return path
