from PySide6.QtWidgets import QTreeWidget

from som_gui import tool
from som_gui.core import class_ as core


def connect():
    widget: QTreeWidget = tool.Class.get_class_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, tool.Class))
    widget.itemSelectionChanged.connect(
        lambda: core.item_selection_changed(tool.Class, tool.PropertySet)
    )
    widget.itemDoubleClicked.connect(item_double_clicked)
    widget.customContextMenuRequested.connect(
        lambda p: core.create_context_menu(p, tool.Class)
    )
    widget.expanded.connect(lambda: core.resize_columns(tool.Class))

    # Connect MainWindow
    main_ui = tool.MainWindow.get_ui()
    main_ui.button_search.pressed.connect(
        lambda: core.search_object(tool.Search, tool.Class, tool.Project)
    )
    main_ui.button_objects_add.clicked.connect(
        lambda: core.create_object_info_widget(
            0, tool.Class, tool.PredefinedPropertySet, tool.Util
        )
    )

    core.load_context_menus(tool.Class, tool.Util)
    core.add_shortcuts(
        tool.Class, tool.Util, tool.Search, tool.MainWindow, tool.Project
    )
    core.init_main_window(tool.Class, tool.MainWindow)


def item_double_clicked():
    core.create_object_info_widget(
        mode=1,
        object_tool=tool.Class,
        predefined_property_set=tool.PredefinedPropertySet,
        util=tool.Util,
    )


def object_info_paint_event():
    core.object_info_refresh(tool.Class)
    pass


def repaint_event():
    core.refresh_object_tree(tool.Class, tool.Project)


def drop_event(event):
    core.item_dropped_on(event.pos(), tool.Class)


def on_new_project():
    core.reset_tree(tool.Class)


def retranslate_ui():
    core.retranslate_ui(tool.Class)


def create_object_called():
    core.create_object(
        tool.Class,
        tool.Project,
        tool.PropertySet,
        tool.PredefinedPropertySet,
        tool.Popups,
        tool.Util,
    )


def copy_object_called():
    core.copy_object(tool.Class)


def modify_object_called():
    core.modify_object(tool.Class)


def create_object_info_widget(mode: int):
    core.create_object_info_widget(
        mode, tool.Class, tool.PredefinedPropertySet, tool.Util
    )
