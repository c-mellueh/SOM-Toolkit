from PySide6.QtWidgets import QPushButton
import ifcopenshell
from som_gui import tool
from som_gui.core import attribute_import as core


def connect():
    tool.MainWindow.add_action("Modelle/Modellinformationen Einlesen21",
                               lambda: core.open_import_window(tool.AttributeImport, tool.AttributeImportSQL,
                                                               tool.IfcImporter))


def connect_import_buttons(run_button: QPushButton, abort_button: QPushButton):
    run_button.clicked.connect(
        lambda: core.run_clicked(tool.AttributeImport, tool.IfcImporter, tool.AttributeImportSQL, tool.Project,
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

def paint_property_set_table():
    core.paint_property_set_table(tool.AttributeImport, tool.AttributeImportSQL)


def paint_attribute_table():
    core.paint_attribute_table(tool.AttributeImport, tool.AttributeImportSQL)


def paint_value_table():
    core.paint_value_table(tool.AttributeImport, tool.AttributeImportSQL)


def on_new_project():
    pass


def last_import_finished():
    core.last_import_finished(tool.AttributeImport)


def start_attribute_import(file: ifcopenshell.file, path: str):
    core.start_attribute_import(file, path, tool.AttributeImport, tool.AttributeImportSQL)
    pass


def somtype_combobox_paint_event():
    core.update_somtype_combobox(tool.AttributeImport, tool.AttributeImportSQL, tool.Project)


def ifctype_combobox_paint_event():
    core.update_ifctype_combobox(tool.AttributeImport, tool.AttributeImportSQL, tool.Project)


def update_attribute_import_window():
    core.update_results_window(tool.AttributeImport, tool.AttributeImportSQL)


def pset_table_selection_changed():
    core.update_results_window(tool.AttributeImport, tool.AttributeImportSQL)


def attribute_table_selection_changed():
    core.update_results_window(tool.AttributeImport, tool.AttributeImportSQL)


def value_table_selection_changed():
    core.update_results_window(tool.AttributeImport, tool.AttributeImportSQL)
