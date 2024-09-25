from __future__ import annotations
from som_gui import tool
from som_gui.core import settings as core
from typing import TYPE_CHECKING


def connect():
    tool.MainWindow.add_action("Bearbeiten/Properties",
                               lambda: core.open_window(tool.Settings))


def on_new_project():
    pass
