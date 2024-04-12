from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import som_gui
from som_gui.module.attribute_import import ui

if TYPE_CHECKING:
    from som_gui.module.attribute_import.prop import AttributeImportProperties
    from som_gui.module.ifc_importer.ui import IfcImportWidget
class AttributeImport(som_gui.core.tool.AttributeImport):
    @classmethod
    def get_properties(cls) -> AttributeImportProperties:
        return som_gui.AttributeImportProperties

    @classmethod
    def is_window_allready_build(cls) -> bool:
        return cls.get_window() is not None

    @classmethod
    def get_window(cls) -> ui.AttributeImport:
        return cls.get_properties().active_window

    @classmethod
    def create_window(cls) -> ui.AttributeImport:
        prop = cls.get_properties()
        prop.active_window = ui.AttributeImport()
        return prop.active_window

    @classmethod
    def set_ifc_importer_widget(cls, widget: IfcImportWidget):
        window = cls.get_window()
        window.widget.main_layout.insertWidget(0, widget)
