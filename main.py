# main.py
import logging
import os
import sys
from logging import config

import som_gui
from som_gui import logs, settings
from som_gui.core import project
from som_gui.tool import Project
# import ifcopenshell.express.rules.IFC2X3 as IFC2X3


def start_log(state: int | None = None) -> None:
    if not os.path.exists(logs.DIR_PATH):
        os.mkdir(logs.DIR_PATH)
    config.fileConfig(
        settings.LOG_CONFIG_PATH,
        defaults={"logfilename": logs.LOG_PATH.replace("\\", "/")},
    )
    if state is None:
        return
    if logging.getLogger("root") is None:
        return
    sh_list = [
        handler
        for handler in logging.getLogger("root").handlers
        if isinstance(handler, logging.StreamHandler)
    ]
    for handler in sh_list:
        handler.setLevel(state)


def main(initial_file: str | None = None):
    from PySide6.QtWidgets import QApplication
    from som_gui import main_window

    print("START")
    app = QApplication(sys.argv)
    window = main_window.MainWindow(app)
    window.show()
    project.create_project(Project)
    som_gui.load_ui_triggers()
    if initial_file is not None:
        project.open_project(initial_file, Project)
    sys.exit(app.exec())


if __name__ == "__main__":
    start_log()
    main()
