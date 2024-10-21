from PySide6.QtWidgets import QPushButton
import ifcopenshell
from som_gui import tool, tr
from som_gui.core import attribute_import as core
from PySide6.QtCore import QCoreApplication


def connect():
    core.create_main_menu_actions(tool.AttributeImport, tool.MainWindow)


def open_window():
    core.open_import_window(tool.AttributeImport, tool.AttributeImportResults, tool.IfcImporter, tool.Project,
                            tool.AttributeImportSQL)

def retranslate_ui():
    core.retranslate_ui(tool.AttributeImport)

def connect_import_buttons(run_button: QPushButton, abort_button: QPushButton):
    run_button.clicked.connect(
        lambda: core.ifc_import_run_clicked(tool.AttributeImport, tool.IfcImporter, tool.AttributeImportSQL,
                                            tool.Project,
                                            tool.Util))
    abort_button.clicked.connect(lambda: core.abort_clicked())


def connect_ifc_import_runner(runner):
    runner.signaller.started.connect(lambda: core.ifc_import_started(runner, tool.AttributeImport, tool.IfcImporter))
    runner.signaller.finished.connect(lambda: core.ifc_import_finished(runner, tool.AttributeImport, tool.IfcImporter))


def connect_attribute_import_runner(runner):
    runner.signaller.finished.connect(
        lambda: core.attribute_import_finished(tool.AttributeImport, tool.IfcImporter))
    runner.signaller.status.connect(tool.ModelcheckWindow.set_status)
    runner.signaller.progress.connect(tool.ModelcheckWindow.set_progress)


def on_new_project():
    pass


def last_import_finished():
    core.last_import_finished(tool.AttributeImport, tool.AttributeImportResults, tool.AttributeImportSQL)


def start_attribute_import(file: ifcopenshell.file, path: str):
    core.start_attribute_import(file, path, tool.AttributeImport, tool.AttributeImportResults, tool.AttributeImportSQL,
                                tool.Project)
    pass


def update_ifc_type_combobox():
    core.update_ifctype_combobox(tool.AttributeImportResults, tool.AttributeImportSQL, tool.Project)


def update_identifier_combobox():
    core.update_identifier_combobox(tool.AttributeImportResults, tool.AttributeImportSQL, tool.Project)


def update_object_count():
    core.update_object_count(tool.AttributeImportResults, tool.AttributeImportSQL)


def update_attribute_import_window():
    core.update_results_window(tool.AttributeImportResults)


def pset_table_selection_changed():
    core.update_attribute_table(tool.AttributeImportResults, tool.AttributeImportSQL)


def attribute_table_selection_changed():
    core.update_value_table(tool.AttributeImportResults, tool.AttributeImportSQL)


def value_checkstate_changed(check_box):
    core.value_checkstate_changed(check_box, tool.AttributeImportResults, tool.AttributeImportSQL)


def update_property_set_table():
    core.update_property_set_table(tool.AttributeImportResults, tool.AttributeImportSQL)


def update_all_checkbox():
    core.update_all_checkbox(tool.AttributeImportResults)


def update_attribute_table():
    core.update_attribute_table(tool.AttributeImportResults, tool.AttributeImportSQL)


def update_value_table():
    core.update_value_table(tool.AttributeImportResults, tool.AttributeImportSQL)


def all_checkbox_checkstate_changed():
    core.all_checkbox_checkstate_changed(tool.AttributeImportResults, tool.AttributeImportSQL)


def result_abort_clicked():
    core.results_abort_clicked(tool.AttributeImportResults)


def result_acccept_clicked():
    core.results_accept_clicked(tool.AttributeImportResults, tool.AttributeImportSQL, tool.Project)


def settings_clicked():
    core.settings_clicked(tool.AttributeImportResults, tool.AttributeImportSQL)
