from som_gui import tool
from som_gui.core import main_window as core
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QDropEvent

TOOGLE_CONSOLE_ACTION = "toggle_console"
import SOMcreator


def connect():
    core.init(
        tool.MainWindow,
        tool.ClassTree,
        tool.ClassInfo,
        tool.Class,
        tool.Property,
        tool.PropertyTable,
        tool.PropertyWindow,
    )
    core.add_class_tree_columns(tool.MainWindow, tool.ClassTree)
    core.add_class_tree_shortcuts(
        tool.ClassTree,
        tool.Util,
        tool.MainWindow,
        tool.ClassInfo,
    )
    core.define_class_tree_context_menu(tool.MainWindow, tool.ClassTree, tool.ClassInfo)


def on_new_project():
    core.one_new_project(tool.MainWindow, tool.ClassTree)


def retranslate_ui():
    core.retranslate_ui(tool.MainWindow, tool.ClassTree)


def toggle_console():
    core.toggle_console_clicked(tool.MainWindow, tool.ClassTree)


def close_event(event):
    return core.close_event(event, tool.MainWindow, tool.Popups)


def paint_event():
    core.refresh_main_window(tool.MainWindow, tool.Project)


def change_active_class(som_class: SOMcreator.SOMClass):
    core.set_active_class(som_class, tool.MainWindow, tool.PropertySet)


def class_tree_item_dropped(event: QDropEvent):
    core.drop_on_class_tree(event, tool.MainWindow, tool.ClassTree, tool.Project)
