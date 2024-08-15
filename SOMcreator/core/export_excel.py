from __future__ import annotations
from SOMcreator import classes
from SOMcreator.tool import ExportExcel
from typing import Type
import os


def export(project: classes.Project, path: str, export_excel: Type[ExportExcel], ident_pset_name: str = None,
           ident_attribute_name: str = None) -> None:
    if not export_excel.directory_of_path_exists(path):
        raise FileNotFoundError(f"path {os.path.dirname(path)} DNE")

    if None not in (ident_pset_name, ident_attribute_name):
        export_excel.set_ident_values(ident_pset_name, ident_attribute_name)

    export_excel.set_project(project)
    workbook = export_excel.create_workbook()
    sheet_main = workbook.active
    export_excel.fill_main_sheet(sheet_main)
    sheet_dict = export_excel.filter_to_sheets()

    table_counter = 1
    for ident, data_dict in sheet_dict.items():
        obj_name, objects = export_excel.get_object_data(data_dict)
        work_sheet = workbook.create_sheet(f"{obj_name} ({ident})")
        for counter, obj in enumerate(sorted(objects)):
            column = 1 + counter * 5
            export_excel.create_object_entry(obj, work_sheet, 1, column, table_counter)
            table_counter += 1
        export_excel.autoadjust_column_widths(work_sheet)
    workbook.save(path)
