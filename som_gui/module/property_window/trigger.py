from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import property_window as core
from typing import TYPE_CHECKING
import SOMcreator

def connect():
    core.connect_signals(tool.PropertyWindow,tool.PropertyTable)

def retranslate_ui():
    pass

def on_new_project():
    pass

def property_info_requested(som_property:SOMcreator.SOMProperty):
    core.open_property_info(som_property,tool.PropertyWindow)
