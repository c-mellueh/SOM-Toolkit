from __future__ import annotations

import itertools
from typing import Callable, TYPE_CHECKING

from PySide6.QtCore import QCoreApplication, QModelIndex, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QCompleter,
    QListWidgetItem,
    QMenu,
    QTableWidget,
    QTableWidgetItem,
)

import SOMcreator
import som_gui
import som_gui.core.tool
from SOMcreator.datastructure.som_json import INHERITED_TEXT
from som_gui import tool
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.resources.icons import get_link_icon
from som_gui.module.property_set import trigger

if TYPE_CHECKING:
    from som_gui.module.property_set.prop import PropertySetProperties
    from som_gui.module.property_set.ui import PsetTableWidget


class PropertySet(som_gui.core.tool.PropertySet):

    @classmethod
    def get_attribute_by_name(cls, property_set: SOMcreator.SOMPropertySet, name: str):
        attribute_dict = {a.name: a for a in property_set.get_properties(filter=False)}
        return attribute_dict.get(name)

    @classmethod
    def get_inheritable_property_sets(
        cls, obj: SOMcreator.SOMClass
    ) -> list[SOMcreator.SOMPropertySet]:
        def loop(o: SOMcreator.SOMClass):
            psets = o.get_property_sets(filter=False)
            if o.parent:
                psets = itertools.chain(psets, loop(o.parent))
            return psets

        return list(loop(obj))

    @classmethod
    def get_pset_from_index(cls, index: QModelIndex) -> SOMcreator.SOMPropertySet:
        return index.data(CLASS_REFERENCE)

    @classmethod
    def pset_table_is_editing(cls):
        props = cls.get_properties()
        return props.is_renaming_property_set

    @classmethod
    def get_property_set_from_row(cls, row, table):
        return cls.get_property_set_from_item(table.item(row, 0))

    @classmethod
    def set_pset_name_by_row(cls, pset, row, table):
        item = table.item(row, 0)
        pset.name = item.text()

    @classmethod
    def rename_table_pset(cls):
        property_set = cls.get_selecte_property_set_from_table()
        table = cls.get_table()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_property_set_from_item(item) == property_set:
                table.editItem(item)

    @classmethod
    def delete_table_pset(cls):
        property_set = cls.get_selecte_property_set_from_table()
        delete_request, delete_child = tool.Popups.req_delete_items(
            [property_set.name], 3
        )
        if delete_request:
            property_set.delete(recursive=delete_child)

    @classmethod
    def create_context_menu(cls, global_pos, function_list: list[list[str, Callable]]):
        menu = QMenu()
        actions = list()
        for action_name, action_function in function_list:
            action = QAction(action_name)
            actions.append(action)
            menu.addAction(action)
            action.triggered.connect(action_function)
        menu.exec(global_pos)

    @classmethod
    def get_property_set_from_item(
        cls, item: QTableWidgetItem | QListWidgetItem
    ) -> SOMcreator.SOMPropertySet:
        return item.data(CLASS_REFERENCE)

    @classmethod
    def check_if_pset_allready_exists(
        cls, pset_name: str, active_object: SOMcreator.SOMClass
    ):
        return bool(
            pset_name in {p.name for p in active_object.get_property_sets(filter=False)}
        )

    @classmethod
    def create_property_set(
        cls,
        name: str,
        obj: SOMcreator.SOMClass | None = None,
        parent: SOMcreator.SOMPropertySet | None = None,
    ) -> SOMcreator.SOMPropertySet | None:

        if obj:
            if name in {p.name for p in obj.get_property_sets(filter=False)}:
                text = QCoreApplication.translate(
                    f"PropertySet", "PropertySet '{}' exists allready"
                ).format(name)
                tool.Popups.create_warning_popup(text)
                return None
        if parent is not None:
            property_set = parent.create_child(name)
            if obj:
                obj.add_property_set(property_set)
        else:
            property_set = SOMcreator.SOMPropertySet(
                name, obj, project=tool.Project.get()
            )
        return property_set

    @classmethod
    def get_pset_from_item(cls, item: QTableWidgetItem) -> SOMcreator.SOMPropertySet:
        return item.data(CLASS_REFERENCE)

    @classmethod
    def get_existing_psets_in_table(cls, table: QTableWidget):
        psets = set()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            psets.add(cls.get_pset_from_item(item))
        return psets

    @classmethod
    def clear_table(cls):
        table = cls.get_table()
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)

    @classmethod
    def get_property_sets(cls) -> set[SOMcreator.SOMPropertySet]:
        active_object = tool.Class.get_active_class()
        if active_object is None:
            return set()
        return set(active_object.get_property_sets(filter=True))

    @classmethod
    def get_table(cls):
        return tool.MainWindow.get_property_set_table_widget()

    @classmethod
    def get_row_from_pset(cls, property_set: SOMcreator.SOMPropertySet):
        table = cls.get_table()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_pset_from_item(item) == property_set:
                return row

    @classmethod
    def remove_property_sets_from_table(
        cls, property_sets: set[SOMcreator.SOMPropertySet], table: QTableWidget
    ):
        rows = sorted(cls.get_row_from_pset(p) for p in property_sets)
        for row in reversed(rows):
            table.removeRow(row)

    @classmethod
    def add_property_sets_to_table(
        cls, property_sets: set[SOMcreator.SOMPropertySet], table: QTableWidget
    ):
        for property_set in property_sets:
            table.setSortingEnabled(False)
            items = [QTableWidgetItem() for _ in range(3)]
            row = table.rowCount()
            table.setRowCount(row + 1)
            [item.setData(CLASS_REFERENCE, property_set) for item in items]
            [
                item.setFlags(
                    item.flags()
                    | Qt.ItemFlag.ItemIsEditable
                    | Qt.ItemFlag.ItemIsUserCheckable
                )
                for item in items
            ]
            [table.setItem(row, col, item) for col, item in enumerate(items)]
            items[2].setCheckState(Qt.CheckState.Unchecked)
            table.setSortingEnabled(True)

    @classmethod
    def update_table_row(cls, table, row):
        items = [table.item(row, col) for col in range(table.columnCount())]
        property_set = cls.get_property_set_from_item(items[0])
        check_state = (
            Qt.CheckState.Checked
            if property_set.is_optional(ignore_hirarchy=True)
            else Qt.CheckState.Unchecked
        )

        if items[0].text() != property_set.name:
            items[0].setText(f"{property_set.name}")
        if property_set.is_child:
            text = (
                property_set.parent.name
                if property_set.parent.som_class is not None
                else INHERITED_TEXT
            )

            if items[1].text() != text:
                items[1].setText(text)
                items[0].setIcon(get_link_icon())
        else:
            if items[1].text() != "":
                items[0].setIcon(QIcon())
                items[1].setText("")

        if items[2].checkState() != check_state:
            items[2].setCheckState(check_state)

    @classmethod
    def update_property_set_table(cls, table: QTableWidget):
        for row in range(table.rowCount()):
            cls.update_table_row(table, row)

    @classmethod
    def select_property_set(cls, property_set: SOMcreator.SOMPropertySet):
        table = cls.get_table()
        table.setFocus()
        for row in range(table.rowCount()):
            if cls.get_pset_from_item(table.item(row, 0)) == property_set:
                table.selectRow(row)
                table.setCurrentCell(row, 0)

    @classmethod
    def get_selecte_property_set_from_table(cls) -> SOMcreator.SOMPropertySet | None:
        table = cls.get_table()
        items = table.selectedItems()
        if not items:
            return
        item = items[0]
        return cls.get_pset_from_item(item)

    @classmethod
    def get_completer(cls) -> QCompleter:
        if not cls.get_properties().completer:
            cls.get_properties().completer = QCompleter()
        return cls.get_properties().completer

    @classmethod
    def update_completer(cls, obj: SOMcreator.SOMClass = None):
        psets = list(tool.PredefinedPropertySet.get_property_sets())
        if obj is not None:
            psets += cls.get_inheritable_property_sets(obj)
        pset_names = sorted({p.name for p in psets})
        cls.get_properties().completer = QCompleter(pset_names)

    @classmethod
    def set_enabled(cls, enabled: bool):
        tool.MainWindow.get_ui().table_attribute.setEnabled(enabled)
        tool.MainWindow.get_ui().table_pset.setEnabled(enabled)
        tool.MainWindow.get_ui().button_Pset_add.setEnabled(enabled)

    @classmethod
    def get_properties(cls) -> PropertySetProperties:
        return som_gui.PropertySetProperties

    @classmethod
    def set_active_property_set(cls, property_set: SOMcreator.SOMPropertySet):
        prop = cls.get_properties()
        prop.active_pset = property_set

    @classmethod
    def get_active_property_set(cls) -> SOMcreator.SOMPropertySet:
        prop = cls.get_properties()
        return prop.active_pset

    @classmethod
    def set_sorting_indicator(
        cls, table_widget: PsetTableWidget, col_index: int
    ) -> None:
        table_widget.setSortingEnabled(True)
        header = table_widget.horizontalHeader()
        header.setSortIndicator(
            col_index, Qt.SortOrder.AscendingOrder
        )  # 0 for ascending order, 1 for descending order
        header.setSortIndicatorShown(True)

    @classmethod
    def trigger_table_repaint(cls):
        trigger.repaint_event()
