from __future__ import annotations
from typing import TYPE_CHECKING, Type
import os
import json

if TYPE_CHECKING:
    from som_gui import tool
    from PySide6.QtWidgets import QGridLayout, QLineEdit, QWidget
from som_gui.module.exports.constants import *

names = [["Vestra", VESTRA_PATH, ],
         ["Card1", CARD1_PATH, ],
         ["Excel", EXCEL_PATH, ],
         ["Allplan", ALLPLAN_PATH, ],
         ["Desite Abkürzungen", ABBREV_PATH, ],
         ["Desite Lesezeichen", BOOKMARK_PATH, ],
         ["Desite Mapping", MAPPING_PATH, ], ]


def export_bookmarks(exports: Type[tool.Exports], main_window: Type[tool.MainWindow],
                     project: Type[tool.Project], popups: Type[tool.Popups], appdata: Type[tool.Appdata]):
    path = appdata.get_path(BOOKMARK_PATH)
    path = popups.get_folder(main_window.get(), path)
    if path:
        exports.export_bookmarks(project.get(), path)
        appdata.set_path(BOOKMARK_PATH, path)


def export_vestra_mapping(exports: Type[tool.Exports], main_window: Type[tool.MainWindow],
                          project: Type[tool.Project], appdata: Type[tool.Appdata]) -> None:
    export_path = appdata.get_path(VESTRA_PATH)
    if not export_path:
        export_path = str(os.getcwd() + "/")
        export_folder = exports.export_vestra(project.get(), main_window.get(), export_path)
        if export_folder:
            appdata.set_path(VESTRA_PATH, export_folder)


def export_card_1(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                  appdata: Type[tool.Appdata]) -> None:
    export_path = appdata.get_path(CARD1_PATH)
    if not export_path:
        export_path = str(os.getcwd() + "/")

    path = exports.export_card_1(project.get(), main_window.get(), export_path)
    if path:
        appdata.set_path(CARD1_PATH, path)


def export_excel(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                 appdata: Type[tool.Appdata], popups: Type[tool.Popups]):
    export_path = appdata.get_path(EXCEL_PATH)
    if export_path is None:
        export_path = str(os.getcwd() + "/")
    path = popups.get_save_path("Excel Files (*.xlsx);;", main_window.get(), export_path)
    if not path:
        return
    exports.export_excel(project.get(), path)
    appdata.set_path(EXCEL_PATH, path)


def export_mapping_script(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                          popups: Type[tool.Popups], appdata: Type[tool.Appdata]):
    name, answer = popups.req_export_pset_name(main_window.get())

    if not answer:
        return
    file_text = "JavaScript (*.js);;"
    path = popups.get_save_path(file_text, main_window.get(), appdata.get_path(MAPPING_PATH),
                                title="Export Mapping Script")
    if not path:
        return

    exports.create_mapping_script(project.get(), name, path)
    appdata.set_path(MAPPING_PATH, path)


def export_allplan_excel(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                         popups: Type[tool.Popups], appdata: Type[tool.Appdata]) -> None:
    name, answer = popups.req_export_pset_name(main_window)
    if not answer:
        return

    file_text = "Excel Files (*.xlsx);;"
    path = popups.get_save_path(file_text, main_window.get(), appdata.get_path(ALLPLAN_PATH))
    if not path:
        return
    if path:
        exports.export_allplan(project.get(), path, name)
        appdata.set_path(ALLPLAN_PATH, path)


def export_desite_abbreviation(main_window: Type[tool.MainWindow],
                               project: Type[tool.Project], appdata: Type[tool.Appdata],
                               popups: Type[tool.Popups]) -> None:
    path = popups.get_save_path("JSON (*.json);;", main_window.get(), appdata.get_path(ABBREV_PATH))
    if path is not None:
        abbrev = {obj.abbreviation: [obj.ident_value, obj.name] for obj in project.get().get_all_objects()}
        with open(path, "w") as file:
            json.dump(abbrev, file, indent=2)
        appdata.set_path(ABBREV_PATH, path)


def create_settings_ui(exports: Type[tool.Exports], appdata: Type[tool.Appdata]) -> QWidget:
    widget = exports.create_settings_widget([n[0] for n in names])
    for row, (name, path_name) in enumerate(names):
        layout: QGridLayout = widget.layout()
        line_edit: QLineEdit = layout.itemAtPosition(row, 1).widget()
        path = appdata.get_path(path_name)
        line_edit.setText(path)
    return widget


def settings_accepted(exports: Type[tool.Exports], appdata: Type[tool.Appdata]):
    widget = exports.get_settings_widget()
    for row, (name, path_name) in enumerate(names):
        layout: QGridLayout = widget.layout()
        line_edit: QLineEdit = layout.itemAtPosition(row, 1).widget()
        appdata.set_path(path_name, line_edit.text())
