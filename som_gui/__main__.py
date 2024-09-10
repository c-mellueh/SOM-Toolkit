import som_gui

import logging
import os
import sys
from logging import config

from som_gui import core
from som_gui import tool
import ifcopenshell.guid
import ifcopenshell.express


def start_log(level: int | None = None) -> None:
    tool.Logging.set_log_level(level)


def main(initial_file: str | None = None, log_level=None):
    print("START")
    from PySide6.QtWidgets import QApplication
    import som_gui.core.main_window
    import som_gui.core.project
    if log_level == None:
        log_level = logging.WARNING

    som_gui.register()
    tool.Logging.set_log_level(log_level)
    app = QApplication(sys.argv)
    core.main_window.create_main_window(app, tool.MainWindow)
    som_gui.load_ui_triggers()
    core.project.create_project(tool.Project)
    core.main_window.create_menus(tool.MainWindow, tool.Util)
    if initial_file is not None:
        core.project.open_project(initial_file, tool.Project)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
