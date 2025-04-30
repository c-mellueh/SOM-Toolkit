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
import logging
import SOMcreator
import som_gui
import som_gui.core.tool
from SOMcreator.datastructure.som_json import INHERITED_TEXT
from som_gui import tool
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.resources.icons import get_link_icon
from som_gui.module.property_set import trigger
from SOMcreator.datastructure import ifc_schema

if TYPE_CHECKING:
    from som_gui.module.property_set.prop import PropertySetProperties
    from som_gui.module.property_set.ui import PsetTableWidget


class PropertySet(som_gui.core.tool.PropertySet):

    @classmethod
    def get_property_by_name(
        cls, property_set: SOMcreator.SOMPropertySet, name: str
    ) -> SOMcreator.SOMProperty | None:
        if property_set is None:
            return None
        property_dict = {a.name: a for a in property_set.get_properties(filter=False)}
        return property_dict.get(name)

    @classmethod
    def get_inheritable_property_sets(
        cls, som_class: SOMcreator.SOMClass
    ) -> list[SOMcreator.SOMPropertySet]:
        def loop(c: SOMcreator.SOMClass):
            psets = c.get_property_sets(filter=False)
            if c.parent:
                psets = itertools.chain(psets, loop(c.parent))
            return psets

        return list(loop(som_class))

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
    def is_pset_existing(cls, pset_name: str, active_class: SOMcreator.SOMClass):
        return bool(
            pset_name in {p.name for p in active_class.get_property_sets(filter=False)}
        )

    @classmethod
    def create_property_set(
        cls,
        name: str,
        som_class: SOMcreator.SOMClass | None = None,
        parent: SOMcreator.SOMPropertySet | None = None,
    ) -> SOMcreator.SOMPropertySet | None:

        if som_class:
            pset_dict = {p.name: p for p in som_class.get_property_sets(filter=False)}
            if name in pset_dict:
                text = QCoreApplication.translate(
                    f"PropertySet", "PropertySet '{}' exists allready"
                ).format(name)
                logging.info(text)
                return pset_dict.get(name)
        if parent is not None:
            property_set = parent.create_child(name)
            if som_class:
                som_class.add_property_set(property_set)
        else:
            property_set = SOMcreator.SOMPropertySet(
                name, som_class, project=tool.Project.get()
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
    def get_property_sets(
        cls, active_class: SOMcreator.SOMClass
    ) -> set[SOMcreator.SOMPropertySet]:
        if active_class is None:
            return set()
        return set(active_class.get_property_sets(filter=True))

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
    def set_enabled(cls, enabled: bool):
        tool.MainWindow.get_ui().table_property.setEnabled(enabled)
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

    @classmethod
    def search_for_parent(
        cls,
        pset_name,som_class:SOMcreator.SOMClass|None = None, allowed_ifc_psets:list[str] = None
    ) -> tuple[SOMcreator.SOMPropertySet,int]:
        """
        If a new PropertySet should be created this function checks if an existing Pset with the same name exists in a parent Class, the Predefined Psets or the IFC-Specification
        returns the parent pset and the mode 0-> No parent Found, 1-> Predefined Pset 2-> Parent Class 3-> IfcSchema
        param: ifc_mappings = allowed
        """
        return trigger.search_parent(pset_name,som_class,allowed_ifc_psets)

    @classmethod
    def remove_property_by_name(
        cls, property_set: SOMcreator.SOMPropertySet, property_name: str
    ):
        """
        checks if propertyset has property with given name. if so it will be removed
        """
        if property_set is None:
            return
        property = cls.get_property_by_name(property_set, property_name)
        if property is None:
            return
        property_set.remove_property(property, recursive=True)

    @classmethod
    def get_pset_name_suggestion(
        cls,
        som_class: SOMcreator.SOMClass,
        predefined_psets: set[SOMcreator.SOMPropertySet],
        ifc_version: ifc_schema.VERSION_TYPE,
    ) -> set[str]:
        possible_pset_names = set()
        possible_pset_names.update({p.name for p in predefined_psets})
        possible_pset_names.update(
            {p.name for p in cls.get_inheritable_property_sets(som_class)}
        )
        
        ifc_names = cls.get_ifc_names(som_class.ifc_mapping[ifc_version], ifc_version)
        possible_pset_names.update(ifc_names)
        existing_property_sets = [
            p.name for p in som_class.get_property_sets(filter=False)
        ]
        return possible_pset_names.difference(existing_property_sets)

    @classmethod
    def get_ifc_names(cls, class_ifc_mappings:list[str], ifc_version:ifc_schema.VERSION_TYPE):
        ifc_names = set()
        for mapping in class_ifc_mappings:
            ifc_names.update(
                    ifc_schema.get_property_sets_of_class(mapping, ifc_version)
                )
        return ifc_names

    @classmethod
    def is_name_in_parent_classes(
        cls, name: str, som_class: SOMcreator.SOMClass
    ) -> bool:
        return name in {p.name for p in cls.get_inheritable_property_sets(som_class)}

    @classmethod
    def get_parent_by_name(cls, name, som_class: SOMcreator.SOMClass):
        pset_dict = {p.name: p for p in cls.get_inheritable_property_sets(som_class)}
        return pset_dict.get(name)

    @classmethod
    def is_name_in_ifc_psets(
        cls,
        name: str,
        som_class: SOMcreator.SOMClass,
        ifc_version: ifc_schema.VERSION_TYPE,
    ):
        return name in cls.get_ifc_names( som_class.ifc_mapping[ifc_version], ifc_version)

    @classmethod
    def create_ifc_pset(cls, name: str, ifc_version: list[ifc_schema.VERSION_TYPE]):
        existing_properties = set()

        if not ifc_schema.is_property_set_existing_in_version(name, ifc_version):
            return None
        for property_name in ifc_schema.get_properties_by_pset_name(name, ifc_version):
            if property_name in {p.name for p in existing_properties}:
                continue
            property_name, description, datatype, values, unit = (
                ifc_schema.get_property_data(name, property_name, ifc_version)
            )
            prop = SOMcreator.SOMProperty(
                name=property_name,
                description=description,
                data_type=datatype,
                allowed_values=values,
                unit=unit,
            )
            existing_properties.add(prop)

        if not existing_properties:
            return None
        pset = SOMcreator.SOMPropertySet(name)
        [pset.add_property(p) for p in existing_properties]
        return pset
