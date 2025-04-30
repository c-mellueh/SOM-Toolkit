from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import ifc_schema as core
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import MappingWidget

def connect():
    core.init(tool.IfcSchema,tool.Appdata)

def mapping_widget_created(widget:MappingWidget):
    core.setup_mapping_widget(widget,tool.IfcSchema)

def append_ifc_mapping(widget:MappingWidget,value:str):
    core.append_ifc_mapping(widget,value,tool.IfcSchema)
def retranslate_ui():
    pass

def on_new_project():
    pass
