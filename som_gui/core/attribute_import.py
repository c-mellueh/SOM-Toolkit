from __future__ import annotations
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui import tool


def open_window(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter]):
    if attribute_import.is_window_allready_build():
        attribute_import.get_window().show()
        return

    window = attribute_import.create_window()
    ifc_import_widget = ifc_importer.create_importer()
    attribute_import.set_ifc_importer_widget(ifc_import_widget)
    ifc_importer.hide_buttons(ifc_import_widget)
    # check_box_widget = modelcheck_window.create_checkbox_widget()
    # ifc_import_widget = ifc_importer.create_importer()
    # modelcheck_window.create_export_line(ifc_import_widget)
    # modelcheck_window.set_importer_widget(ifc_import_widget)
    # modelcheck_window.add_splitter(window.vertical_layout, Qt.Orientation.Vertical, check_box_widget, ifc_import_widget)
    # modelcheck_window.connect_buttons(modelcheck_window.get_buttons())
    # modelcheck_window.connect_check_widget(check_box_widget)
    window.show()
