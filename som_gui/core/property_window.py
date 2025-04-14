from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_window import ui
import SOMcreator
from som_gui.module.property_.ui import UnitComboBox


def connect_signals(
    property_window: Type[tool.PropertyWindow], property_table: Type[tool.PropertyTable]
):
    property_table.signaller.property_info_requested.connect(
        property_window.property_info_requested
    )


def init_window(window: ui.PropertyWindow, property_window: Type[tool.PropertyWindow]):
    property_window.prefill_comboboxes(window)
    property_window.update_unit_completer(window)

def connect_window(
    window: ui.PropertyWindow, property_window: Type[tool.PropertyWindow]
):
    som_property = property_window.get_property_from_window(window)
    ui = window.ui
    ui.lineEdit_name.textEdited.connect(
        lambda t: property_window.rename_property(som_property, t)
    )


def update_window(
    window: ui.PropertyWindow,
    property_window: Type[tool.PropertyWindow],
    util: Type[tool.Util],
):
    som_property = property_window.get_property_from_window(window)
    ui = window.ui
    ui.lineEdit_name.setText(som_property.name)
    ui.combo_data_type.setCurrentText(som_property.data_type)
    ui.combo_value_type.setCurrentText(som_property.value_type)
    ui.combo_unit.setCurrentText(som_property.unit or "")
    ui.description.setText(som_property.description)
    property_window.set_comboboxes_enabled(som_property.is_child, window)
    inherits_values_checkstate = util.bool_to_checkstate(
        som_property.child_inherits_values
    )
    ui.check_box_inherit.setCheckState(inherits_values_checkstate)


def open_property_info(
    som_property: SOMcreator.SOMProperty, property_window: Type[tool.PropertyWindow]
):
    if not (window := property_window.get_window(som_property)):
        window = property_window.create_window(som_property)
    window.show()
    window.activateWindow()
