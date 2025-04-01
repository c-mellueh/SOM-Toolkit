from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import usecases as core
from typing import TYPE_CHECKING


def connect():
    core.create_main_menu_actions(tool.Usecases,tool.MainWindow)
    pass

def retranslate_ui():
    pass

def on_new_project():
    pass

def open_window():
    core.open_window(tool.Usecases,tool.Project,tool.Util,tool.Search)
