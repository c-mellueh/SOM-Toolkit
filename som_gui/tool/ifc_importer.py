from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui
import som_gui.core.tool
from som_gui.module.ifc_importer import ui

if TYPE_CHECKING:
    from som_gui.module.ifc_importer.prop import IfcImportProperties


class IfcImporter(som_gui.core.tool.IfcImporter):
    @classmethod
    def get_properties(cls) -> IfcImportProperties:
        return som_gui.IfcImportProperties

    @classmethod
    def create_importer(cls):
        widget = ui.IfcImportWidget()
        cls.get_properties().active_importer = widget
        return widget
