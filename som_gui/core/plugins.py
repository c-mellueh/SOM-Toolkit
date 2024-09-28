from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.plugins import ui


def settings_accepted(plugins: Type[tool.Plugins], appdata: Type[tool.Appdata]):
    pass


def settings_widget_created(widget: ui.SettingsWidget, plugins: Type[tool.Plugins], appdata: Type[tool.Appdata]):
    for plugin_name in plugins.get_available_plugins():
        if not plugins.is_plugin_active(plugin_name):
            logging.info(f"skipping plugin {plugin_name}")
            continue
        plugins.import_plugin(plugin_name)
