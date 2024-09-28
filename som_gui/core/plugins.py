from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Type
from PySide6.QtWidgets import QFormLayout, QCheckBox

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.plugins import ui


def settings_accepted(plugins: Type[tool.Plugins], popups: Type[tool.Popups]):
    layout: QFormLayout = plugins.get_settings_widget().layout()
    for index, plugin_name in enumerate(plugins.get_available_plugins()):
        cb: QCheckBox = layout.itemAt(index, QFormLayout.ItemRole.FieldRole).widget()
        new_checkstate = cb.isChecked()
        old_checkstate = plugins.is_plugin_active(plugin_name)
        friendly_name = plugins.get_friendly_name(plugin_name)
        if new_checkstate == old_checkstate:
            continue
        plugins.set_plugin_active(plugin_name, new_checkstate)
        state = "activated" if new_checkstate else "deactivated"
        info_text = f"The plugin '{friendly_name}' has been successfully {state}. \nPlease restart the program for the changes to take effect."
        popups.create_info_popup(info_text, f"Plugin {state.title()}: Restart Required")


def settings_widget_created(widget: ui.SettingsWidget, plugins: Type[tool.Plugins]):
    layout: QFormLayout = widget.layout()
    plugins.set_settings_widget(widget)
    for plugin_name in plugins.get_available_plugins():
        label, checkbox = plugins.create_settings_entry(plugin_name)
        layout.addRow(label, checkbox)
