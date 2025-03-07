from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.tool.ifc_importer import IfcImportRunner
    from PySide6.QtWidgets import QPushButton
    import ifcopenshell
from som_gui import tool
from som_gui.plugins.ifc_tools.core import move as core
from som_gui.plugins.ifc_tools import tool as ifc_tool


def activate():
    core.create_main_menu_actions(ifc_tool.Move, tool.MainWindow)


def deactivate():
    pass

def open_window():
    core.open_window(ifc_tool.Move, tool.Util, tool.Appdata)


def button_box_clicked(button: QPushButton):
    bb = ifc_tool.Move.get_widget().ui.buttonBox
    if button == bb.button(bb.StandardButton.Apply):
        core.apply_clicked(ifc_tool.Move, tool.Util, tool.Appdata, tool.IfcImporter)
    if button == bb.button(bb.StandardButton.Close):
        core.close_clicked(ifc_tool.Move)


def on_new_project():
    pass


def ifc_import_started(runner: IfcImportRunner):
    core.ifc_import_started(runner, ifc_tool.Move)


def ifc_import_finished(runner: IfcImportRunner):
    core.ifc_import_finished(runner, ifc_tool.Move)


def move_started(ifc_file: ifcopenshell.file, path: str):
    core.move_started(ifc_file, path, ifc_tool.Move)


def move_finished():
    core.move_finished(ifc_tool.Move)


def retranslate_ui():
    core.retranslate_ui(ifc_tool.Move, tool.Util)
