from __future__ import annotations

from typing import TYPE_CHECKING, Type
from som_gui.module.ifc_schema.constants import APPDATA_SECTION,VERSION_OPTION,IFC4_3
if TYPE_CHECKING:
    from som_gui import tool

def init(ifc_schema:Type[tool.IfcSchema],appdata:Type[tool.Appdata]):
    versions = appdata.get_list_setting(APPDATA_SECTION,VERSION_OPTION,[IFC4_3])
    ifc_schema.set_active_versions(versions)
    for version in versions:
        ifc_schema.read_jsons(version)
    