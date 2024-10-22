from __future__ import annotations

from typing import Type, TYPE_CHECKING
import os
from som_gui import tool
from PySide6.QtCore import QCoreApplication


def create_results(data_base_path: os.PathLike | str, results: Type[tool.ModelcheckResults],
                   modelcheck_window: Type[tool.ModelcheckWindow]):
    _issues = results.query_issues(data_base_path)
    text = QCoreApplication.translate("Modelcheck", "{} Issues found!").format(len(_issues))
    modelcheck_window.set_status(text)

    if len(_issues) == 0:
        modelcheck_window.set_status(QCoreApplication.translate("Modelcheck", "Model free of errors"))
        return
    workbook, worksheet = results.create_workbook()
    last_cell = results.fill_worksheet(_issues, worksheet)
    results.create_table(worksheet, last_cell)
    results.autofit_column_width(worksheet)
    save_workbook(workbook, results)


def save_workbook(workbook, results: Type[tool.ModelcheckResults]):
    path = results.get_export_path()
    try:
        workbook.save(path)
    except PermissionError:

        title = QCoreApplication.translate("Modelcheck", "Excel still open")
        text = QCoreApplication.translate("Modelcheck", "The output file is locked by another process")
        detail = QCoreApplication.translate("Modelcheck", "Path:'{}'\nWarning: file will be overridden!").format(path)
        if tool.Popups.file_in_use_warning(title, text, detail):
            save_workbook(workbook, results)
