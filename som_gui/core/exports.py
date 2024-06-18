from __future__ import annotations
from typing import TYPE_CHECKING, Type
from som_gui import settings
import os
import json

if TYPE_CHECKING:
    from som_gui import tool


def export_bookmarks(exports: Type[tool.Exports], main_window: Type[tool.MainWindow],
                     project: Type[tool.Project]):
    path = exports.get_folder(main_window.get())
    if path:
        exports.export_bookmarks(project.get(), path)


def export_vestra_mapping(exports: Type[tool.Exports], main_window: Type[tool.MainWindow],
                          project: Type[tool.Project]) -> None:
    export_path = settings.get_export_path()
    if not export_path:
        export_path = str(os.getcwd() + "/")
        exports.export_vestra(project.get(), main_window.get(), export_path)


def export_card_1(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project]) -> None:
    export_path = settings.get_export_path()
    if not export_path:
        export_path = str(os.getcwd() + "/")

    exports.export_card_1(project.get(), main_window.get(), export_path)


def export_excel(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project]):
    export_path = settings.get_export_path()
    if export_path is None:
        export_path = str(os.getcwd() + "/")
    path = exports.get_path(main_window.get(), "Excel Files (*.xlsx);;")
    if not path:
        return
    exports.export_excel(project.get(), path)
    settings.set_export_path(path)


def export_mapping_script(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                          popups: Type[tool.Popups]):
    name, answer = popups.req_export_pset_name(main_window)

    if not answer:
        return
    file_text = "JavaScript (*.js);;"
    path = exports.get_path(main_window.get(), file_text)
    if not path:
        return

    exports.create_mapping_script(project.get(), name, path)
    settings.set_export_path(path)


def export_allplan_excel(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                         popups: Type[tool.Popups]) -> None:
    name, answer = popups.req_export_pset_name(main_window)
    if not answer:
        return

    file_text = "Excel Files (*.xlsx);;"
    path = exports.get_path(main_window.get(), file_text)
    if not path:
        return
    if path:
        exports.export_allplan(project.get(), path, name)
        settings.set_export_path(path)


def export_desite_abbreviation(exports: Type[tool.Exports], main_window: Type[tool.MainWindow],
                               project: Type[tool.Project]) -> None:
    path = exports.get_path(main_window.get(), "JSON (*.json);;")
    if path is not None:
        abbrev = {obj.abbreviation: [obj.ident_value, obj.name] for obj in project.get().get_all_objects()}
        with open(path, "w") as file:
            json.dump(abbrev, file, indent=2)
        settings.set_export_path(path)
