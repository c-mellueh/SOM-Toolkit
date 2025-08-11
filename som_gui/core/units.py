from __future__ import annotations
from PySide6.QtGui import QStandardItemModel
from typing import TYPE_CHECKING, Type
import logging

if TYPE_CHECKING:
    from som_gui import tool
from ifcopenshell.util.unit import unit_names, prefixes

from som_gui.module.units import ui
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
    units_tool.import_units()

    all_units = [un.capitalize() for un in unit_names]
    allowed_units = units_tool.get_allowed_units(appdata)
    util.fill_list_widget_with_checkstate(
        widget.ui.list_units, allowed_units, all_units
    )

    all_prefixes = [pf.capitalize() for pf in prefixes.keys()]
    allowed_prefixes = units_tool.get_allowed_unit_prefixes(appdata)

    util.fill_list_widget_with_checkstate(
        widget.ui.list_prefixes, allowed_prefixes, all_prefixes
    )


def unit_settings_accepted(units_tool: Type[tool.Units], appdata: Type[tool.Appdata]):
    widget = units_tool.get_unit_settings_widget()
    if not widget:
        return
    allowed_units = units_tool.get_checked_texts_from_list_widget(widget.ui.list_units)
    appdata.set_setting(UNITS_SECTION, ALLOWED_UNITS, allowed_units)

    allowed_prefixes = units_tool.get_checked_texts_from_list_widget(
        widget.ui.list_prefixes
    )
    appdata.set_setting(UNITS_SECTION, ALLOWED_PREFIXES, allowed_prefixes)


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
