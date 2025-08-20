from __future__ import annotations
from typing import TYPE_CHECKING, Type
import logging
from som_gui import tool
from PySide6.QtWidgets import QListWidget,QTreeView
from PySide6.QtCore import Qt
import som_gui.core.tool
import som_gui
import os
from som_gui.module.units import constants
from som_gui.resources.data import UNIT_PATH
if TYPE_CHECKING:
    from som_gui.module.units.prop import UnitsProperties
    from som_gui.module.units import ui
from ifcopenshell.util.unit import unit_names, prefixes
import json

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
    def load_units(cls,path):
        prop = cls.get_properties()
        with open(path, "r") as f:
            data = json.load(f)
        prop.unit_dict = data 
        return prop.unit_dict
    
    @classmethod
    def update_units(cls,data_dict,path):
        def remove_parent_key(d):
            for element in d:
                for un in element["units"]:
                    if "parent" in un: 
                        un.pop("parent")
                if "parent" in element:
                    element.pop("parent")
                element["children"] = remove_parent_key(element["children"] )
            return d

        data_dict = remove_parent_key(data_dict)
        with open(path,"w") as file:
            json.dump(data_dict,file)
        cls.get_properties().unit_dict = data_dict
    
    @classmethod
    def get_units_dict(cls):
        from som_gui import tool
        if cls.get_properties().unit_dict:
            return cls.get_properties().unit_dict
    
        appdata_folder = tool.Appdata.get_appdata_folder()
        appdata_path  = os.path.join(appdata_folder,"units.json")
        if os.path.exists(appdata_path):
            try:
                unit_dict = cls.load_units(appdata_path)
            except:
                unit_dict = cls.load_units(UNIT_PATH)
        else:
            unit_dict = cls.load_units(UNIT_PATH)
        return unit_dict
    
    @classmethod
    def uri_to_code(cls,uri):
        from SOMcreator.templates import UNITS_DICT
        element =  UNITS_DICT.get(uri)
        if not element:
            return ""
        return element.get("Code","")