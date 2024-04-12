from PySide6.QtWidgets import QPushButton
import ifcopenshell
from som_gui import tool
from som_gui.core import attribute_import as core


def connect():
    tool.MainWindow.add_action("Modelle/Modellinformationen Einlesen21",
                               lambda: core.open_window(tool.AttributeImport, tool.IfcImporter))


def connect_buttons(run_button: QPushButton, abort_button: QPushButton, accept_button: QPushButton,
                    close_button: QPushButton):
    run_button.clicked.connect(lambda: core.run_clicked(tool.AttributeImport, tool.IfcImporter))
    accept_button.clicked.connect(lambda: core.accept_clicked())
    abort_button.clicked.connect(lambda: core.abort_clicked())
    close_button.clicked.connect(lambda: core.close_clicked())


def connect_ifc_import_runner(runner):
    runner.signaller.started.connect(lambda: core.ifc_import_started(runner, tool.AttributeImport, tool.IfcImporter))
    runner.signaller.finished.connect(lambda: core.ifc_import_finished(runner, tool.AttributeImport, tool.IfcImporter))


def connect_attribute_import_runner(runner):
    runner.signaller.finished.connect(
        lambda: core.attribute_import_finished(tool.AttributeImport, tool.IfcImporter))
    runner.signaller.status.connect(tool.ModelcheckWindow.set_status)
    runner.signaller.progress.connect(tool.ModelcheckWindow.set_progress)

def paint_property_set_table():
    core.paint_property_set_table()


def paint_attribute_table():
    core.paint_attribute_table()


def paint_value_table():
    core.paint_value_table()


def on_new_project():
    pass


def last_import_finished():
    core.last_import_finished(tool.AttributeImport)


def start_attribute_import(file: ifcopenshell.file):
    core.start_attribute_import(file, tool.AttributeImport)
    pass
