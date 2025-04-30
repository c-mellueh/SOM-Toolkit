from __future__ import annotations

from typing import TYPE_CHECKING, Type
from som_gui.module.ifc_schema.constants import (
    APPDATA_SECTION,
    VERSION_OPTION,
    IFC2X3,
    IFC4,
    IFC4_3,

    PREDEFINED_SPLITTER,
)

from PySide6.QtGui import QStandardItem

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.ifc_schema import ui


def init(ifc_schema: Type[tool.IfcSchema], appdata: Type[tool.Appdata]):
    versions = appdata.get_list_setting(APPDATA_SECTION, VERSION_OPTION, [IFC2X3,IFC4,IFC4_3])
    ifc_schema.set_active_versions(versions)
    for version in versions:
        ifc_schema.read_jsons(version)


def setup_mapping_widget(widget: ui.MappingWidget, ifc_schema: Type[tool.IfcSchema]):
    widget.ui.table_view.setFrameStyle


def append_ifc_mapping(
    widget: ui.MappingWidget, text: str, ifc_schema: Type[tool.IfcSchema]
):
    table = widget.ui.table_view
    row = table.model().rowCount()
    table.model().insertRow(row)

    enitity_text, predef_text = (
        text.split(PREDEFINED_SPLITTER) if PREDEFINED_SPLITTER in text else (text, "")
    )
    table.model().setItem(row, 0, QStandardItem(enitity_text))
    table.model().setItem(row, 1, QStandardItem(predef_text))
