from __future__ import annotations
import logging

from PySide6.QtWidgets import QTableWidgetItem, QCompleter, QTableWidget, QHBoxLayout, QLineEdit, QListWidget, \
    QListWidgetItem, QMenu
from PySide6.QtCore import Qt, QModelIndex, QPoint
from PySide6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator, QAction, QIcon, QGuiApplication

from SOMcreator.constants.json_constants import INHERITED_TEXT
from SOMcreator.constants.value_constants import VALUE_TYPE_LOOKUP, DATA_TYPES
from SOMcreator.constants import value_constants

import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.icons import get_link_icon
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.attribute import trigger as attribute_trigger
from som_gui.module.property_set import trigger as property_set_trigger
from som_gui.module.property_set import ui

import SOMcreator

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from som_gui.module.property_set_window.prop import PropertySetWindowProperties
    from som_gui.module.property_set_window import ui


class PropertySetWindow(som_gui.core.tool.PropertySetWindow):
    @classmethod
    def get_properties(cls) -> PropertySetWindowProperties:
        return som_gui.PropertySetWindowProperties




    @classmethod
    def get_table(cls, window: ui.PropertySetWindow):
        return window.widget.table_widget


    @classmethod
    def set_active_window(cls, window):
        cls.get_properties().active_window = window

    @classmethod
    def get_table(cls, window: PropertySetWindow):
        return window.widget.table_widget

    @classmethod
    def get_window_by_property_set(cls, property_set: SOMcreator.PropertySet):
        prop = cls.get_properties()
        return {pset: window for window, pset in prop.property_set_windows.items()}.get(property_set)

    @classmethod
    def get_property_set_from_window(cls, window: PropertySetWindow) -> SOMcreator.PropertySet:
        prop = cls.get_properties()
        return prop.property_set_windows.get(window)

    @classmethod
    def get_attribute_name(cls, window: ui.PropertySetWindow):
        return window.widget.lineEdit_name.text()

    @classmethod
    def pw_get_attribute_data(cls, window: ui.PropertySetWindow):
        d = dict()
        d["name"] = cls.get_attribute_name(window)
        d["data_type"] = window.widget.combo_data_type.currentText()
        d["value_type"] = window.widget.combo_type.currentText()
        d["values"] = cls.get_values(window)
        d["description"] = window.widget.description.toPlainText()
        return d

    @classmethod
    def get_input_value_lines(cls, window: ui.PropertySetWindow) -> list[list[QLineEdit]]:
        lines = list()
        base_layout = window.widget.verticalLayout_2
        for row in range(base_layout.count()):
            hor_layout: QHBoxLayout = base_layout.itemAt(row)
            lines.append([hor_layout.itemAt(col).widget() for col in range(hor_layout.count())])
        return lines

    @classmethod
    def get_values(cls, window: ui.PropertySetWindow):
        lines = cls.get_input_value_lines(window)
        value_list = list()
        for row in lines:
            values = cls.format_values([line.text() for line in row if line.text()], window)
            if not values:
                continue
            if len(values) > 1:
                value_list.append(values)
            else:
                value_list.append(values[0])
        return value_list

    @classmethod
    def format_values(cls, value_list: list[str], window: ui.PropertySetWindow):
        data_type = cls.get_data_type(window)
        if data_type not in (value_constants.REAL, value_constants.INTEGER):
            return [str(val) for val in value_list]
        values = [val.replace(".", "") for val in value_list]  # remove thousend Point
        values = [float(val.replace(",", ".")) for val in values if val]
        if data_type == value_constants.INTEGER:
            values = [int(val) for val in value_list]
        if len(values) < len(value_list):
            values += [None for _ in range(len(value_list) - len(values))]
        return values

    @classmethod
    def get_data_type(cls, window: ui.PropertySetWindow):
        return window.widget.combo_data_type.currentText()

    @classmethod
    def get_value_type(cls, window: ui.PropertySetWindow):
        return window.widget.combo_type.currentText()

    @classmethod
    def add_value_line(cls, column_count: int, window: ui.PropertySetWindow) -> QHBoxLayout:
        new_layout = QHBoxLayout()
        for _ in range(column_count):
            new_layout.addWidget(ui.LineInput())
        window.widget.verticalLayout_2.addLayout(new_layout)
        return new_layout

    @classmethod
    def close_property_set_window(cls, window: ui.PropertySetWindow):
        logging.debug(f"Remove {window}")
        prop = cls.get_properties()
        if window in prop.property_set_windows:
            prop.property_set_windows.pop(window)
        else:
            logging.warning(f"PropertySetWindow can't be removed because it's not registred")

    @classmethod
    def get_paste_text_list(cls):
        seperator = tool.Settings.get_seperator()
        seperator_status = tool.Settings.get_seperator_status()
        if not seperator_status:
            return True

        text = QGuiApplication.clipboard().text()
        text_list = text.split(seperator)
        return text_list

    @classmethod
    def get_required_column_count(cls, window: ui.PropertySetWindow):
        value_type = cls.get_value_type(window)
        if value_type == value_constants.RANGE:
            return 2
        else:
            return 1

    @classmethod
    def bring_window_to_front(cls, window: ui.PropertySetWindow):
        window.raise_()

    @classmethod
    def create_window(cls, property_set: SOMcreator.PropertySet):
        prop = cls.get_properties()
        window = ui.PropertySetWindow()
        prop.property_set_windows[window] = property_set
        window.show()

    @classmethod
    def get_allowed_value_types(cls):
        return VALUE_TYPE_LOOKUP.keys()

    @classmethod
    def get_allowed_data_types(cls):
        return DATA_TYPES

    @classmethod
    def fill_window_ui(cls, window: ui.PropertySetWindow):
        window.widget.combo_type.clear()
        window.widget.combo_type.addItems(cls.get_allowed_value_types())
        window.widget.combo_data_type.clear()
        window.widget.combo_data_type.addItems(cls.get_allowed_data_types())
        window.widget.combo_type.setCurrentText(value_constants.LIST)
        window.widget.combo_data_type.setCurrentText(value_constants.LABEL)
        cls.add_value_line(1, window)

    @classmethod
    def connect_window_triggers(cls, window):
        som_gui.module.property_set_window.trigger.connect_window(window)

    @classmethod
    def fill_window_title(cls, window: ui.PropertySetWindow, property_set: SOMcreator.PropertySet):
        title = f"{property_set.object.name}:{property_set.name}" if property_set.object else f"{property_set.name}"
        window.setWindowTitle(title)
