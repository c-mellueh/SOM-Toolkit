from __future__ import annotations
from typing import TYPE_CHECKING, Type
from som_gui import tool
from .. import tool as aw_tool


def open_window(grouping_window: Type[aw_tool.GroupingWindow], ifc_importer: Type[tool.IfcImporter]):
    window = modelcheck_window.create_window()
    check_box_widget = modelcheck_window.create_checkbox_widget()
    ifc_import_widget = ifc_importer.create_importer()
    modelcheck_window.create_export_line(ifc_import_widget)
    modelcheck_window.set_importer_widget(ifc_import_widget)
    modelcheck_window.add_splitter(window.vertical_layout, Qt.Orientation.Vertical, check_box_widget, ifc_import_widget)
    modelcheck_window.connect_buttons(modelcheck_window.get_buttons())
    modelcheck_window.connect_check_widget(check_box_widget)
    window.show()
