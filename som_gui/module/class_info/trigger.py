from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import SOMcreator
    from PySide6.QtWidgets import QTreeWidgetItem
from som_gui import tool
from som_gui.core import class_info as core


def on_new_project():
    pass


def connect():
    core.init(tool.ClassInfo,tool.MainWindow)

def class_info_paint_event():
    core.class_info_refresh(tool.Class, tool.ClassInfo)
    pass


def retranslate_ui():
    core.retranslate_ui(tool.ClassInfo)


def create_class_info_widget(mode: int,som_class:SOMcreator.SOMClass|None):
    core.create_class_info_widget(
        mode,som_class, tool.Class, tool.ClassInfo, tool.PredefinedPropertySet, tool.Util
    )
