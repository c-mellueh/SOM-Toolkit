from __future__ import annotations
import SOMcreator
import som_gui.core.tool
from typing import Callable, TYPE_CHECKING
from som_gui import tool
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6 import QtGui
from PySide6.QtCore import Qt
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.property_set import ui as property_set_ui

if TYPE_CHECKING:
    from som_gui.module.attribute.prop import AttributeProperties


class Attribute(som_gui.core.tool.Attribute):
    @classmethod
    def get_attribute_table_header_names(cls):
        prop = cls.get_attribute_properties()
        return [d["display_name"] for d in prop.attribute_table_columns]

    @classmethod
    def get_attribute_name(cls, attribute: SOMcreator.Attribute):
        return attribute.name

    @classmethod
    def get_attribute_data_type(cls, attribute: SOMcreator.Attribute):
        return attribute.data_type

    @classmethod
    def get_attribute_value_type(cls, attribute: SOMcreator.Attribute):
        return attribute.value_type

    @classmethod
    def get_attribute_values(cls, attribute: SOMcreator.Attribute):
        return attribute.value

    @classmethod
    def is_attribute_optional(cls, attribute: SOMcreator.Attribute):
        return attribute.optional

    @classmethod
    def get_attribute_properties(cls) -> AttributeProperties:
        return som_gui.AttributeProperties

    @classmethod
    def add_column_to_table(cls, name: str, get_function: Callable):
        prop = cls.get_attribute_properties()
        d = {"display_name": name,
             "get_function": get_function}
        prop.attribute_table_columns.append(d)

    @classmethod
    def get_existing_attributes_in_table(cls, table: QTableWidget):
        attributes = set()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            attributes.add(cls.get_attribute_from_item(item))
        return attributes

    @classmethod
    def get_attribute_from_item(cls, item: QTableWidgetItem):
        if item is None:
            return None
        entity = item.data(CLASS_REFERENCE)
        return entity if isinstance(entity, SOMcreator.Attribute) else None

    @classmethod
    def get_property_set_by_table(cls, table: QTableWidget):
        window = table.window()
        if isinstance(window, property_set_ui.PropertySetWindow):
            return tool.PropertySet.get_property_set_from_window(window)
        if isinstance(window, som_gui.main_window.MainWindow):
            return tool.PropertySet.get_active_property_set()

    @classmethod
    def get_row_from_attribute(cls, attribute: SOMcreator.Attribute, table: QTableWidget):
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_attribute_from_item(item) == attribute:
                return row

    @classmethod
    def remove_attributes_from_table(cls, attributes: set[SOMcreator.Attribute], table: QTableWidget):
        rows = sorted([cls.get_row_from_attribute(a, table) for a in attributes])
        for row in reversed(rows):
            table.removeRow(row)

    @classmethod
    def format_attribute_table_value(cls, item: QTableWidgetItem, value):
        if isinstance(value, (list, set)):
            item.setText("; ".join(value))
            return
        if isinstance(value, bool):
            cs = Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
            item.setText("")
            item.setCheckState(cs)
            return
        item.setText(str(value))

    @classmethod
    def format_row(cls, row: list[QTableWidgetItem]):
        attribute = cls.get_attribute_from_item(row[0])
        brush = QtGui.QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        if attribute.property_set.object.ident_attrib == attribute:
            brush.setColor(Qt.GlobalColor.lightGray)
        else:
            brush.setColor(Qt.GlobalColor.white)
        for item in row:
            item.setBackground(brush)

    @classmethod
    def update_row(cls, table: QTableWidget, index: int):
        items = [table.item(index, col) for col in range(table.columnCount())]
        prop = cls.get_attribute_properties()
        column_list = prop.attribute_table_columns
        attribute = cls.get_attribute_from_item(items[0])
        if attribute is None:
            return
        for item, column_dict in zip(items, column_list):
            value = column_dict["get_function"](attribute)
            cls.format_attribute_table_value(item, value)
        cls.format_row(items)

    @classmethod
    def add_attributes_to_table(cls, attributes: list[SOMcreator.Attribute], table: QTableWidget):
        prop = cls.get_attribute_properties()
        column_list = prop.attribute_table_columns
        for attribute in attributes:
            items = [QTableWidgetItem() for _ in range(len(column_list))]
            row = table.rowCount()
            table.setRowCount(row + 1)
            [item.setData(CLASS_REFERENCE, attribute) for item in items]
            [table.setItem(row, col, item) for col, item in enumerate(items)]
            cls.update_row(table, row)
