from __future__ import annotations

import os
from typing import Type

from PySide6.QtCore import QCoreApplication

from som_gui import tool


def create_results(data_base_path: os.PathLike | str, results: Type[tool.ModelcheckResults],
                   modelcheck_window: Type[tool.ModelcheckWindow], popups: Type[tool.Popups]):
    _issues = results.query_issues(data_base_path)
    issue_count = len(_issues)
    if issue_count:
        text = QCoreApplication.translate("Modelcheck", "{} Issues found!").format(issue_count)
    else:
        text = QCoreApplication.translate("Modelcheck", "Model free of errors")

    popups.create_info_popup(text, QCoreApplication.translate("Modelcheck", "Modelcheck done!"))

    if issue_count == 0:
        return
    modelcheck_window.set_progress_bar_layout_visible(False)
    modelcheck_window.clear_progress_bars()
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
