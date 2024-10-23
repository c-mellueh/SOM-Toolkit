from __future__ import annotations

import SOMcreator
from som_gui.core import attribute as core
from som_gui import tool


def connect():
    core.add_basic_attribute_data(tool.Attribute)
    core.add_attribute_compare_widget(tool.AttributeCompare, tool.CompareWindow)

def init_attribute_compare(project_0:SOMcreator.Project,project_1:SOMcreator.Project):
    core.init_attribute_compare(project_0,project_1,tool.AttributeCompare)


def export_attribute_differences(file):
    core.export_attribute_differences(file,tool.AttributeCompare)

def object_tree_selection_changed(widget, ):
    core.object_tree_selection_changed(widget, tool.AttributeCompare)


def pset_tree_selection_changed(widget):
    core.pset_tree_selection_changed(widget, tool.AttributeCompare)

def retranslate_ui():
    pass

def on_new_project():
    pass
