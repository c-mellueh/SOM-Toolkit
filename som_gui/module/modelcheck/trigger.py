from __future__ import annotations
from typing import TYPE_CHECKING
from som_gui import tool
from som_gui.core import modelcheck as core

if TYPE_CHECKING:
    from .ui import ModelcheckWindow


def connect():
    tool.MainWindow.add_action("Modelcheck/Interne Modellprüfung",
                               lambda: core.open_window(tool.Modelcheck, tool.IfcImporter))


def connect_window(widget: ModelcheckWindow):
    pass


def on_new_project():
    pass
