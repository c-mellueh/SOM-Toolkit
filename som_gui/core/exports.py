from __future__ import annotations
from typing import TYPE_CHECKING, Type
import os
import json

if TYPE_CHECKING:
    from som_gui import tool


def export_bookmarks(exports: Type[tool.Exports], main_window: Type[tool.MainWindow],
                     project: Type[tool.Project], popups: Type[tool.Popups], ):
    path = popups.get_folder(main_window.get())
    if path:
        exports.export_bookmarks(project.get(), path)


def export_vestra_mapping(exports: Type[tool.Exports], main_window: Type[tool.MainWindow],
                          project: Type[tool.Project], settings: Type[tool.Settings]) -> None:
    export_path = settings.get_export_path()
    if not export_path:
        export_path = str(os.getcwd() + "/")
        export_folder = exports.export_vestra(project.get(), main_window.get(), export_path)
        if export_folder:
            settings.set_export_path(export_folder)


def export_card_1(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                  settings: Type[tool.Settings]) -> None:
    export_path = settings.get_export_path()
    if not export_path:
        export_path = str(os.getcwd() + "/")

    path = exports.export_card_1(project.get(), main_window.get(), export_path)
    if path:
        settings.set_export_path(path)


def export_excel(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                 settings: Type[tool.Settings], popups: Type[tool.Popups]):
    export_path = settings.get_export_path()
    if export_path is None:
        export_path = str(os.getcwd() + "/")
    path = popups.get_path("Excel Files (*.xlsx);;", main_window.get(), export_path)
    if not path:
        return
    exports.export_excel(project.get(), path)
    settings.set_export_path(path)


def export_mapping_script(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                          popups: Type[tool.Popups], settings: Type[tool.Settings]):
    name, answer = popups.req_export_pset_name(main_window.get())

    if not answer:
        return
    file_text = "JavaScript (*.js);;"
    path = popups.get_path(file_text, main_window.get(), settings.get_export_path(), save=True,
                           title="Export Mapping Script")
    if not path:
        return

    exports.create_mapping_script(project.get(), name, path)
    settings.set_export_path(path)


def export_allplan_excel(exports: Type[tool.Exports], main_window: Type[tool.MainWindow], project: Type[tool.Project],
                         popups: Type[tool.Popups], settings: Type[tool.Settings]) -> None:
    name, answer = popups.req_export_pset_name(main_window)
    if not answer:
        return

    file_text = "Excel Files (*.xlsx);;"
    path = popups.get_path(file_text, main_window.get(), settings.get_export_path())
    if not path:
        return
    if path:
        exports.export_allplan(project.get(), path, name)
        settings.set_export_path(path)


def export_desite_abbreviation(exports: Type[tool.Exports], main_window: Type[tool.MainWindow],
                               project: Type[tool.Project], settings: Type[tool.Settings],
                               popups: Type[tool.Popups]) -> None:
    path = popups.get_path("JSON (*.json);;", main_window.get(), )
    if path is not None:
        abbrev = {obj.abbreviation: [obj.ident_value, obj.name] for obj in project.get().get_all_objects()}
        with open(path, "w") as file:
            json.dump(abbrev, file, indent=2)
        settings.set_export_path(path)
