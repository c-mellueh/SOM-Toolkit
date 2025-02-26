from __future__ import annotations

import SOMcreator
from som_gui import tool
from som_gui.core import attribute as core
from typing import TYPE_CHECKING
from . import ui

def connect():
    core.add_basic_attribute_data(tool.Attribute)
    core.add_attribute_compare_widget(tool.AttributeCompare, tool.CompareWindow)
    tool.Settings.add_page_to_toolbox(ui.UnitSettings, "pageUnits",
                                      lambda: core.unit_settings_accepted(tool.Attribute, tool.Appdata))

def init_attribute_compare(project_0: SOMcreator.Project, project_1: SOMcreator.Project):
    core.create_compare_widget(project_0, project_1, tool.AttributeCompare)


def export_attribute_differences(file):
    core.export_attribute_differences(file, tool.AttributeCompare)


def object_tree_selection_changed(widget, ):
    core.activate_object_in_compare_tree(widget, tool.AttributeCompare)


def pset_tree_selection_changed(widget):
    core.pset_tree_selection_changed(widget, tool.AttributeCompare)


def retranslate_ui():
    pass


def on_new_project():
    pass

def repaint_unit_combobox(cb:ui.UnitComboBox):
    core.update_unit_combobox(cb,tool.Attribute,tool.Appdata)


def unit_settings_created(widget:ui.UnitSettings):
    core.fill_unit_settings(widget,tool.Attribute,tool.Appdata,tool.Util)
