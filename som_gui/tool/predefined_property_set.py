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
    from som_gui.module.predefined_property_set.prop import PredefinedPsetProperties, PredefinedPsetCompareProperties
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


class PredefinedPropertySetCompare(som_gui.core.tool.PredefinedPropertySetCompare):

    @classmethod
    def get_properties(cls) -> PredefinedPsetCompareProperties:
        return som_gui.PredefinedPsetCompareProperties

    @classmethod
    def reset(cls):
        cls.get_properties().widget = None
        cls.get_properties().predefined_psets = None
        cls.get_properties().pset_lists = list()
        cls.get_properties().value_dict = dict()

    @classmethod
    def create_pset_list(cls):
        psets0, psets1 = cls.get_predefined_psets(0), cls.get_predefined_psets(1)
        uuid_dict = tool.AttributeCompare.generate_uuid_dict(psets1)
        name_dict = tool.AttributeCompare.generate_name_dict(psets1)
        pset_list = list()
        missing = list(psets1)
        for pset in psets0:
            match = tool.AttributeCompare.find_matching_entity(pset, uuid_dict, name_dict)
            if match:
                pset_list.append((pset, match))
                missing.remove(match)
            else:
                pset_list.append((pset, None))
        for pset in missing:
            pset_list.append((None, pset))
        cls.set_pset_lists(pset_list)
        return pset_list

    @classmethod
    def create_tree_selection_trigger(cls, widget: ui.CompareWidget):
        widget.widget.tree_widget_propertysets.itemSelectionChanged.connect(
            lambda: som_gui.module.predefined_property_set.trigger.compare_psetselection_changed(widget))

    @classmethod
    def create_value_dict(cls, pset_list: list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]]):
        value_dict = dict()
        for pset0, pset1 in pset_list:
            if pset0 is None:
                value_dict[pset1] = [(None, p) for p in pset1.get_all_attributes()]
                continue
            if pset1 is None:
                value_dict[pset0] = [(p, None) for p in pset0.get_all_attributes()]
                continue
            children0 = pset0.get_all_children()
            children1 = pset1.get_all_children()
            missing = list(children1)
            uuid_dict = tool.AttributeCompare.generate_uuid_dict(children1)
            result_list = list()
            for pset in children0:
                match = tool.AttributeCompare.find_matching_entity(pset, uuid_dict, [])
                if match is not None:
                    print(match)
                    missing.remove(match)
                result_list.append((pset, match))
            for pset in missing:
                result_list.append((None, pset))
            value_dict[pset0] = result_list
            value_dict[pset1] = result_list
        cls.get_properties().value_dict = value_dict

    @classmethod
    def fill_pset_info(cls):
        pset_tree = tool.AttributeCompare.get_pset_tree(cls.get_widget())
        item = tool.AttributeCompare.get_selected_item(pset_tree)
        table = cls.get_info_table(cls.get_widget())

        pset0, pset1 = tool.AttributeCompare.get_entities_from_item(item)

        item0 = QTableWidgetItem()
        item0.setData(Qt.ItemDataRole.EditRole, len(list(pset0.children)))
        item1 = QTableWidgetItem()
        item1.setData(Qt.ItemDataRole.EditRole, len(list(pset1.children)))

        table.insertRow(table.rowCount())
        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem("Child Count"))
        table.setItem(table.rowCount() - 1, 1, item0)
        table.setItem(table.rowCount() - 1, 2, item1)

    @classmethod
    def fill_attribute_info(cls):
        pset_tree = tool.AttributeCompare.get_pset_tree(cls.get_widget())
        item = tool.AttributeCompare.get_selected_item(pset_tree)
        table = cls.get_info_table(cls.get_widget())
        attributes = tool.AttributeCompare.get_entities_from_item(item)
        info_list = list()
        info_list.append(("Vererbt Werte", lambda a: getattr(a, "child_inherits_values")))
        info_list.append(("Datentyp", lambda a: getattr(a, "data_type")))
        info_list.append(("Werttyp", lambda a: getattr(a, "value_type")))

        for text, getter_func in info_list:
            table.insertRow(table.rowCount())
            table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(text))
            for index, attrib in enumerate(attributes):
                item = QTableWidgetItem()
                item.setData(Qt.ItemDataRole.EditRole, getter_func(attrib))
                table.setItem(table.rowCount() - 1, 1 + index, item)

    @classmethod
    def fill_value_table_pset(cls):
        pset_tree = tool.AttributeCompare.get_pset_tree(cls.get_widget())
        item = tool.AttributeCompare.get_selected_item(pset_tree)
        table = tool.AttributeCompare.get_value_table(cls.get_widget())
        tool.AttributeCompare.clear_table(table)
        pset0, pset1 = tool.AttributeCompare.get_entities_from_item(item)
        for property_sets in cls.get_value_list(pset0 or pset1):
            table.insertRow(table.rowCount())
            for index, p in enumerate(property_sets):
                item = QTableWidgetItem(p.object.name if p else "")
                table.setItem(table.rowCount() - 1, index, item)



    @classmethod
    def get_widget(cls):
        if cls.get_properties().widget is None:
            cls.get_properties().widget = som_gui.module.predefined_property_set.ui.CompareWidget()
        return cls.get_properties().widget

    @classmethod
    def set_predefined_psets(cls, psets0, psets1):
        cls.get_properties().predefined_psets = (psets0, psets1)

    @classmethod
    def get_predefined_psets(cls, index: int) -> set[SOMcreator.PropertySet]:
        return cls.get_properties().predefined_psets[index]

    @classmethod
    def set_pset_lists(cls, list: list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]]) -> None:
        cls.get_properties().pset_lists = list

    @classmethod
    def get_pset_lists(cls) -> list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]]:
        return cls.get_properties().pset_lists

    @classmethod
    def get_info_table(cls, widget: ui.CompareWidget):
        return widget.widget.table_infos

    @classmethod
    def get_value_list(cls, pset: SOMcreator.PropertySet) -> list[tuple[SOMcreator.PropertySet]]:
        return cls.get_properties().value_dict.get(pset)
