from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.class_info.prop import ClassDataDict
    from . import ui
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from som_gui import tool
from som_gui.core import class_ as core
import SOMcreator


def connect():
    widget: QTreeWidget = tool.Class.get_class_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, tool.Class))
    widget.itemSelectionChanged.connect(
        lambda: core.item_selection_changed(tool.Class, tool.PropertySet)
    )
    widget.customContextMenuRequested.connect(
        lambda p: core.create_context_menu(p, tool.Class)
    )
    widget.expanded.connect(lambda: core.resize_columns(tool.Class))

    # Connect MainWindow
    main_ui = tool.MainWindow.get_ui()
    main_ui.button_search.pressed.connect(
        lambda: core.search_class(tool.Search, tool.Class, tool.Project)
    )

    core.load_context_menus(tool.Class, tool.ClassInfo, tool.Util)
    core.add_shortcuts(
        tool.Class, tool.Util, tool.Search, tool.MainWindow, tool.Project
    )
    core.init_main_window(tool.Class, tool.ClassInfo, tool.MainWindow)


def repaint_event():
    core.refresh_class_tree(tool.Class, tool.Project)


def drop_event(event, target: ui.ClassTreeWidget):
    core.drop_event(event, target, tool.Class,tool.Project)


def on_new_project():
    core.reset_tree(tool.Class)


def retranslate_ui():
    core.retranslate_ui(tool.Class)


def create_class_called(data_dict: ClassDataDict):
    core.create_class(
        data_dict,
        tool.Class,
        tool.ClassInfo,
        tool.Project,
        tool.PropertySet,
        tool.PredefinedPropertySet,
    )


def copy_class_called(som_class: SOMcreator.SOMClass, data_dict: ClassDataDict):
    core.copy_class(som_class, data_dict, tool.Class, tool.ClassInfo)


def modify_class_called(som_class: SOMcreator.SOMClass, data_dict: ClassDataDict):
    core.modify_class(som_class, data_dict, tool.Class, tool.ClassInfo,tool.PropertySet,tool.PredefinedPropertySet)


def create_mime_data(items: list[QTreeWidgetItem], mime_data):
    return core.create_mime_data(items, mime_data, tool.Class)
