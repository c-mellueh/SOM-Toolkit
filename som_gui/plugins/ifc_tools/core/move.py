from __future__ import annotations
from typing import TYPE_CHECKING, Type
import logging
import os
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
SECTION_NAME = "IfcMove"
X_PATH = "x"
Y_PATH = "y"
Z_PATH = "z"
if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.plugins.ifc_tools import tool as ifc_tool
    from som_gui.tool.ifc_importer import IfcImportRunner
    import ifcopenshell


def create_main_menu_actions(move: Type[ifc_tool.Move], main_window: Type[tool.MainWindow]):
    from som_gui.plugins.ifc_tools.module.move import trigger
    move_menu = main_window.add_submenu(None, "_IfcTool")
    action = move_menu.addAction("_Move")
    action.triggered.connect(trigger.open_window)
    move.set_action("open_window", action)
    move.set_action("menu", move_menu)


def retranslate_ui(move: Type[ifc_tool.Move], util: Type[tool.Util]):
    action = move.get_action("open_window")
    action.setText(QCoreApplication.translate("Move", "Move"))
    menu: QMenu = move.get_action("menu")
    menu.setTitle(QCoreApplication.translate("IfcTools", "Ifc-Tool"))

    widget = move.get_widget()
    if not widget:
        return
    widget.ui.widget_file_selector.name = QCoreApplication.translate("Move", "IFC Path")
    widget.ui.retranslateUi(widget)
    title = QCoreApplication.translate("Move", "Move")

    widget.setWindowTitle(f"{title} | {util.get_status_text()}")


def open_window(move: Type[ifc_tool.Move], util: Type[tool.Util], appdata: Type[tool.Appdata]):
    widget = move.get_widget()
    if widget is None:
        widget = move.create_widget()

    util.fill_file_selector(widget.ui.widget_file_selector, "_IFC path", "IFC Files (*.ifc *.IFC);;", "ifc_move")

    coordinates: tuple[float, float, float] = tuple(
        [appdata.get_float_setting(SECTION_NAME, path_name, 0.) for path_name in [X_PATH, Y_PATH, Z_PATH]])
    move.set_coordinate_values(coordinates)
    widget.ui.widget_progress_bar.hide()
    move.reset_buttons()
    retranslate_ui(move, util)
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

    status = QCoreApplication.translate("Move", "Import '{}'").format(file_name)
    move.set_status(status, 0)


def ifc_import_finished(runner: IfcImportRunner, move: Type[ifc_tool.Move]):
    logging.info(f"IfcImport is finished")
    move_runner = move.create_move_runner(runner.ifc, runner.path)
    status = QCoreApplication.translate("Move", "Import Done!")

    move.set_status(status, 0)
    move.get_threadpool().start(move_runner)


def move_started(ifc_file: ifcopenshell.file, export_path, move: Type[ifc_tool.Move]):
    logging.debug(f"Move Started")
    coordinates = move.get_coordinate_values()

    status = QCoreApplication.translate("Move", "Move '{}'").format(os.path.basename(export_path))
    move.set_status(status, 0)
    move.move_ifc(ifc_file, export_path, coordinates)

    status = QCoreApplication.translate("Move", "Move Done!")
    move.set_status(status, 100)


def move_finished(move: Type[ifc_tool.Move]):
    logging.debug(f"Move finished")
    move.reset_buttons()
