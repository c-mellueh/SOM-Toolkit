from __future__ import annotations
from typing import TYPE_CHECKING, Any
import logging
from PySide6.QtWidgets import QFormLayout, QLabel, QCheckBox
import som_gui.core.tool
import som_gui
import importlib
import pkgutil
from som_gui import tool
from som_gui.module.plugins import constants
if TYPE_CHECKING:
    from som_gui.module.plugins.prop import PluginsProperties
    from som_gui.module.plugins import ui

class Plugins(som_gui.core.tool.Plugins):

    @classmethod
    def get_properties(cls) -> PluginsProperties:
        return som_gui.PluginsProperties

    @classmethod
    def get_settings_widget(cls) -> ui.SettingsWidget:
        return cls.get_properties().settings_widget

    @classmethod
    def set_settings_widget(cls, widget: ui.SettingsWidget):
        cls.get_properties().settings_widget = widget

    @classmethod
    def get_available_plugins(cls) -> list[str]:
        module = importlib.import_module("som_gui.plugins")
        modules = sorted(m.name for m in pkgutil.iter_modules(module.__path__) if m.ispkg)
        return modules

    @classmethod
    def import_plugin(cls, plugin_name: str) -> list[tuple[str, Any]]:
        module_text = f"som_gui.plugins.{plugin_name}.module"
        submodule_names = [m.name for m in pkgutil.iter_modules(importlib.import_module(module_text).__path__) if
                           m.ispkg]
        submodules = [importlib.import_module(f"{module_text}.{n}") for n in submodule_names]
        return list(zip(submodule_names, submodules))

    @classmethod
    def is_plugin_active(cls, plugin_name: str) -> bool:
        return tool.Appdata.get_bool_setting(constants.PLUGINS, plugin_name)

    @classmethod
    def set_plugin_active(cls, plugin_name: str, state: bool) -> None:
        tool.Appdata.set_setting(constants.PLUGINS, plugin_name, state)

    @classmethod
    def get_friendly_name(cls, name: str):
        module = importlib.import_module(f"som_gui.plugins.{name}")
        if not "friendly_name" in dir(module):
            return name
        return getattr(module, "friendly_name")

    @classmethod
    def get_description(cls, name: str):
        module = importlib.import_module(f"som_gui.plugins.{name}")
        if not "description" in dir(module):
            return ""
        return getattr(module, "description")

    @classmethod
    def create_settings_entry(cls, plugin_name: str) -> tuple[QLabel, QCheckBox]:
        cb = QCheckBox()
        cb.setChecked(cls.is_plugin_active(plugin_name))

        friendly_name = cls.get_friendly_name(plugin_name)
        label = QLabel(friendly_name)
        label.setToolTip(cls.get_description(plugin_name))
        return label, cb
