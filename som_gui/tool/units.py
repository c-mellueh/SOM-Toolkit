from __future__ import annotations
from typing import TYPE_CHECKING, Type
import logging
from som_gui import tool
from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import Qt
import som_gui.core.tool
import som_gui
from som_gui.module.units import constants

if TYPE_CHECKING:
    from som_gui.module.units.prop import UnitsProperties
    from som_gui.module.units import ui
from ifcopenshell.util.unit import unit_names, prefixes


class Units(som_gui.core.tool.Units):
    @classmethod
    def get_properties(cls) -> UnitsProperties:
        return som_gui.UnitsProperties

    @classmethod
    def set_unit_settings_widget(cls, widget: ui.UnitSettings):
        cls.get_properties().unit_settings_widget = widget

    @classmethod
    def get_unit_settings_widget(
        cls,
    ) -> ui.UnitSettings | None:
        return cls.get_properties().unit_settings_widget

    @classmethod
    def get_allowed_units(cls, appdata: Type[tool.Appdata]):
        """
        Search Appdata for allowed units. If no allowed units are saved, return all existing units.

        :param appdata: The application data instance to retrieve settings from.
        :type appdata: Type[tool.Appdata]
        :return: A list of allowed units.
        :rtype: list[str]
        """
        all_units = [un.capitalize() for un in unit_names]
        allowed_units = appdata.get_list_setting(
            constants.UNITS_SECTION, constants.ALLOWED_UNITS, None
        )
        if allowed_units is None:
            allowed_units = list(all_units)
        return allowed_units

    @classmethod
    def get_allowed_unit_prefixes(cls, appdata: Type[tool.Appdata]):
        """
        Retrieve the list of allowed unit prefixes from the application data.
        :param appdata: The application data instance to retrieve settings from.
        :type appdata: Type[tool.Appdata]
        :return: A list of allowed unit prefixes.
        :rtype: list[str]
        """
        all_prefixes = [pf.capitalize() for pf in prefixes.keys()]
        allowed_prefixes = appdata.get_list_setting(
            constants.UNITS_SECTION, constants.ALLOWED_PREFIXES, None
        )
        if allowed_prefixes is None:
            allowed_prefixes = list(all_prefixes)
        return allowed_prefixes

    @classmethod
    def get_checked_texts_from_list_widget(cls, list_widget: QListWidget) -> list[str]:
        items = [list_widget.item(i) for i in range(list_widget.count())]
        return [i.text() for i in items if i.checkState() == Qt.CheckState.Checked]
