from __future__ import annotations
from typing import TYPE_CHECKING, Type
import logging
import os

SECTION_NAME = "IfcMove"
X_PATH = "x"
Y_PATH = "y"
Z_PATH = "z"
if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.plugins.ifc_tools import tool as ifc_tool
    from som_gui.tool.ifc_importer import IfcImportRunner
    import ifcopenshell


def open_window(move: Type[ifc_tool.Move], util: Type[tool.Util], appdata: Type[tool.Appdata]):
    widget = move.get_widget()
    if widget is None:
        widget = move.create_widget()
    util.fill_file_selector(widget.ui.widget_file_selector, "IFC Pfad", "IFC Files (*.ifc *.IFC);;", "ifc_move")

    coordinates: tuple[float, float, float] = tuple(
        [appdata.get_float_setting(SECTION_NAME, path_name, 0.) for path_name in [X_PATH, Y_PATH, Z_PATH]])
    move.set_coordinate_values(coordinates)
    widget.ui.widget_progress_bar.hide()
    move.reset_buttons()
    widget.show()


def apply_clicked(move: Type[ifc_tool.Move], util: Type[tool.Util], appdata: Type[tool.Appdata],
                  ifc_importer: Type[tool.IfcImporter]):
    logging.debug("Apply Clicked")
    widget = move.get_widget()
    path_list = util.get_path_from_fileselector(widget.ui.widget_file_selector)
    coordinates = move.get_coordinate_values()
    widget.ui.buttonBox.setStandardButtons(widget.ui.buttonBox.StandardButton.Close)
    for value, settings_path in zip(coordinates, [X_PATH, Y_PATH, Z_PATH]):
        appdata.set_setting(SECTION_NAME, settings_path, value)

    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(3)
    widget.ui.widget_progress_bar.show()
    for path in path_list:
        runner = ifc_importer.create_runner(widget.ui.widget_progress_bar.ui.label, path)
        move.connect_runner(runner)
        pool.start(runner)


def close_clicked(move: Type[ifc_tool.Move]):
    widget = move.get_widget()
    widget.hide()


def ifc_import_started(runner: IfcImportRunner, move: Type[ifc_tool.Move]):
    logging.debug(f"Importer Started")
    file_name = os.path.basename(runner.path)
    move.set_status(f"Import {file_name}", 0)


def ifc_import_finished(runner: IfcImportRunner, move: Type[ifc_tool.Move]):
    logging.info(f"IfcImport is finished")
    move_runner = move.create_move_runner(runner.ifc, runner.path)
    move.set_status(f"Import Done!", 0)
    move.get_threadpool().start(move_runner)


def move_started(ifc_file: ifcopenshell.file, export_path, move: Type[ifc_tool.Move]):
    logging.debug(f"Move Started")
    coordinates = move.get_coordinate_values()
    move.set_status(f"Move {os.path.basename(export_path)}", 0)
    move.move_ifc(ifc_file, export_path, coordinates)
    move.set_status(f"Move Done!", 100)


def move_finished(move: Type[ifc_tool.Move]):
    logging.debug(f"Move finished")
    move.reset_buttons()
