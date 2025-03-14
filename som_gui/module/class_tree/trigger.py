from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.class_info.prop import ClassDataDict
    from . import ui
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from som_gui import tool
from som_gui.core import class_tree as core
import SOMcreator


def connect():
    widget: QTreeWidget = tool.ClassTree.get_class_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, tool.ClassTree))
    widget.itemSelectionChanged.connect(
        lambda: core.item_selection_changed(tool.ClassTree, tool.PropertySet)
    )
    widget.customContextMenuRequested.connect(
        lambda p: core.create_context_menu(p, tool.ClassTree)
    )
    widget.expanded.connect(lambda: core.resize_columns(tool.ClassTree))

    # Connect MainWindow
    main_ui = tool.MainWindow.get_ui()
    main_ui.button_search.pressed.connect(
        lambda: core.search_class(tool.Search, tool.ClassTree, tool.Project)
    )

    core.load_context_menus(tool.ClassTree, tool.ClassInfo, tool.Project)
    core.add_shortcuts(
        tool.ClassTree,
        tool.Util,
        tool.Search,
        tool.MainWindow,
        tool.Project,
        tool.ClassInfo,
    )
    core.init_main_window(tool.ClassTree, tool.ClassInfo, tool.MainWindow)


def repaint_event():
    core.refresh_class_tree(tool.ClassTree, tool.Project)


def drop_event(event, target: ui.ClassTreeWidget):
    core.drop_event(event, target, tool.ClassTree, tool.Project)


def on_new_project():
    core.reset_tree(tool.ClassTree)


def retranslate_ui():
    core.retranslate_ui(tool.ClassTree)


def create_class_called(data_dict: ClassDataDict):
    core.create_class(
        data_dict,
        tool.ClassTree,
        tool.ClassInfo,
        tool.Project,
        tool.PropertySet,
        tool.PredefinedPropertySet,
    )


def copy_class_called(som_class: SOMcreator.SOMClass, data_dict: ClassDataDict):
    core.copy_class(som_class, data_dict, tool.ClassTree, tool.ClassInfo)


def modify_class_called(som_class: SOMcreator.SOMClass, data_dict: ClassDataDict):
    core.modify_class(
        som_class,
        data_dict,
        tool.ClassTree,
        tool.ClassInfo,
        tool.PropertySet,
        tool.PredefinedPropertySet,
    )


def create_mime_data(items: list[QTreeWidgetItem], mime_data):
    return core.create_mime_data(items, mime_data, tool.ClassTree)


def group_selection():
    core.create_group(tool.ClassTree, tool.Project)
