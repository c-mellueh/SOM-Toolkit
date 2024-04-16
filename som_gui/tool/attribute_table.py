from __future__ import annotations

from PySide6.QtWidgets import QTableWidgetItem, QTableWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QBrush, QIcon

import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.property_set_window.ui import PropertySetWindow
from som_gui.icons import get_link_icon
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from som_gui.module.attribute_table.prop import AttributeTableProperties
    from som_gui.module.attribute_table import ui

LINKSTATE = Qt.ItemDataRole.UserRole + 2


class AttributeTable(som_gui.core.tool.AttributeTable):
    @classmethod
    def set_active_table(cls, table: ui.AttributeTable):
        cls.get_properties().active_table = table

    @classmethod
    def get_active_table(cls):
        return cls.get_properties().active_table

    @classmethod
    def set_active_attribute(cls, attribute: SOMcreator.Attribute):
        prop = cls.get_properties()
        prop.active_attribute = attribute

    @classmethod
    def edit_attribute_name(cls):
        attribute = cls.get_properties().active_attribute
        window = cls.get_active_table().window()
        answer = tool.Popups.request_attribute_name(attribute.name, window)
        if answer:
            attribute.name = answer

    @classmethod
    def delete_selected_attribute(cls, delete_subattributes=False):
        attribute = cls.get_properties().active_attribute
        tool.Attribute.delete(attribute, delete_subattributes)

    @classmethod
    def remove_parent_of_selected_attribute(cls):
        attribute = cls.get_properties().active_attribute
        attribute.parent.remove_child(attribute)

    @classmethod
    def add_parent_of_selected_attribute(cls):
        attribute = cls.get_properties().active_attribute
        parent = cls.get_possible_parent(attribute)
        if not parent:
            return

        parent.add_child(attribute)

    @classmethod
    def get_properties(cls) -> AttributeTableProperties:
        return som_gui.AttributeTableProperties

    @classmethod
    def get_attribute_from_item(cls, item: QTableWidgetItem):
        if item is None:
            return None
        entity = item.data(CLASS_REFERENCE)
        return entity if isinstance(entity, SOMcreator.Attribute) else None

    @classmethod
    def remove_attributes_from_table(cls, attributes: set[SOMcreator.Attribute], table: QTableWidget):
        rows = sorted([cls.get_row_from_attribute(a, table) for a in attributes])
        for row in reversed(rows):
            table.removeRow(row)

    @classmethod
    def get_row_from_attribute(cls, attribute: SOMcreator.Attribute, table: QTableWidget):
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_attribute_from_item(item) == attribute:
                return row

    @classmethod
    def add_attributes_to_table(cls, attributes: list[SOMcreator.Attribute], table: QTableWidget):
        prop = cls.get_properties()
        column_list = prop.attribute_table_columns
        for attribute in attributes:
            table.setSortingEnabled(False)
            items = [QTableWidgetItem() for _ in range(len(column_list))]
            row = table.rowCount()
            table.setRowCount(row + 1)
            [item.setData(CLASS_REFERENCE, attribute) for item in items]
            [table.setItem(row, col, item) for col, item in enumerate(items)]
            [item.setFlags(item.flags() | item.flags().ItemIsUserCheckable) for item in items]
            cls.update_row(table, row)
            table.setSortingEnabled(True)

    @classmethod
    def update_row(cls, table: QTableWidget, index: int):
        items = [table.item(index, col) for col in range(table.columnCount())]
        prop = cls.get_properties()
        column_list = prop.attribute_table_columns
        attribute = cls.get_attribute_from_item(items[0])
        if attribute is None:
            return

        if attribute.parent is not None:
            if not items[0].data(LINKSTATE):
                items[0].setIcon(get_link_icon())
                items[0].setData(LINKSTATE, True)
        else:
            if items[0].data(LINKSTATE):
                items[0].setIcon(QIcon())
                items[0].setData(LINKSTATE, False)

        for item, column_dict in zip(items, column_list):
            value = column_dict["get_function"](attribute)
            cls.format_attribute_table_value(item, value)
        cls.format_row(items)

    @classmethod
    def format_attribute_table_value(cls, item: QTableWidgetItem, value):
        if isinstance(value, (list, set)):
            item.setText("; ".join([str(v) for v in value]))
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
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        if not attribute.property_set.object:
            brush.setColor(Qt.GlobalColor.white)
        elif attribute.property_set.object.ident_attrib == attribute:
            brush.setColor(Qt.GlobalColor.lightGray)
        else:
            brush.setColor(Qt.GlobalColor.white)
        for item in row:
            item.setBackground(brush)

    @classmethod
    def add_column_to_table(cls, name: str, get_function: Callable):
        prop = cls.get_properties()
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
    def get_property_set_by_table(cls, table: QTableWidget):
        window = table.window()
        if isinstance(window, PropertySetWindow):
            return tool.PropertySetWindow.get_property_set_by_window(window)
        if isinstance(window, som_gui.main_window.MainWindow):
            return tool.PropertySet.get_active_property_set()

    @classmethod
    def get_item_from_pos(cls, table: QTableWidget, pos: QPoint):
        item = table.itemAt(pos)
        return cls.get_attribute_from_item(item)

    @classmethod
    def get_attribute_table_header_names(cls):
        prop = cls.get_properties()
        return [d["display_name"] for d in prop.attribute_table_columns]

    @classmethod
    def get_possible_parent(cls, attribute: SOMcreator.Attribute) -> None | SOMcreator.Attribute:
        if not attribute.property_set:
            return None
        if not attribute.property_set.parent:
            return None
        return {a.name: a for a in attribute.property_set.parent.attributes}.get(attribute.name)
