from __future__ import annotations

from PySide6.QtWidgets import QTableWidgetItem, QCompleter, QTableWidget, QListWidget, QListWidgetItem, QMenu
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QAction, QIcon

from SOMcreator.constants.json_constants import INHERITED_TEXT

import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.icons import get_link_icon
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.property_set import trigger as property_set_trigger

import SOMcreator

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from som_gui.module.property_set.prop import PropertySetProperties
    from som_gui.module.predefined_property_set.ui import PredefinedPropertySetWindow


class PropertySet(som_gui.core.tool.PropertySet):

    @classmethod
    def get_attribute_by_name(cls, property_set: SOMcreator.PropertySet, name: str):
        attribute_dict = {a.name: a for a in property_set.get_all_attributes()}
        return attribute_dict[name]

    @classmethod
    def get_inheritable_property_sets(cls, obj: SOMcreator.Object) -> list[SOMcreator.PropertySet]:
        def loop(o):
            psets = o.property_sets
            if o.parent:
                psets += loop(o.parent)
            return psets

        return loop(obj)

    @classmethod
    def get_pset_from_index(cls, index: QModelIndex) -> SOMcreator.PropertySet:
        return index.data(CLASS_REFERENCE)

    @classmethod
    def pset_table_is_editing(cls):
        props = cls.get_pset_properties()
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
        property_set.delete()

    @classmethod
    def delete_predefined_pset(cls):
        property_set = cls.get_active_predefined_pset()
        property_set.delete(False, False)

    @classmethod
    def rename_predefined_pset(cls):
        pset = cls.get_active_predefined_pset()
        list_widget = cls.get_predefine_pset_list_widget()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            if cls.get_property_set_from_item(item) == pset:
                list_widget.editItem(item)

    @classmethod
    def add_predefined_pset(cls):
        existing_names = [p.name for p in cls.get_predefined_psets()]
        cls.create_property_set(tool.ObjectFilter.get_new_use_case_name("Neues PropertySet", existing_names))

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
    def close_predefined_pset_window(cls):
        window = cls.get_pset_properties().predefined_property_set_window
        window.hide()

    @classmethod
    def get_property_set_from_item(cls, item: QTableWidgetItem | QListWidgetItem) -> SOMcreator.PropertySet:
        return item.data(CLASS_REFERENCE)

    @classmethod
    def get_selected_predef_property_set(cls):
        props = cls.get_pset_properties()
        return props.predefined_property_set_window.widget.list_view_pset.selectedItems()[0].data(CLASS_REFERENCE)

    @classmethod
    def set_predef_property_set(cls, property_set: SOMcreator.PropertySet):
        props = cls.get_pset_properties()
        props.active_predefined_pset = property_set

    @classmethod
    def get_active_predefined_pset(cls) -> SOMcreator.PropertySet:
        props = cls.get_pset_properties()
        return props.active_predefined_pset

    @classmethod
    def get_predefined_pset_window(cls):
        props = cls.get_pset_properties()
        return props.predefined_property_set_window

    @classmethod
    def create_predefined_pset_window(cls) -> PredefinedPropertySetWindow:
        props = cls.get_pset_properties()
        window = som_gui.module.property_set.ui.PredefinedPropertySetWindow()
        props.predefined_property_set_window = window
        window.edit_started.connect(cls.predef_edit_started)
        window.edit_stopped.connect(cls.predef_edit_stopped)
        return props.predefined_property_set_window

    @classmethod
    def predefined_pset_list_is_editing(cls):
        props = cls.get_pset_properties()
        return props.is_renaming_predefined_pset

    @classmethod
    def predef_edit_started(cls):
        props = cls.get_pset_properties()
        props.is_renaming_predefined_pset = True

    @classmethod
    def predef_edit_stopped(cls):
        props = cls.get_pset_properties()
        props.is_renaming_predefined_pset = False

    @classmethod
    def remove_property_sets_from_list(cls, property_sets: list[SOMcreator.PropertySet], list_widget: QListWidget):
        rows = {row for row in range(list_widget.count()) if
                list_widget.item(row).data(CLASS_REFERENCE) in property_sets}
        for row in reversed(sorted(rows)):
            list_widget.takeItem(row)

    @classmethod
    def add_property_sets_to_list(cls, property_sets: list[SOMcreator.PropertySet], list_widget: QListWidget):
        list_widget.setSortingEnabled(False)

        for property_set in property_sets:
            item = QListWidgetItem(property_set.name)
            item.setData(CLASS_REFERENCE, property_set)
            list_widget.addItem(item)
        list_widget.setSortingEnabled(True)

    @classmethod
    def add_property_sets_to_inheritance_list(cls, property_sets: list[SOMcreator.PropertySet],
                                              list_widget: QListWidget):
        list_widget.setSortingEnabled(False)
        for property_set in property_sets:
            item = QListWidgetItem(property_set.object.name)
            item.setData(CLASS_REFERENCE, property_set)
            list_widget.addItem(item)
        list_widget.setSortingEnabled(True)

    @classmethod
    def get_existing_psets_in_list(cls, pset_list: QListWidget):
        return {pset_list.item(row).data(CLASS_REFERENCE) for row in range(pset_list.count())}

    @classmethod
    def get_predefine_pset_list_widget(cls):
        return cls.get_pset_properties().predefined_property_set_window.widget.list_view_pset

    @classmethod
    def get_predefined_pset_inheritance_list(cls):
        return cls.get_pset_properties().predefined_property_set_window.widget.list_view_existance

    @classmethod
    def update_predefined_pset_list(cls):
        list_widget = cls.get_predefine_pset_list_widget()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            item.setText(item.data(CLASS_REFERENCE).name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    @classmethod
    def update_predefined_pset_inheritance_list(cls):
        list_widget = cls.get_predefined_pset_inheritance_list()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            property_set: SOMcreator.PropertySet = item.data(CLASS_REFERENCE)
            item.setText(f"{property_set.object.name}")

    @classmethod
    def check_if_pset_allready_exists(cls, pset_name: str, active_object: SOMcreator.Object):
        return bool(pset_name in {p.name for p in active_object.get_all_property_sets()})

    @classmethod
    def create_property_set(cls, name: str, obj: SOMcreator.Object | None = None,
                            parent: SOMcreator.PropertySet | None = None) -> SOMcreator.PropertySet | None:

        if obj:
            if name in {p.name for p in obj.property_sets}:
                tool.Popups.create_warning_popup(f"PropertySet existiert bereits")
                return None
        if parent is not None:
            property_set = parent.create_child(name)
            obj.add_property_set(property_set)
        else:
            property_set = SOMcreator.PropertySet(name, obj, project=tool.Project.get())
        return property_set

    @classmethod
    def get_pset_from_item(cls, item: QTableWidgetItem) -> SOMcreator.PropertySet:
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
    def get_property_sets(cls) -> set[SOMcreator.PropertySet]:
        active_object = tool.Object.get_active_object()
        if active_object is None:
            return set()
        return set(active_object.property_sets)

    @classmethod
    def get_table(cls):
        return som_gui.MainUi.ui.table_pset

    @classmethod
    def get_row_from_pset(cls, property_set: SOMcreator.PropertySet):
        table = cls.get_table()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_pset_from_item(item) == property_set:
                return row

    @classmethod
    def remove_property_sets_from_table(cls, property_sets: set[SOMcreator.PropertySet], table: QTableWidget):
        rows = sorted(cls.get_row_from_pset(p) for p in property_sets)
        for row in reversed(rows):
            table.removeRow(row)

    @classmethod
    def add_property_sets_to_table(cls, property_sets: set[SOMcreator.PropertySet], table: QTableWidget):
        table.setSortingEnabled(False)
        for property_set in property_sets:
            items = [QTableWidgetItem() for _ in range(3)]
            row = table.rowCount()
            table.setRowCount(row + 1)
            [item.setData(CLASS_REFERENCE, property_set) for item in items]
            [item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable) for item in items]
            [table.setItem(row, col, item) for col, item in enumerate(items)]
        table.setSortingEnabled(True)

    @classmethod
    def update_property_set_table(cls, table: QTableWidget):
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            items = [table.item(row, col) for col in range(table.columnCount())]
            property_set = cls.get_property_set_from_item(item)
            check_state = Qt.CheckState.Checked if property_set.optional else Qt.CheckState.Unchecked
            items[0].setText(f"{property_set.name}")
            if property_set.is_child:
                text = property_set.parent.name if property_set.parent.object is not None else INHERITED_TEXT
                items[1].setText(text)
                items[0].setIcon(get_link_icon())
            else:
                items[0].setIcon(QIcon())
                items[1].setText("")
            items[2].setCheckState(check_state)

    @classmethod
    def get_predefined_psets(cls) -> set[SOMcreator.PropertySet]:
        proj = tool.Project.get()
        return proj.get_predefined_psets()

    @classmethod
    def select_property_set(cls, property_set: SOMcreator.PropertySet):
        table = cls.get_table()
        table.setFocus()
        for row in range(table.rowCount()):
            if cls.get_pset_from_item(table.item(row, 0)) == property_set:
                table.selectRow(row)
                table.setCurrentCell(row, 0)

    @classmethod
    def get_selecte_property_set_from_table(cls) -> SOMcreator.PropertySet | None:
        table = cls.get_table()
        items = table.selectedItems()
        if not items:
            return
        item = items[0]
        return cls.get_pset_from_item(item)

    @classmethod
    def update_completer(cls, obj: SOMcreator.Object = None):
        psets = list(cls.get_predefined_psets())
        if obj is not None:
            psets += cls.get_inheritable_property_sets(obj)
        pset_names = sorted({p.name for p in psets})
        completer = QCompleter(pset_names)
        som_gui.MainUi.ui.lineEdit_ident_pSet.setCompleter(completer)
        som_gui.MainUi.ui.lineEdit_pSet_name.setCompleter(completer)

    @classmethod
    def set_enabled(cls, enabled: bool):
        layout = som_gui.MainUi.ui.box_layout_pset
        layout.setEnabled(enabled)

    @classmethod
    def get_pset_properties(cls) -> PropertySetProperties:
        return som_gui.PropertySetProperties

    @classmethod
    def set_active_property_set(cls, property_set: SOMcreator.PropertySet):
        prop = cls.get_pset_properties()
        prop.active_pset = property_set

    @classmethod
    def get_active_property_set(cls) -> SOMcreator.PropertySet:
        prop = cls.get_pset_properties()
        return prop.active_pset
