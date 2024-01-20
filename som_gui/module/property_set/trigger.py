from __future__ import annotations
import som_gui
from som_gui.core import property_set as core
from som_gui import tool
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import PropertySetWindow


def connect():
    table = som_gui.MainUi.ui.table_pset
    table.itemSelectionChanged.connect(lambda: core.pset_selection_changed(tool.PropertySet, tool.Attribute))
    table.itemDoubleClicked.connect(lambda: core.table_double_clicked(tool.PropertySet))


def connect_property_set_window(widget: PropertySetWindow):
    pass


def repaint_pset_window(widget: PropertySetWindow):
    core.repaint_pset_window(widget, tool.PropertySet, tool.Attribute)


def on_new_project():
    pass


def repaint_event():
    core.refresh_table(tool.PropertySet, tool.Object)
