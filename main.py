# main.py
import logging
import os
import sys
from logging import config

from som_gui import logs, settings
from som_gui import core
from som_gui import tool

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
    import som_gui
    from PySide6.QtWidgets import QApplication
    import som_gui.core.main_window
    import som_gui.core.project

    print("START")
    som_gui.register()
    app = QApplication(sys.argv)
    core.main_window.create_main_window(app, tool.MainWindow)
    som_gui.load_ui_triggers()
    core.project.create_project(tool.Project)
    core.main_window.create_menus(tool.MainWindow, tool.Util)

    if initial_file is not None:
        core.project.open_project(initial_file, tool.Project)
    sys.exit(app.exec())


if __name__ == "__main__":
    start_log()
    main()
