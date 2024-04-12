from __future__ import annotations
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui import tool


def open_window(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter]):
    if attribute_import.is_window_allready_build():
        attribute_import.get_attribute_widget().show()
        return

    window = attribute_import.create_window()
    attribute_import_widget = attribute_import.create_import_widget()
    ifc_import_widget = ifc_importer.create_importer()
    window.layout().addWidget(ifc_import_widget)
    window.layout().addWidget(attribute_import_widget)
    attribute_import_widget.hide()


    attribute_import.set_ifc_importer_widget(ifc_import_widget)
    attribute_import.connect_buttons(attribute_import.get_buttons())
    window.show()
    print(attribute_import_widget)


def run_clicked():
    pass


def accept_clicked():
    pass


def abort_clicked():
    pass


def close_clicked():
    pass


def paint_property_set_table():
    pass


def paint_attribute_table():
    pass


def paint_value_table():
    pass
