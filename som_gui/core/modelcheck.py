from __future__ import annotations
from typing import TYPE_CHECKING, Type
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from som_gui import tool


def open_window(modelcheck: Type[tool.Modelcheck], ifc_importer: Type[tool.IfcImporter]):
    window = modelcheck.create_window()
    check_box_widget = modelcheck.create_checkbox_widget()
    ifc_import_widget = ifc_importer.create_importer()

    modelcheck.add_splitter(window.vertical_layout, Qt.Orientation.Vertical, check_box_widget, ifc_import_widget)
    modelcheck.connect_window(window)
    window.setWindowTitle("Modellprüfung")
    window.show()
