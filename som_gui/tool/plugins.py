from __future__ import annotations
from typing import TYPE_CHECKING, Any
import logging

import som_gui.core.tool
import som_gui
import importlib
import pkgutil
from som_gui import tool
from som_gui.module.plugins import constants
if TYPE_CHECKING:
    from som_gui.module.plugins.prop import PluginsProperties


class Plugins(som_gui.core.tool.Plugins):
    @classmethod
    def get_properties(cls) -> PluginsProperties:
        return som_gui.PluginsProperties

    @classmethod
    def get_available_plugins(cls) -> list[str]:
        module = importlib.import_module("som_gui.plugins")
        modules = [m.name for m in pkgutil.iter_modules(module.__path__) if m.ispkg]
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
