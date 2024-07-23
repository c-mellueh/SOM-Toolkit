from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import som_gui
from som_gui.module.mapping import ui, trigger

if TYPE_CHECKING:
    from som_gui.module.mapping.prop import MappingProperties

class Mapping(som_gui.core.tool.Mapping):
    @classmethod
    def get_properties(cls) -> MappingProperties:
        return som_gui.MappingProperties

    @classmethod
    def get_window(cls):
        if cls.get_properties().window is None:
            cls.get_properties().window = ui.MappingWindow()
        return cls.get_properties().window

    @classmethod
    def connect_window_triggers(cls, window: ui.MappingWindow) -> None:
        window.widget.action_ifc.triggered.connect(trigger.export_revit_ifc_mapping)
        window.widget.action_shared_parameters.triggered.connect(trigger.export_revit_shared_parameters)
