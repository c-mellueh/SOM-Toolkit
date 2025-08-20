from __future__ import annotations

from typing import TYPE_CHECKING, Type
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QModelIndex
from SOMcreator.util.units import uri_to_code
if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.property_window import ui
    from PySide6.QtCore import QPoint
    from PySide6.QtWidgets import QTreeView
import SOMcreator

from som_gui.module.property_window.constants import (
    SEPERATOR_SECTION,
    SEPERATOR_STATUS,
    SEPERATOR,
)


def open_property_info(
    som_property: SOMcreator.SOMProperty,
    property_window: Type[tool.PropertyWindow],
    util: Type[tool.Util],
):
    if window := property_window.get_window(som_property):
        if window.isHidden():
            window.close()
            window = property_window.create_window(som_property)
    else:
        window = property_window.create_window(som_property)
    window.show()
    window.activateWindow()
    window.showNormal()


def retranslate_ui(property_window: Type[tool.PropertyWindow]):
    for window in property_window.get_windows():
        window.ui.retranslateUi(window)
        title = property_window.create_window_title(window.som_property)
        window.setWindowTitle(title)


def connect_signals(
    property_window: Type[tool.PropertyWindow], property_table: Type[tool.PropertyTable]
):
    property_table.signaller.property_info_requested.connect(
        property_window.show_property_info
    )
    property_window.connect_signals()


def init_window(
    window: ui.PropertyWindow,
    property_window: Type[tool.PropertyWindow],
    util: Type[tool.Util],
):
    property_window.prefill_comboboxes(window)
    property_window.update_unit_completer(window)
    property_window.connect_value_view(window)


def connect_window(
    window: ui.PropertyWindow,
    property_window: Type[tool.PropertyWindow],
    util: Type[tool.Util],
):
    som_property = property_window.get_property_from_window(window)
    widget_ui = window.ui
    widget_ui.lineEdit_name.textEdited.connect(
        lambda t: property_window.rename_property(som_property, t)
    )

    def get_datatype_text():
        return property_window.get_datatype_combobox(widget_ui).currentText()

    def get_valuetype_text():
        return property_window.get_valuetype_combobox(widget_ui).currentText()

    def get_unit_text():
        return property_window.get_unit_combobox(widget_ui).currentText()

    def get_description_text():
        return property_window.get_description_textedit(widget_ui).toPlainText()

    widget_ui.combo_data_type.currentIndexChanged.connect(
        lambda i: property_window.set_datatype(som_property, get_datatype_text())
    )
    widget_ui.combo_value_type.currentIndexChanged.connect(
        lambda i: property_window.set_valuetype(som_property, get_valuetype_text())
    )
    # widget_ui.combo_unit.currentIndexChanged.connect(
    #     lambda i: property_window.set_unit(som_property, get_unit_text())
    # )

    widget_ui.description.textChanged.connect(
        lambda: property_window.set_description(som_property, get_description_text())
    )
    widget_ui.check_box_optional.checkStateChanged.connect(
        lambda cs: property_window.set_optional(
            som_property, util.checkstate_to_bool(cs)
        )
    )
    widget_ui.check_box_inherit.checkStateChanged.connect(
        lambda cs: property_window.set_value_inherit_state(
            som_property, util.checkstate_to_bool(cs)
        )
    )
    widget_ui.button_add_line.clicked.connect(
        lambda: property_window.add_value(
            widget_ui.table_view_value,
        )
    )
    window.closed.connect(lambda: property_window.remove_window(window))


def update_window(
    window: ui.PropertyWindow,
    property_window: Type[tool.PropertyWindow],
    util: Type[tool.Util],
    units:Type[tool.Units]
):
    som_property = property_window.get_property_from_window(window)
    ui = window.ui
    ui.lineEdit_name.setText(som_property.name)
    ui.combo_data_type.setCurrentText(som_property.data_type)
    ui.combo_value_type.setCurrentText(som_property.value_type)
    ui.combo_unit.setCurrentText(uri_to_code(som_property.unit))
    ui.description.setText(som_property.description)
    property_window.set_comboboxes_enabled(not som_property.is_child, window)
    inherits_values_checkstate = util.bool_to_checkstate(
        som_property.child_inherits_values
    )
    ui.check_box_inherit.setCheckState(inherits_values_checkstate)
    ui.table_view_value.model().sourceModel().update_values()


def create_context_menu_builders(property_window: Type[tool.PropertyWindow]):
    property_window.add_context_menu_builder(property_window.ignore_builder)
    property_window.add_context_menu_builder(property_window.unignore_builder)
    property_window.add_context_menu_builder(property_window.remove_builder)


def value_context_menu_request(
    pos: QPoint,
    table_view: ui.ValueView,
    property_window: Type[tool.PropertyWindow],
    util: Type[tool.Util],
):
    menu_builders = property_window.get_context_menu_builders()
    menu_list = []
    for builder in menu_builders:
        result = builder(table_view)
        if result is not None:
            menu_list.append(result)
    menu = util.create_context_menu(menu_list)
    menu.exec(table_view.mapToGlobal(pos))


def handle_paste_event(
    table_view: ui.ValueView,
    property_window: Type[tool.PropertyWindow],
    appdata: Type[tool.Appdata],
) -> None:
    start_row = min(property_window.get_selected_rows(table_view), default=0)
    sep_bool = appdata.get_bool_setting(SEPERATOR_SECTION, SEPERATOR_STATUS)
    text = QGuiApplication.clipboard().text()
    if not sep_bool:
        property_window.set_value(table_view, start_row, text)
        return

    seperator = appdata.get_string_setting(SEPERATOR_SECTION, SEPERATOR, ";")
    text_list = text.split(seperator)
    property_window.set_values(table_view, start_row, text_list)


def handle_copy_event(
    table_view: ui.ValueView,
    property_window: Type[tool.PropertyWindow],
    appdata: Type[tool.Appdata],
):
    values = property_window.get_selected_values(table_view)
    if not values:
        return
    seperator = appdata.get_string_setting(SEPERATOR_SECTION, SEPERATOR, ";")
    QGuiApplication.clipboard().setText(seperator.join(values))


#### Settings Window


def fill_splitter_settings(
    widget: ui.SplitterSettings,
    property_window: Type[tool.PropertyWindow],
    appdata: Type[tool.Appdata],
):
    property_window.set_splitter_settings_widget(widget)
    seperator = appdata.get_string_setting(SEPERATOR_SECTION, SEPERATOR, ",")
    is_sperator_activated = appdata.get_bool_setting(
        SEPERATOR_SECTION, SEPERATOR_STATUS
    )

    widget.ui.line_edit_seperator.setText(seperator)
    widget.ui.check_box_seperator.setChecked(is_sperator_activated)
    property_window.connect_splitter_widget(widget)
    update_splitter_enabled_state(widget, property_window)
    pass


def splitter_settings_accepted(
    property_window: Type[tool.PropertyWindow], appdata: Type[tool.Appdata]
):
    widget = property_window.get_splitter_settings_widget()
    is_seperator_activated = property_window.get_splitter_settings_checkstate(widget)
    text = property_window.get_splitter_settings_text(widget)
    text = text.replace("\\n", "\n")
    text = text.replace("\\t", "\t")

    appdata.set_setting(SEPERATOR_SECTION, SEPERATOR, text)
    appdata.set_setting(SEPERATOR_SECTION, SEPERATOR_STATUS, is_seperator_activated)
    if not text:
        appdata.set_setting(SEPERATOR_SECTION, SEPERATOR_STATUS, False)


def update_splitter_enabled_state(
    widget: ui.SplitterSettings,
    property_window: Type[tool.PropertyWindow],
):
    is_seperator_activated = property_window.get_splitter_settings_checkstate(widget)
    widget.ui.line_edit_seperator.setEnabled(is_seperator_activated)
