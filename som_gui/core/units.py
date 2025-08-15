from __future__ import annotations
from PySide6.QtGui import QStandardItemModel
from typing import TYPE_CHECKING, Type
import logging
import os
if TYPE_CHECKING:
    from som_gui import tool
from ifcopenshell.util.unit import unit_names, prefixes

from som_gui.module.units import ui
from som_gui.resources.data import UNIT_PATH
from som_gui.module.units.constants import (
    ALLOWED_PREFIXES,
    ALLOWED_UNITS,
    UNITS_SECTION,
)

#### Settings Window


def fill_unit_settings(
    widget: ui.UnitSettings,
    units_tool: Type[tool.Units],
    appdata: Type[tool.Appdata],
    util: Type[tool.Util],
):
    units_tool.set_unit_settings_widget(widget)
    appdata_folder = appdata.get_appdata_folder()
    appdata_path  = os.path.join(appdata_folder,"units.json")
    if os.path.exists(appdata_path):
        unit_dict = units_tool.load_units(appdata_path)
    else:
        unit_dict = units_tool.load_units(UNIT_PATH)
    model = ui.SettingsItemModel(unit_dict)
    widget.ui.unit_tree.setModel(model)

def unit_settings_accepted(units_tool: Type[tool.Units], appdata: Type[tool.Appdata]):
    widget = units_tool.get_unit_settings_widget()
    if not widget:
        return
    unit_data = units_tool.get_unit_settings_widget().ui.unit_tree.model().data_dict
    appdata_folder = appdata.get_appdata_folder()
    appdata_path  = os.path.join(appdata_folder,"units.json")
    units_tool.update_units(unit_data,appdata_path)


def update_unit_combobox(
    cb: ui.UnitComboBox, units_tool: Type[tool.Units], appdata: Type[tool.Appdata]
):
    logging.debug(f"Update unit combobox")
    model: QStandardItemModel = cb.mod
    tree_view = cb.tree_view
    allowed_units = units_tool.get_allowed_units(appdata)
    allowed_prefixes = units_tool.get_allowed_unit_prefixes(appdata)
    for row in range(model.rowCount()):
        item = model.item(row)
        index = item.index()
        hide_item = item.text() not in allowed_units
        tree_view.setRowHidden(row, index.parent(), hide_item)

        for child_row in range(item.rowCount()):
            child_item = item.child(child_row)
            hide_item = child_item.text() not in allowed_prefixes
            tree_view.setRowHidden(child_row, index, hide_item)
