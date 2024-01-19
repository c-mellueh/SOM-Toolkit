import som_gui
from som_gui.tool import Project, Object, Search, PropertySet
from som_gui.core import objects as core
from PySide6.QtWidgets import QTreeWidget
from som_gui.icons import get_search_icon
def connect():
    widget: QTreeWidget = Object.get_object_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, Object))
    widget.itemSelectionChanged.connect(lambda: core.item_selection_changed(Object, PropertySet))
    widget.itemDoubleClicked.connect(item_double_clicked)
    widget.customContextMenuRequested.connect(lambda p: core.create_context_menu(p, Object))
    widget.expanded.connect(lambda: core.resize_columns(Object))
    som_gui.MainUi.ui.button_search.pressed.connect(lambda: core.search_object(Search, Object))

    core.load_context_menus(Object)
    core.add_shortcuts(Object, Project, Search)
    som_gui.MainUi.ui.button_search.setIcon(get_search_icon())

def item_double_clicked():
    core.create_object_info_widget(mode=1, object_tool=Object)

def item_copy_event():
    core.create_object_info_widget(mode=2, object_tool=Object)

def object_info_paint_event():
    core.object_info_refresh(Object)
    pass

def repaint_event():
    core.refresh_object_tree(Object, Project)


def change_event():
    core.item_changed(Object)


def drop_event(event):
    core.item_dropped_on(event.pos(), Object)


def on_new_project():
    core.reset_tree(Object)
