from __future__ import annotations
from typing import TYPE_CHECKING
from som_gui import tool
from som_gui.core import modelcheck as core

if TYPE_CHECKING:
    from .ui import ModelcheckWindow
    from PySide6.QtWidgets import QTreeView
    from PySide6.QtGui import QStandardItemModel

def connect():
    tool.MainWindow.add_action("Modelcheck/Interne Modellprüfung",
                               lambda: core.open_window(tool.Modelcheck, tool.IfcImporter))


def paint_object_tree():
    core.paint_object_tree(tool.Modelcheck, tool.Project)


def paint_pset_tree():
    core.paint_pset_tree(tool.Modelcheck)

def connect_object_check_tree(widget: QTreeView):
    model: QStandardItemModel = widget.model()
    model.itemChanged.connect(lambda item: core.object_check_changed(item, tool.Modelcheck))
    widget.selectionModel().selectionChanged.connect(
        lambda item: core.object_selection_changed(widget.selectionModel(), tool.Modelcheck))


def connect_pset_check_tree(widget: QTreeView):
    model: QStandardItemModel = widget.model()
    model.itemChanged.connect(lambda item: core.object_check_changed(item, tool.Modelcheck))

def connect_window(widget: ModelcheckWindow):
    pass


def on_new_project():
    pass
