from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import units as core
from typing import TYPE_CHECKING

from . import ui


def connect():
    tool.Settings.add_page_to_toolbox(
        ui.UnitSettings,
        "pageUnits",
        lambda: core.unit_settings_accepted(tool.Units, tool.Appdata),
    )


def retranslate_ui():
    pass


def on_new_project():
    pass


def repaint_unit_combobox(cb: ui.UnitComboBox):
    core.update_unit_combobox(cb, tool.Units, tool.Appdata)


def unit_settings_created(widget: ui.UnitSettings):
    core.fill_unit_settings(widget, tool.Units, tool.Appdata, tool.Util)

def update_current_unit(widget,data_dict):
    core.update_current_unit(widget,data_dict,tool.Units,tool.PropertyWindow)