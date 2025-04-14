from __future__ import annotations

from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from som_gui import tool

import SOMcreator

def connect_signals(property_window:Type[tool.PropertyWindow],property_table:Type[tool.PropertyTable]):
    property_table.signaller.property_info_requested.connect(property_window.property_info_requested)

def open_property_info(som_property:SOMcreator.SOMProperty,property_window:Type[tool.PropertyWindow]):
    print(som_property)