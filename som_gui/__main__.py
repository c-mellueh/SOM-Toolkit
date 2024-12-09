from __future__ import annotations
import sys
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QApplication

if TYPE_CHECKING:
    from os import PathLike

from som_gui import core,tool
import som_gui.core.main_window
import som_gui.core.project
from som_gui.module.project.constants import OPEN_PATH
from som_gui.module.language.trigger import set_language

print("HELLO WORLD")

def main(initial_file: PathLike | None = None, log_level=None, open_last_project=False):
    """
    Opens the Application and starts the GUI
    :param initial_file: SOMJson file that will be opened on startup
    :param log_level: Logging level that will be set on startup
    :param open_last_project: Should the last project be opened?
    :return:
    """
    print("START")

    if log_level is not None:
        tool.Logging.set_log_level(log_level)

    som_gui.register()

    #Create UI
    app = QApplication(sys.argv)
    core.main_window.create_main_window(app, tool.MainWindow)
    som_gui.load_ui_triggers()

    #create Empty Project (calls som_gui.on_new_project)
    core.project.create_project(tool.Project)

    if initial_file is not None:
        core.project.open_project(initial_file, tool.Project)

    elif open_last_project:
        core.project.open_project(tool.Appdata.get_path(OPEN_PATH), tool.Project)

    set_language(None)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
