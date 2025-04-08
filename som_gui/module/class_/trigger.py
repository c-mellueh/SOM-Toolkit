from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import class_ as core
from typing import TYPE_CHECKING
import SOMcreator

if TYPE_CHECKING:
    from .prop import ClassDataDict


def connect():
    core.init(tool.Class,tool.ClassInfo,tool.MainWindow)


def retranslate_ui():
    pass


def on_new_project():
    pass


def copy_class_called(som_class: SOMcreator.SOMClass, data_dict: ClassDataDict):
    core.copy_class(som_class, data_dict, tool.Class, tool.ClassInfo)


def modify_class_called(som_class: SOMcreator.SOMClass, data_dict: ClassDataDict):
    core.modify_class(
        som_class,
        data_dict,
        tool.Class,
        tool.ClassInfo,
        tool.PropertySet,
        tool.PredefinedPropertySet,
    )


def create_class_called(data_dict: ClassDataDict):
    core.create_class(
        data_dict,
        tool.Class,
        tool.ClassInfo,
        tool.Project,
        tool.PropertySet,
        tool.PredefinedPropertySet,
    )
