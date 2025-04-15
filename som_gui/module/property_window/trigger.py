from __future__ import annotations
import som_gui
from som_gui import tool
from som_gui.core import property_window as core
from typing import TYPE_CHECKING
import SOMcreator

if TYPE_CHECKING:
    from . import ui


def connect():
    core.connect_signals(tool.PropertyWindow, tool.PropertyTable)
    core.create_context_menu_builders(tool.PropertyWindow)


def retranslate_ui():
    pass


def on_new_project():
    pass


def property_info_requested(som_property: SOMcreator.SOMProperty):
    core.open_property_info(som_property, tool.PropertyWindow)


def window_created(window: ui.PropertyWindow):
    core.init_window(window, tool.PropertyWindow)
    core.connect_window(window, tool.PropertyWindow, tool.Util)
    core.update_window(window, tool.PropertyWindow, tool.Util)


def update_window(window: ui.PropertyWindow):
    core.update_window(window, tool.PropertyWindow, tool.Util)


def value_context_menu_request(pos, table_view: ui.ValueView):
    core.value_context_menu_request(pos, table_view, tool.PropertyWindow, tool.Util)
