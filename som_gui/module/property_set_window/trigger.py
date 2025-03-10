from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6 import QtGui

from som_gui import tool
from som_gui.core import property_set_window as core
from .constants import SEPERATOR_SECTION, SEPERATOR_STATUS
from . import ui

if TYPE_CHECKING:
    from .ui import PropertySetWindow


def connect():
    tool.Settings.add_page_to_toolbox(
        ui.SplitterSettings,
        "pageSplitter",
        lambda: core.splitter_settings_accepted(tool.PropertySetWindow, tool.Appdata),
    )

    pass


def on_new_project():
    pass


def connect_window(window: ui.PropertySetWindow):
    window.ui.button_add_line.clicked.connect(
        lambda: core.add_value_button_clicked(window, tool.PropertySetWindow)
    )
    window.ui.button_add.clicked.connect(
        lambda: core.add_attribute_button_clicked(
            window, tool.PropertySet, tool.PropertySetWindow, tool.Property
        )
    )
    window.ui.combo_value_type.currentIndexChanged.connect(
        lambda: core.value_type_changed(window, tool.PropertySetWindow)
    )
    window.ui.check_box_inherit.stateChanged.connect(
        lambda: core.inherit_checkbox_toggled(window, tool.PropertySetWindow)
    )

    table = window.ui.table_widget
    table.itemClicked.connect(
        lambda item: core.attribute_clicked(
            item, tool.PropertyTable, tool.PropertySetWindow
        )
    )


def repaint_window(widget: ui.PropertySetWindow):
    core.repaint_pset_window(widget, tool.PropertySetWindow,tool.PropertySet, tool.PropertyTable)


def close_window(window: ui.PropertySetWindow):
    core.close_pset_window(window, tool.PropertySetWindow)


def key_press_event(event, window: ui.PropertySetWindow):
    sep_bool = tool.Appdata.get_bool_setting(SEPERATOR_SECTION, SEPERATOR_STATUS)
    if not event.matches(QtGui.QKeySequence.StandardKey.Paste) and sep_bool:
        return True
    return core.handle_paste_event(window, tool.PropertySetWindow)


def retranslate_ui():
    core.retranslate_ui(tool.PropertySetWindow)


def splitter_settings_created(widget: ui.SplitterSettings):
    core.fill_splitter_settings(widget, tool.PropertySetWindow, tool.Appdata)


def splitter_checkstate_changed(widget: ui.SplitterSettings):
    core.update_splitter_enabled_state(widget, tool.PropertySetWindow)
