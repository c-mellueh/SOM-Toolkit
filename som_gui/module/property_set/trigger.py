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
    table.itemDoubleClicked.connect(lambda: core.table_double_clicked(tool.PropertySet, tool.Attribute))


def connect_property_set_window(window: PropertySetWindow):
    window.widget.button_add_line.clicked.connect(lambda: core.add_value_button_clicked(window, tool.PropertySet))
    window.widget.button_add.clicked.connect(
        lambda: core.add_attribute_button_clicked(window, tool.PropertySet, tool.Attribute))

    window.widget.combo_type.currentIndexChanged.connect(lambda: core.value_type_changed(window, tool.PropertySet))
def repaint_pset_window(widget: PropertySetWindow):
    core.repaint_pset_window(widget, tool.PropertySet, tool.Attribute)


def close_pset_window(window: PropertySetWindow):
    core.close_pset_window(window, tool.PropertySet)

def on_new_project():
    pass


def repaint_event():
    core.refresh_table(tool.PropertySet, tool.Object)
