from som_gui import tool
from som_gui.core import main_window as core

TOOGLE_CONSOLE_ACTION = "toggle_console"


def connect():
    core.init(tool.MainWindow, tool.ClassTree)
    core.add_class_tree_shortcuts(
        tool.ClassTree,
        tool.Util,
        tool.MainWindow,
        tool.ClassInfo,
    )
    core.connect_class_tree(tool.MainWindow, tool.ClassTree,tool.ClassInfo)
    core.define_class_tree_context_menu(tool.MainWindow,tool.ClassTree,tool.ClassInfo)

def on_new_project():
    core.one_new_project(tool.MainWindow,tool.ClassTree)


def retranslate_ui():
    core.retranslate_ui(tool.MainWindow, tool.ClassTree)


def toggle_console():
    core.toggle_console_clicked(tool.MainWindow,tool.ClassTree)


def close_event(event):
    return core.close_event(event, tool.MainWindow, tool.Popups)


def paint_event():
    core.refresh_main_window(tool.MainWindow, tool.Project)


def class_item_selection_changed():
    core.class_selection_changed(tool.MainWindow, tool.ClassTree, tool.PropertySet)
