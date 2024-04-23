from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFileDialog
from SOMcreator import classes, vestra, card1, filehandling, allplan
from SOMcreator import excel as som_excel
from SOMcreator.external_software.desite import modelcheck, bookmarks, building_structure, bill_of_quantities

from .. import settings
from ..windows import popups
from SOMcreator.tool import ExportExcel

if TYPE_CHECKING:
    from ..main_window import MainWindow


def get_path(main_window: MainWindow, file_format: str) -> str:
    """ File Open Dialog with modifiable file_format"""
    path = settings.get_export_path()
    if path:
        basename = os.path.basename(path)
        split = os.path.splitext(basename)[0]
        filename_without_extension = os.path.splitext(split)[0]
        dirname = os.path.dirname(path)
        path = os.path.join(dirname, filename_without_extension)

    path = \
        QFileDialog.getSaveFileName(main_window, f"Save {file_format}", path,
                                    f"{file_format} Files (*.{file_format})")[0]
    if path:
        settings.set_export_path(path)
    return path


def get_folder(main_window: MainWindow) -> str:
    """Folder Open Dialog"""
    path = settings.get_export_path()
    if path:
        path = os.path.basename(path)
    path = \
        QFileDialog.getExistingDirectory(parent=main_window, dir=path)
    return path


def export_building_structure(main_window: MainWindow):
    """Exports dummy Building Structure for Desite"""
    path = get_path(main_window, "bs.xml")
    if path:
        building_structure.export_bs(main_window.project, path)


def export_bookmarks(main_window: MainWindow):
    path = get_folder(main_window)
    if path:
        bookmarks.export_bookmarks(main_window.project, path)

def export_vestra_mapping(main_window: MainWindow) -> None:
    file_text = "Excel Files (*.xlsx);;"
    export_path = settings.get_export_path()
    if not export_path:
        export_path = str(os.getcwd() + "/")
    excel_path, answer = QFileDialog.getOpenFileName(main_window, "Template Excel", export_path, file_text)
    if answer:
        export_folder = QFileDialog.getExistingDirectory(main_window, "Export Folder", export_path)
        if export_folder:
            vestra.create_mapping(excel_path, export_folder, main_window.project)
            settings.set_export_path(export_folder)


def export_card_1(main_window: MainWindow) -> None:
    file_text = "Excel Files (*.xlsx);;"
    export_path = settings.get_export_path()
    if not export_path:
        export_path = str(os.getcwd() + "/")

    src, answer = QFileDialog.getOpenFileName(main_window, "Template Excel", export_path, file_text)
    if not answer:
        return
    path = QFileDialog.getSaveFileName(main_window, "CARD1 Excel", export_path, file_text)[0]

    if path:
        card1.create_mapping(src, path, main_window.project)
        settings.set_export_path(path)


def export_excel(main_window: MainWindow):
    export_path = settings.get_export_path()
    if export_path is None:
        export_path = str(os.getcwd() + "/")
    path = QFileDialog.getSaveFileName(main_window, "SOM Excel", export_path, "Excel Files (*.xlsx);;")[0]
    if not path:
        return
    som_excel.export(main_window.project, path, ExportExcel)
    settings.set_export_path(path)


def export_mapping_script(main_window: MainWindow):
    name, answer = popups.req_export_pset_name(main_window)

    if not answer:
        return
    export_path = settings.get_export_path()
    file_text = "JavaScript (*.js);;"
    if export_path is None:
        export_path = str(os.getcwd() + "/")

    path = QFileDialog.getSaveFileName(main_window, "Safe Mapping Script", export_path, file_text)[0]
    if not path:
        return

    project = main_window.project
    filehandling.create_mapping_script(project, name, path)
    settings.set_export_path(path)


def export_allplan_excel(main_window: MainWindow) -> None:
    file_text = "Excel Files (*.xlsx);;"
    export_path = settings.get_export_path()
    if export_path is None:
        export_path = str(os.getcwd() + "/")
    name, answer = popups.req_export_pset_name(main_window)
    if not answer:
        return
    path = QFileDialog.getSaveFileName(main_window, "Safe Attribute Excel", export_path, file_text)[0]

    if path:
        allplan.create_mapping(main_window.project, path, name)
        settings.set_export_path(path)


def export_desite_abbreviation(main_window: MainWindow) -> None:
    abbrev = {obj.abbreviation: [obj.ident_value, obj.name] for obj in
              main_window.project.objects}
    export_path = settings.get_export_path()
    file_text = "JSON (*.json);;"
    path = QFileDialog.getSaveFileName(main_window, "Abbreviations File", export_path, file_text)[0]
    if path is not None:
        with open(path, "w") as file:
            json.dump(abbrev, file, indent=2)

        settings.set_export_path(path)
