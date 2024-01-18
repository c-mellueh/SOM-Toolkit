import som_gui
from som_gui.tool import Project, Objects
from som_gui.core import objects as core
from PySide6.QtWidgets import QTreeWidget


def connect():
    widget: QTreeWidget = Objects.get_object_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, Objects))


def repaint_event():
    core.refresh_object_tree(Objects, Project)


def mouse_press_event(event):
    pass


def mouse_move_event(event):
    pass


def mouse_release_event(event):
    pass
