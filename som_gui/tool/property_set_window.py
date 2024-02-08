from __future__ import annotations
import logging

from PySide6.QtWidgets import QTableWidgetItem, QCompleter, QTableWidget, QHBoxLayout, QLineEdit, QListWidget, \
    QListWidgetItem, QMenu
from PySide6.QtCore import Qt, QModelIndex, QPoint
from PySide6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator, QAction, QIcon

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
    def edit_attribute_name(cls):
        attribute = cls.get_properties().active_attribute
        window = tool.PropertySet.get_active_window()
        answer = tool.Popups.request_attribute_name(attribute.name, window)
        if answer:
            attribute.name = answer

    @classmethod
    def delete_selected_attribute(cls):
        attribute = cls.get_properties().active_attribute
        tool.Attribute.delete(attribute)

    @classmethod
    def get_attribute_from_item(cls, item: QTableWidgetItem):
        if item is None:
            return None
        entity = item.data(CLASS_REFERENCE)
        return entity if isinstance(entity, SOMcreator.Attribute) else None

    @classmethod
    def get_item_from_pos(cls, table: QTableWidget, pos: QPoint):
        item = table.itemAt(pos)
        return cls.get_attribute_from_item(item)

    @classmethod
    def get_table(cls, window: ui.PropertySetWindow):
        return window.widget.table_widget

    @classmethod
    def set_active_attribute(cls, attribute: SOMcreator.Attribute):
        prop = cls.get_properties()
        prop.active_attribute = attribute

    @classmethod
    def set_active_window(cls, window):
        cls.get_properties().active_window = window

    @classmethod
    def get_table(cls, window: PropertySetWindow):
        return window.widget.table_widget

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
