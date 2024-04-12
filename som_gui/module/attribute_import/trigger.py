from PySide6.QtWidgets import QPushButton

from som_gui import tool
from som_gui.core import attribute_import as core


def connect():
    tool.MainWindow.add_action("Modelle/Modellinformationen Einlesen21",
                               lambda: core.open_window(tool.AttributeImport, tool.IfcImporter))


def connect_buttons(run_button: QPushButton, abort_button: QPushButton, accept_button: QPushButton,
                    close_button: QPushButton):
    run_button.clicked.connect(lambda: core.run_clicked())
    accept_button.clicked.connect(lambda: core.accept_clicked())
    abort_button.clicked.connect(lambda: core.abort_clicked())
    close_button.clicked.connect(lambda: core.close_clicked())


def paint_property_set_table():
    core.paint_property_set_table()


def paint_attribute_table():
    core.paint_attribute_table()


def paint_value_table():
    core.paint_value_table()


def on_new_project():
    pass
