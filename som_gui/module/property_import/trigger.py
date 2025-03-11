from __future__ import annotations
from typing import TYPE_CHECKING
import ifcopenshell
from PySide6.QtWidgets import QPushButton

from som_gui import tool
from som_gui.core import property_import as core
from som_gui.tool.ifc_importer import IfcImportRunner

if TYPE_CHECKING:
    from som_gui.tool.property_import import PropertyImportRunner


def connect():
    core.create_main_menu_actions(tool.PropertyImport, tool.MainWindow)


def open_import_window():
    core.open_import_window(
        tool.PropertyImport,
        tool.PropertyImportResults,
        tool.IfcImporter,
        tool.Project,
        tool.PropertyImportSQL,
    )


def open_results_window():
    core.open_results_window(tool.PropertyImportResults)


def retranslate_ui():
    core.retranslate_ui(tool.PropertyImport, tool.PropertyImportResults, tool.Util)


def connect_import_buttons(run_button: QPushButton, abort_button: QPushButton):
    run_button.clicked.connect(
        lambda: core.ifc_import_run_clicked(
            tool.PropertyImport,
            tool.IfcImporter,
            tool.PropertyImportSQL,
            tool.Project,
            tool.Util,
        )
    )
    abort_button.clicked.connect(lambda: core.abort_clicked())


def connect_ifc_import_runner(runner: IfcImportRunner):
    runner.signaller.started.connect(
        lambda: core.ifc_import_started(runner, tool.PropertyImport, tool.IfcImporter)
    )
    runner.signaller.finished.connect(
        lambda: core.ifc_import_finished(runner, tool.PropertyImport, tool.IfcImporter)
    )
    runner.signaller.status.connect(
        lambda s: tool.Util.set_status(runner.progress_bar, s)
    )
    runner.signaller.progress.connect(
        lambda p: tool.Util.set_progress(runner.progress_bar, p)
    )


def connect_property_import_runner(runner: PropertyImportRunner):
    runner.signaller.finished.connect(
        lambda: core.property_import_finished(tool.PropertyImport, tool.IfcImporter)
    )
    runner.signaller.status.connect(
        lambda s: tool.Util.set_status(runner.progress_bar, s)
    )
    runner.signaller.progress.connect(
        lambda p: tool.Util.set_progress(runner.progress_bar, p)
    )


def last_import_finished():
    core.last_import_finished(tool.PropertyImport, tool.PropertyImportSQL)


def start_property_import(runner: PropertyImportRunner):
    core.start_property_import(
        runner,
        tool.PropertyImport,
        tool.PropertyImportResults,
        tool.PropertyImportSQL,
        tool.Project,
    )


def update_ifc_type_combobox():
    core.update_ifctype_combobox(
        tool.PropertyImportResults, tool.PropertyImportSQL, tool.Project
    )


def update_identifier_combobox():
    core.update_identifier_combobox(
        tool.PropertyImportResults, tool.PropertyImportSQL, tool.Project
    )


def update_class_count():
    core.update_class_count(tool.PropertyImportResults, tool.PropertyImportSQL)


def update_import_window():
    core.update_results_window(tool.PropertyImportResults)


def pset_table_selection_changed():
    core.update_property_table(tool.PropertyImportResults, tool.PropertyImportSQL)


def property_table_selection_changed():
    core.update_value_table(tool.PropertyImportResults, tool.PropertyImportSQL)


def value_checkstate_changed(check_box):
    core.value_checkstate_changed(
        check_box, tool.PropertyImportResults, tool.PropertyImportSQL
    )


def update_property_set_table():
    core.update_property_set_table(tool.PropertyImportResults, tool.PropertyImportSQL)


def update_all_checkbox():
    core.update_all_checkbox(tool.PropertyImportResults)


def update_property_table():
    core.update_property_table(tool.PropertyImportResults, tool.PropertyImportSQL)


def update_value_table():
    core.update_value_table(tool.PropertyImportResults, tool.PropertyImportSQL)


def all_checkbox_checkstate_changed():
    core.all_checkbox_checkstate_changed(
        tool.PropertyImportResults, tool.PropertyImportSQL
    )


def result_abort_clicked():
    core.results_abort_clicked(tool.PropertyImportResults)


def result_acccept_clicked():
    core.import_values_to_som(
        tool.PropertyImportResults, tool.PropertyImportSQL, tool.Project
    )


def settings_clicked():
    core.settings_clicked(tool.PropertyImportResults, tool.PropertyImportSQL, tool.Util)


def on_new_project():
    pass


def download_clicked():
    core.export_properties(
        tool.PropertyImportResults, tool.PropertyImportSQL, tool.Appdata, tool.Popups
    )
