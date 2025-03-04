from PySide6.QtWidgets import QTreeWidget

from som_gui import tool
from som_gui.core import class_ as core


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


    core.load_context_menus(tool.Class, tool.Util)
    core.add_shortcuts(
        tool.Class, tool.Util, tool.Search, tool.MainWindow, tool.Project
    )
    core.init_main_window(tool.Class, tool.MainWindow)


def repaint_event():
    core.refresh_class_tree(tool.Class, tool.Project)


def drop_event(event):
    core.item_dropped_on(event.pos(), tool.Class)


def on_new_project():
    core.reset_tree(tool.Class)


def retranslate_ui():
    core.retranslate_ui(tool.Class)


def create_object_called():
    core.create_class(
        tool.Class,
        tool.Project,
        tool.PropertySet,
        tool.PredefinedPropertySet,
        tool.Popups,
        tool.Util,
    )


def copy_object_called():
    core.copy_class(tool.Class)


def modify_object_called():
    core.modify_class(tool.Class)
