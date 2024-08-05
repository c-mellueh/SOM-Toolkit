from __future__ import annotations
import som_gui.core.tool
import som_gui.module.predefined_property_set
import SOMcreator
from som_gui.module.project.constants import CLASS_REFERENCE
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
from som_gui import tool

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.predefined_property_set.prop import PredefinedPsetProperties
    from som_gui.module.predefined_property_set import ui


class PredefinedPropertySet(som_gui.core.tool.PredefinedPropertySet):

    @classmethod
    def get_properties(cls) -> PredefinedPsetProperties:
        return som_gui.PredefinedPsetProperties

    @classmethod
    def get_window(cls) -> ui.PredefinedPropertySetWindow:
        return cls.get_properties().predefined_property_set_window

    @classmethod
    def set_window(cls, window):
        props = cls.get_properties()
        props.predefined_property_set_window = window

    @classmethod
    def connect_triggers(cls, window):
        som_gui.module.predefined_property_set.trigger.connect_dialog(window)

    @classmethod
    def create_window(cls) -> ui.PredefinedPropertySetWindow:
        window = som_gui.module.predefined_property_set.ui.PredefinedPropertySetWindow()
        cls.set_window(window)
        return cls.get_window()

    @classmethod
    def close_window(cls):
        window = cls.get_window()
        window.hide()

    @classmethod
    def get_object_table_widget(cls) -> QTableWidget:
        return cls.get_window().widget.table_widgets_objects

    @classmethod
    def get_pset_list_widget(cls):
        return cls.get_window().widget.list_view_pset

    @classmethod
    def update_pset_widget(cls):
        list_widget = cls.get_pset_list_widget()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            item.setText(item.data(CLASS_REFERENCE).name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    @classmethod
    def update_object_widget(cls):
        table_widget = cls.get_object_table_widget()
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, 0)
            property_set: SOMcreator.PropertySet = tool.PropertySet.get_property_set_from_item(item)
            item.setText(f"{property_set.object.name}")
            table_widget.item(row, 1).setText(f"{property_set.object.ident_value}")

    @classmethod
    def get_selected_property_set(cls):
        props = cls.get_properties()
        return props.predefined_property_set_window.widget.list_view_pset.selectedItems()[0].data(CLASS_REFERENCE)

    @classmethod
    def set_active_property_set(cls, property_set: SOMcreator.PropertySet):
        props = cls.get_properties()
        props.active_predefined_pset = property_set

    @classmethod
    def get_active_property_set(cls) -> SOMcreator.PropertySet:
        props = cls.get_properties()
        return props.active_predefined_pset

    @classmethod
    def is_edit_mode_active(cls):
        props = cls.get_properties()
        return props.is_renaming_predefined_pset

    @classmethod
    def remove_property_sets_from_list_widget(cls, property_sets: list[SOMcreator.PropertySet],
                                              list_widget: QListWidget):
        rows = {row for row in range(list_widget.count()) if
                list_widget.item(row).data(CLASS_REFERENCE) in property_sets}
        for row in reversed(sorted(rows)):
            list_widget.takeItem(row)

    @classmethod
    def remove_property_sets_from_table_widget(cls, property_sets: list[SOMcreator.PropertySet],
                                               table_widget: QTableWidget):
        remove_rows = set()
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, 0)
            if tool.PropertySet.get_property_set_from_item(item) in property_sets:
                remove_rows.add(row)
        for row in reversed(sorted(remove_rows)):
            table_widget.removeRow(row)

    @classmethod
    def add_property_sets_to_widget(cls, property_sets: list[SOMcreator.PropertySet], list_widget: QListWidget):
        list_widget.setSortingEnabled(False)

        for property_set in property_sets:
            item = QListWidgetItem(property_set.name)
            item.setData(CLASS_REFERENCE, property_set)
            list_widget.addItem(item)
        list_widget.setSortingEnabled(True)

    @classmethod
    def add_objects_to_table_widget(cls, property_sets: list[SOMcreator.PropertySet], table_widget: QTableWidget):
        for property_set in property_sets:
            row_count = table_widget.rowCount()
            table_widget.setRowCount(row_count + 1)
            obj = property_set.object

            item_1 = QTableWidgetItem(obj.name)
            item_2 = QTableWidgetItem(obj.ident_value)

            item_1.setData(CLASS_REFERENCE, property_set)
            item_2.setData(CLASS_REFERENCE, property_set)

            table_widget.setItem(row_count, 0, item_1)
            table_widget.setItem(row_count, 1, item_2)

    @classmethod
    def get_existing_psets_in_list_widget(cls, pset_list: QListWidget):
        return {pset_list.item(row).data(CLASS_REFERENCE) for row in range(pset_list.count())}

    @classmethod
    def get_existing_psets_in_table_widget(cls, object_table: QTableWidget):
        psets = set()
        for row in range(object_table.rowCount()):
            item = object_table.item(row, 0)
            psets.add(tool.PropertySet.get_property_set_from_item(item))
        return psets

    @classmethod
    def delete_selected_property_set(cls):
        property_set = cls.get_active_property_set()
        property_set.delete(False, False)

    @classmethod
    def rename_selected_property_set(cls):
        pset = cls.get_active_property_set()
        list_widget = cls.get_pset_list_widget()
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            if tool.PropertySet.get_property_set_from_item(item) == pset:
                list_widget.editItem(item)

    @classmethod
    def create_property_set(cls):
        existing_names = [p.name for p in cls.get_property_sets()]
        tool.PropertySet.create_property_set(
            tool.Util.get_new_name("Neues PropertySet", existing_names))

    @classmethod
    def get_property_sets(cls) -> set[SOMcreator.PropertySet]:
        """
        get all Predefined PropertySets
        """
        proj = tool.Project.get()
        return proj.get_predefined_psets()

    @classmethod
    def get_selected_linked_psets(cls) -> set[SOMcreator.PropertySet]:
        return {tool.PropertySet.get_property_set_from_item(item) for item in
                cls.get_object_table_widget().selectedItems()}

    @classmethod
    def delete_selected_objects(cls):
        property_sets = cls.get_selected_linked_psets()
        for property_set in property_sets:
            property_set.delete(override_ident_deletion=False)

    @classmethod
    def remove_selected_links(cls):
        property_sets = cls.get_selected_linked_psets()
        parent = cls.get_active_property_set()
        for property_set in property_sets:
            parent.remove_child(property_set)

    @classmethod
    def clear_object_table(cls):
        table = cls.get_object_table_widget()
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)
