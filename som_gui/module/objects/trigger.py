import som_gui
from som_gui import tool
from som_gui.core import objects as core
from PySide6.QtWidgets import QTreeWidget
from som_gui.icons import get_search_icon
def connect():
    widget: QTreeWidget = tool.Object.get_object_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, tool.Object))
    widget.itemSelectionChanged.connect(lambda: core.item_selection_changed(tool.Object, tool.PropertySet))
    widget.itemDoubleClicked.connect(item_double_clicked)
    widget.customContextMenuRequested.connect(lambda p: core.create_context_menu(p, tool.Object))
    widget.expanded.connect(lambda: core.resize_columns(tool.Object))
    main_ui = tool.MainWindow.get_ui()

    main_ui.button_search.pressed.connect(lambda: core.search_object(tool.Search, tool.Object))
    main_ui.button_objects_add.clicked.connect(
        lambda: core.add_object_clicked(tool.MainWindow, tool.Object, tool.Project))

    core.load_context_menus(tool.Object)
    core.add_shortcuts(tool.Object, tool.Project, tool.Search)
    main_ui.button_search.setIcon(get_search_icon())

def item_double_clicked():
    core.create_object_info_widget(mode=1, object_tool=tool.Object)

def item_copy_event():
    core.create_object_info_widget(mode=2, object_tool=tool.Object)

def object_info_paint_event():
    core.object_info_refresh(tool.Object)
    pass

def repaint_event():
    core.refresh_object_tree(tool.Object, tool.Project)


def change_event():
    core.item_changed(tool.Object)


def drop_event(event):
    core.item_dropped_on(event.pos(), tool.Object)


def on_new_project():
    core.reset_tree(tool.Object)
