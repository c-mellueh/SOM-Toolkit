from __future__ import annotations
from som_gui.core import attribute as core
from som_gui import tool


def connect():
    core.add_basic_attribute_data(tool.Attribute)


def on_new_project():
    pass
