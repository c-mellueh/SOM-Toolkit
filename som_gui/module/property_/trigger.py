from __future__ import annotations

import SOMcreator
from som_gui import tool
from som_gui.core import property_ as core
from typing import TYPE_CHECKING
from . import ui


def connect():
    core.add_basic_property_data(tool.Property)
    core.add_compare_widget(tool.PropertyCompare, tool.CompareWindow)
    tool.Settings.add_page_to_toolbox(
        ui.UnitSettings,
        "pageUnits",
        lambda: core.unit_settings_accepted(tool.Property, tool.Appdata),
    )
    core.connect_signals(tool.Property)

def create_empty_property(property_set:SOMcreator.SOMPropertySet):
    core.create_empty_property(property_set,tool.Property,tool.Util,tool.Project)

def init_property_compare(
    project_0: SOMcreator.SOMProject, project_1: SOMcreator.SOMProject
):
    core.create_compare_widget(project_0, project_1, tool.PropertyCompare)


def export_property_differences(file):
    core.export_differences(file, tool.PropertyCompare)


def class_tree_selection_changed(
    widget,
):
    core.activate_class_in_compare_tree(widget, tool.PropertyCompare)


def pset_tree_selection_changed(widget):
    core.pset_tree_selection_changed(widget, tool.PropertyCompare)


def retranslate_ui():
    pass


def on_new_project():
    pass


def repaint_unit_combobox(cb: ui.UnitComboBox):
    core.update_unit_combobox(cb, tool.Property, tool.Appdata)


def unit_settings_created(widget: ui.UnitSettings):
    core.fill_unit_settings(widget, tool.Property, tool.Appdata, tool.Util)
