from __future__ import annotations

from typing import Type, TYPE_CHECKING
import os
import logging

if TYPE_CHECKING:
    from som_gui import tool

HEADER = ["Datum", "GUID", "Beschreibung", "Typ", "Name", "PropertySet", "Attribut", "Datei",
          "Bauteilklassifikation"]


def create_results(data_base_path: os.PathLike | str, results: Type[tool.ModelcheckResults],
                   modelcheck_window: Type[tool.ModelcheckWindow]):
    _issues = results.query_issues(data_base_path)
    modelcheck_window.set_status(f"{len(_issues)} Fehler gefunden!")

    if len(_issues) == 0:
        modelcheck_window.set_status("Modelle fehlerfrei!")

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
        logging.warning("-" * 60)
        logging.warning(f"folgende Datei ist noch geöffnet: {path} \n Datei schließen und beliebige Taste Drücken")
        input("Achtung! Datei wird danach überschrieben!")
        save_workbook(workbook, path)
