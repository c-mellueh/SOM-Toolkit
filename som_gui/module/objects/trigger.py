import som_gui
from som_gui.tool import Project, Objects
from som_gui.core import objects as core
from PySide6.QtWidgets import QTreeWidget


def connect():
    widget: QTreeWidget = Objects.get_object_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, Objects))
    widget.itemSelectionChanged.connect(lambda: core.item_selection_changed(Objects))

def repaint_event():
    core.refresh_object_tree(Objects, Project)


def change_event():
    core.item_changed(Objects)


def drop_event(event):
    print(F"DROP EVENT")
    core.item_dropped_on(event.pos(), Objects)
