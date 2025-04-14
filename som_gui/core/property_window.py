from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_window import ui
import SOMcreator

def connect_signals(property_window:Type[tool.PropertyWindow],property_table:Type[tool.PropertyTable]):
    property_table.signaller.property_info_requested.connect(property_window.property_info_requested)

def connect_window(window:ui.PropertyWindow,property_window:Type[tool.PropertyWindow]):
    som_property = property_window.get_property_from_window(window)
    ui = window.ui
    ui.lineEdit_name.textEdited.connect(lambda t:property_window.rename_property(som_property,t))

def update_window(window:ui.PropertyWindow,property_window:Type[tool.PropertyWindow]):
    som_property = property_window.get_property_from_window(window)
    ui = window.ui
    ui.lineEdit_name.setText(som_property.name)


def open_property_info(som_property:SOMcreator.SOMProperty,property_window:Type[tool.PropertyWindow]):
    if not (window:=property_window.get_window(som_property)):
        window  = property_window.create_window(som_property)
    window.show()
    window.activateWindow()