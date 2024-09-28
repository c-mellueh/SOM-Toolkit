from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.plugins import ui


def settings_accepted(plugins: Type[tool.Settings], appdata: Type[tool.Appdata]):
    pass


def settings_widget_created(widget: ui.SettingsWidget, plugins: Type[tool.Settings], appdata: Type[tool.Appdata]):
    pass
