from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, TextIO, Any
from PySide6.QtGui import QBrush, QPalette, QColor, QIcon
from PySide6.QtCore import QModelIndex, Qt
from som_gui import tool
import SOMcreator
from som_gui.module.attribute import ui
import som_gui.core.tool
import som_gui
from PySide6.QtWidgets import QTableWidgetItem, QTreeWidgetItem, QTreeWidget, QTableWidget
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.compare import trigger

DELETE_TEXT = "was deleted."
ADD_TEXT = "was added."
RENAME_TEXT = "was renamed to"
CHANGED_FROM = "was changed from"
ADD_CHILD = "added child"
REMOVE_CHILD = "removed child"
style_list = [
    [None, [0, 1]],
    ["#897e00", [0, 1]],  # Yellow
    ["#006605", [1]],  # green
    ["#840002", [0]]  # red
]



if TYPE_CHECKING:
    from som_gui.module.attribute.prop import AttributeProperties, CompareAttributesProperties

class Attribute(som_gui.core.tool.Attribute):
    @classmethod
    def set_inherit_state(cls, state: bool, attribute: SOMcreator.Attribute):
        attribute.child_inherits_values = state

    @classmethod
    def get_inherit_state(cls, attribute: SOMcreator.Attribute):
        return attribute.child_inherits_values

    @classmethod
    def delete(cls, attributes: set[SOMcreator.Attribute], with_subattributes=False):
        for attribute in attributes:
            attribute.delete(with_subattributes)

    @classmethod
    def add_attribute_data_value(cls, name: str, getter: Callable, setter: Callable):
        prop = cls.get_attribute_properties()
        prop.attribute_data_dict[name] = {"getter": getter,
                                          "setter": setter}

    @classmethod
    def get_attribute_data(cls, attribute: SOMcreator.Attribute) -> dict[str, Any]:
        prop = cls.get_attribute_properties()
        d = dict()
        for name, data_dict in prop.attribute_data_dict.items():
            value = data_dict["getter"](attribute)
            d[name] = value
        return d

    @classmethod
    def set_attribute_data(cls, attribute: SOMcreator, data_dict: dict[str, str | list]):
        prop = cls.get_attribute_properties()
        for name, value in data_dict.items():
            d = prop.attribute_data_dict.get(name)
            if not d:
                logging.warning(f"data {name} not found")
                continue
            d["setter"](value, attribute)

    @classmethod
    def get_attribute_name(cls, attribute: SOMcreator.Attribute):
        return attribute.name

    @classmethod
    def set_attribute_name(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.name = value

    @classmethod
    def get_attribute_data_type(cls, attribute: SOMcreator.Attribute):
        return attribute.data_type

    @classmethod
    def set_attribute_data_type(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.data_type = value

    @classmethod
    def get_attribute_value_type(cls, attribute: SOMcreator.Attribute):
        return attribute.value_type

    @classmethod
    def set_attribute_value_type(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.value_type = value

    @classmethod
    def get_attribute_values(cls, attribute: SOMcreator.Attribute):
        return attribute.value

    @classmethod
    def set_attribute_values(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.value = value

    @classmethod
    def get_attribute_description(cls, attribute: SOMcreator.Attribute):
        return attribute.description

    @classmethod
    def set_attribute_description(cls, value: str, attribute: SOMcreator.Attribute):
        attribute.description = value

    @classmethod
    def is_attribute_optional(cls, attribute: SOMcreator.Attribute):
        return attribute.optional

    @classmethod
    def set_attribute_optional(cls, optional: bool, attribute: SOMcreator.Attribute):
        attribute.optional = optional

    @classmethod
    def get_attribute_properties(cls) -> AttributeProperties:
        return som_gui.AttributeProperties

    @classmethod
    def create_attribute(cls, property_set: SOMcreator.PropertySet, attribute_data: dict[str, str | list | bool]):
        name = attribute_data["name"]
        if not name:
            return
        values = attribute_data["values"]
        value_type = attribute_data["value_type"]
        inherit = attribute_data["inherit_value"]
        attribute = SOMcreator.Attribute(property_set, name, values, value_type, child_inherits_values=inherit)
        cls.set_attribute_data(attribute, attribute_data)
        return attribute


class AttributeCompare(som_gui.core.tool.AttributeCompare):
    @classmethod
    def get_properties(cls) -> CompareAttributesProperties:
        return som_gui.CompareAttributesProperties

    @classmethod
    def reset(cls):
        prop = cls.get_properties()
        prop.projects = [None, None]
        prop.uuid_dicts = [None, None]
        prop.ident_dicts = [None, None]
        prop.object_dict = dict()
        prop.object_lists = list()
        prop.missing_objects = [None, None]
        prop.object_tree_item_dict = dict()
        prop.pset_lists = dict()
        prop.attributes_lists = dict()
        prop.values_lists = dict()
        prop.widget = None

    @classmethod
    def create_tree_selection_trigger(cls, widget: ui.AttributeWidget):
        widget.widget.tree_widget_object.itemSelectionChanged.connect(
            lambda: trigger.object_tree_selection_changed(widget))
        widget.widget.tree_widget_propertysets.itemSelectionChanged.connect(
            lambda: trigger.pset_tree_selection_changed(widget))

    @classmethod
    def find_matching_object(cls, obj: SOMcreator.Object, index=1) -> SOMcreator.Object | None:
        uuid_dict = cls.get_uuid_dict(index)
        ident_dict = cls.get_ident_dict(index)
        uuid_match = uuid_dict.get(obj.uuid)
        if uuid_match:
            return uuid_match
        ident_match = ident_dict.get(obj.ident_value)

        if ident_match:
            return ident_match
        return None

    @classmethod
    def find_matching_entity(cls, entity_0, uuid_dict1,
                             name_dict1) -> SOMcreator.PropertySet | SOMcreator.Attribute | None:
        if entity_0.uuid in uuid_dict1:
            return uuid_dict1[entity_0.uuid]
        if entity_0.name in name_dict1:
            return name_dict1[entity_0.name]
        return None

    @classmethod
    def generate_uuid_dict(cls, entity_list):
        return {p.uuid: p for p in entity_list}

    @classmethod
    def generate_name_dict(cls, entity_list):
        return {p.name: p for p in entity_list}

    @classmethod
    def compare_objects(cls, obj0: None | SOMcreator.Object, obj1: None | SOMcreator.Object):
        property_set_uuid_dict1 = cls.generate_uuid_dict(obj1.get_all_property_sets()) if obj1 is not None else dict()
        property_set_name_dict1 = cls.generate_name_dict(obj1.get_all_property_sets()) if obj1 is not None else dict()
        pset_list = list()

        missing_property_sets1 = list(obj1.get_all_property_sets()) if obj1 is not None else []
        if obj0 is not None:
            for property_set0 in obj0.get_all_property_sets():
                match = cls.find_matching_entity(property_set0, property_set_uuid_dict1, property_set_name_dict1)
                if match is not None:
                    missing_property_sets1.remove(match)
                cls.compare_property_sets(property_set0, match)
                pset_list.append((property_set0, match))

        for property_set1 in missing_property_sets1:
            pset_list.append((None, property_set1))
        if obj0 is not None:
            cls.set_pset_list(obj0, pset_list)
        if obj1 is not None:
            cls.set_pset_list(obj1, pset_list)

    @classmethod
    def compare_property_sets(cls, pset0: SOMcreator.PropertySet, pset1: SOMcreator.PropertySet):
        result_list = tool.AttributeCompare.create_child_matchup(pset0, pset1)
        if pset0 is not None:
            cls.set_value_list(pset0, result_list)
        if pset1 is not None:
            cls.set_value_list(pset1, result_list)

        if None in (pset0, pset1):
            return
        attribute_uuid_dict1 = cls.generate_uuid_dict(pset1.get_all_attributes())
        attribute_name_dict1 = cls.generate_name_dict(pset1.get_all_attributes())
        missing_attributes1 = list(pset1.get_all_attributes())
        attributes_list = list()

        for attribute0 in pset0.get_all_attributes():
            match = cls.find_matching_entity(attribute0, attribute_uuid_dict1, attribute_name_dict1)
            if match is not None:
                missing_attributes1.remove(match)
                attributes_list.append((attribute0, match))
            else:
                attributes_list.append((attribute0, None))

        for attribute1 in missing_attributes1:
            attributes_list.append((None, attribute1))

        for a1, a2 in attributes_list:
            cls.compare_attributes(a1, a2)
        cls.set_attribute_list(pset0, attributes_list)
        cls.set_attribute_list(pset1, attributes_list)

    @classmethod
    def compare_attributes(cls, attribute0: SOMcreator.Attribute, attribute1: SOMcreator.Attribute):
        values0 = set(attribute0.get_own_values()) if attribute0 is not None else set()
        values1 = set(attribute1.get_own_values()) if attribute1 is not None else set()

        unique0 = values0.difference(values1)
        main = values0.intersection(values1)
        unique1 = values1.difference(values0)

        value_list = [(v, v) for v in main] + [(v, None) for v in unique0] + [(None, v) for v in unique1]
        if attribute0 is not None:
            cls.set_value_list(attribute0, value_list)
        if attribute1 is not None:
            cls.set_value_list(attribute1, value_list)

    @classmethod
    def create_object_lists(cls) -> None:
        object_list = cls.get_object_lists()
        if object_list:
            return
        project_0, project_1 = cls.get_project(0), cls.get_project(1)
        found_objects = list()
        for obj0 in project_0.get_objects(filter=False):
            match = cls.find_matching_object(obj0, 1)
            if match is None:
                object_list.append((obj0, None))
                cls.compare_objects(obj0, None)
            else:
                object_list.append((obj0, match))
                found_objects.append(match)
                cls.compare_objects(obj0, match)

        for obj1 in [o for o in project_1.get_objects(filter=False) if o not in found_objects]:
            object_list.append((None, obj1))
            cls.compare_objects(None, obj1)

        cls.create_object_dicts()

    @classmethod
    def create_object_dicts(cls) -> None:
        od = dict()
        for o0, o1 in cls.get_object_lists():
            if o0 is not None:
                od[o0] = o1
            if o1 is not None:
                od[o1] = o1
        cls.get_properties().object_dict = od

    @classmethod
    def add_object_to_item(cls, obj: SOMcreator.Object, item: QTreeWidgetItem, index: int):
        start_index = index
        ident_text = f"({obj.ident_value})" if obj.ident_value else ""
        text = f"{obj.name} {ident_text}"
        item.setText(start_index, text)
        item.setData(start_index, CLASS_REFERENCE, obj)
        cls.set_object_item_relation(obj, item)

    @classmethod
    def fill_object_tree_layer(cls, objects: list[SOMcreator.Object], parent_item: QTreeWidgetItem, add_missing: bool):
        object_dict = cls.get_object_dict()

        for obj in objects:
            match_obj = object_dict.get(obj)
            item = QTreeWidgetItem()
            cls.add_object_to_item(obj, item, 0)
            if match_obj:
                cls.add_object_to_item(match_obj, item, 1)

            if match_obj is not None or add_missing:
                parent_item.addChild(item)
            cls.fill_object_tree_layer(list(obj.get_all_children()), item, add_missing)

    @classmethod
    def fill_object_tree(cls, tree: QTreeWidget, add_missing: bool = True):
        proj0, proj1 = cls.get_project(0), cls.get_project(1)
        tree_root = tree.invisibleRootItem()
        root_objects = tool.Project.get_root_objects(False, proj0)
        cls.fill_object_tree_layer(root_objects, tree_root, add_missing)
        if add_missing:
            cls.add_missing_objects_to_tree(tree, tool.Project.get_root_objects(False, proj1))

    @classmethod
    def fill_value_table_pset(cls, widget: ui.AttributeWidget):
        pset_tree = cls.get_pset_tree(widget)
        item = cls.get_selected_item(pset_tree)
        table = cls.get_value_table(widget)
        cls.clear_table(table)
        pset0, pset1 = cls.get_entities_from_item(item)
        for property_sets in cls.get_value_list(pset0 or pset1):
            table.insertRow(table.rowCount())
            for index, p in enumerate(property_sets):
                item = QTableWidgetItem(p.object.name if p else "")
                table.setItem(table.rowCount() - 1, index, item)

    @classmethod
    def fill_table(cls, table: QTableWidget, info_list, entities):
        for text, getter_func in info_list:
            table.insertRow(table.rowCount())
            table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(text))
            for index, entity in enumerate(entities):
                item = QTableWidgetItem()
                text = getter_func(entity) if entity is not None else ""

                item.setData(Qt.ItemDataRole.EditRole, text)
                table.setItem(table.rowCount() - 1, 1 + index, item)

    @classmethod
    def get_pset_info_list(cls):
        info_list = list()
        info_list.append(("Name", lambda p: getattr(p, "name")))
        info_list.append(("Child Count", lambda p: len(list(p.children)) if p else ""))
        return info_list

    @classmethod
    def get_attribute_info_list(cls):
        info_list = list()
        info_list.append(("Name", lambda a: getattr(a, "name")))
        info_list.append(("Vererbt Werte", lambda a: getattr(a, "child_inherits_values")))
        info_list.append(("Datentyp", lambda a: getattr(a, "data_type")))
        info_list.append(("Werttyp", lambda a: getattr(a, "value_type")))
        return info_list

    @classmethod
    def find_existing_parent_item(cls, obj: SOMcreator.Object) -> QTreeWidgetItem | None:
        parent = obj.parent
        while parent is not None:
            parent_item = cls.get_item_from_object(parent)
            if parent_item is not None:
                return parent_item
            parent = parent.parent
        return None

    @classmethod
    def add_missing_objects_to_tree(cls, tree: QTreeWidget, root_objects: list[SOMcreator.Object]):
        missing_objects = cls.get_missing_objects(1)
        for obj in root_objects:
            if obj in missing_objects:
                parent = cls.find_existing_parent_item(obj)
                parent = parent if parent is not None else tree.invisibleRootItem()
                item = QTreeWidgetItem()
                cls.add_object_to_item(obj, item, 1)
                parent.addChild(item)
            cls.add_missing_objects_to_tree(tree, list(obj.get_all_children()))

    @classmethod
    def clear_tree(cls, tree: QTreeWidget):
        root = tree.invisibleRootItem()
        for child_index in reversed(range(root.childCount())):
            root.removeChild(root.child(child_index))

    @classmethod
    def clear_table(cls, table: QTableWidget):
        table.setRowCount(0)

    @classmethod
    def fill_pset_tree(cls, tree: QTreeWidget, pset_list: list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]],
                       add_missing: bool = True) -> None:
        cls.clear_tree(tree)
        if pset_list is None:
            return
        for pset0, pset1 in pset_list:
            item = QTreeWidgetItem()
            if pset0:
                item.setText(0, pset0.name)
                item.setData(0, CLASS_REFERENCE, pset0)
            if pset1:
                item.setText(1, pset1.name)
                item.setData(1, CLASS_REFERENCE, pset1)
            if (pset0 and pset1) or add_missing:
                tree.invisibleRootItem().addChild(item)

    @classmethod
    def add_attributes_to_pset_tree(cls, tree: QTreeWidget, add_missing: bool):
        root = tree.invisibleRootItem()
        for index in range(root.childCount()):
            item = root.child(index)
            pset0, pset1 = cls.get_entities_from_item(item)
            attribute_list = cls.get_attribute_list(pset0) or cls.get_attribute_list(pset1)
            if attribute_list is None:
                return
            for attribute0, attribute1 in attribute_list:
                attribute_item = QTreeWidgetItem()
                if attribute0 is not None:
                    attribute_item.setText(0, attribute0.name)
                    attribute_item.setData(0, CLASS_REFERENCE, attribute0)
                if attribute1 is not None:
                    attribute_item.setText(1, attribute1.name)
                    attribute_item.setData(1, CLASS_REFERENCE, attribute1)

                if (attribute0 and attribute1) or add_missing:
                    item.addChild(attribute_item)

    @classmethod
    def fill_value_table(cls, table: QTableWidget, attribute: SOMcreator.Attribute):
        cls.clear_table(table)
        if attribute is None:
            return
        if cls.get_value_list(attribute) is None:
            return

        for value0, value1 in cls.get_value_list(attribute):
            item0 = QTableWidgetItem()
            item1 = QTableWidgetItem()

            if value0 is not None:
                item0.setText(value0)

            if value1 is not None:
                item1.setText(value1)

            table.insertRow(table.rowCount())
            table.setItem(table.rowCount() - 1, 0, item0)
            table.setItem(table.rowCount() - 1, 1, item1)

    @classmethod
    def create_child_matchup(cls, entity0, entity1):
        if entity0 is None:
            return [(None, p) for p in entity1.get_all_children()]
        if entity1 is None:
            return [(p, None) for p in entity0.get_all_children()]
        children0 = entity0.get_all_children()
        children1 = entity1.get_all_children()
        missing = list(children1)
        uuid_dict = cls.generate_uuid_dict(children1)
        name_dict = {cls.get_name_path(e): e for e in children1}
        result_list = list()
        for pset in children0:
            name_path = cls.get_name_path(pset)
            match = cls.find_matching_entity(pset, uuid_dict, {})
            if match is None:
                match = name_dict.get(name_path)
            if match is not None:
                missing.remove(match)
            result_list.append((pset, match))
        for pset in missing:
            result_list.append((None, pset))
        return result_list

    @classmethod
    def children_are_identical(cls, entity0, entity1):
        child_matchup = cls.create_child_matchup(entity0, entity1)
        return all(None not in x for x in child_matchup)

    @classmethod
    def are_objects_identical(cls, object0: SOMcreator.Object, object1: SOMcreator.Object, check_pset=True) -> bool:
        if object0 is None or object1 is None:
            return False
        names_are_identical = object0.name == object1.name
        identifiers_are_identical = object0.ident_value == object1.ident_value
        property_set_list = cls.get_pset_list(object0)
        if not property_set_list:
            return False

        if check_pset:
            psets_are_identical = all(cls.are_property_sets_identical(p0, p1) for p0, p1 in property_set_list)
        else:
            psets_are_identical = True
        return all((names_are_identical, identifiers_are_identical, psets_are_identical))

    @classmethod
    def are_property_sets_identical(cls, property_set0: SOMcreator.PropertySet,
                                    property_set1: SOMcreator.PropertySet, check_attributes=True) -> bool:
        if property_set0 is None or property_set1 is None:
            return False
        attribute_list = cls.get_attribute_list(property_set0)
        if not attribute_list:
            return False

        checks = list()

        checks.append(property_set0.name == property_set1.name)  # names_are_identical

        if check_attributes:
            checks.append(
                all(cls.are_attributes_identical(a0, a1) for a0, a1 in attribute_list))  # are attributes identical
        checks.append(cls.children_are_identical(property_set0, property_set1))
        return all(checks)

    @classmethod
    def are_attributes_identical(cls, attribute0: SOMcreator.Attribute, attribute1: SOMcreator.Attribute) -> bool:
        if attribute0 is None or attribute1 is None:
            return False

        checks = list()
        checks.append(set(attribute0.get_own_values()) == set(attribute1.get_own_values()))  # values_are_identical
        checks.append(attribute0.data_type == attribute1.data_type)  # datatypes_are_identical
        checks.append(attribute0.value_type == attribute1.value_type)  # valuetypes_are_identical
        checks.append(attribute0.name == attribute1.name)  # names_are_identical
        checks.append(attribute0.child_inherits_values == attribute1.child_inherits_values)  # Inherits Values
        return all(checks)

    @classmethod
    def style_table(cls, table: QTableWidget, shift=0):
        column_count = table.columnCount()
        for row in range(table.rowCount()):
            item0 = table.item(row, shift)
            item1 = table.item(row, shift + 1)
            t0 = item0.text()
            t1 = item1.text()

            if t0 and not t1:
                color = style_list[3][0]
            elif t1 and not t0:
                color = style_list[2][0]
            elif t1 != t0:
                color = style_list[1][0]
            else:
                color = None

            brush = QBrush(QColor(color)) if color is not None else QBrush()
            for col in range(column_count):
                table.item(row, col).setBackground(brush)

    @classmethod
    def style_parent_item(cls, item: QTreeWidgetItem, style: int) -> None:
        """
        iterates branch upwards to style every parent item so the child won't be overseen
        """
        parent = item.parent()
        if parent is None or parent == item.treeWidget().invisibleRootItem():
            return
        parent_style_index = parent.data(0, CLASS_REFERENCE + 1)
        if parent_style_index < style:
            cls.set_tree_row_color(parent, style)
            cls.style_parent_item(parent, style)

    @classmethod
    def style_tree_item(cls, item: QTreeWidgetItem) -> None:
        entity0, entity1 = cls.get_entities_from_item(item)
        style = 2 if entity0 is None else 3 if entity1 is None else None
        if style is None:
            if isinstance(entity0, SOMcreator.Object):
                compare_func = cls.are_objects_identical
            elif isinstance(entity0, SOMcreator.PropertySet):
                compare_func = lambda p1, p2: cls.are_property_sets_identical(p1, p2, False)
            else:
                compare_func = cls.are_attributes_identical

            style = 0 if compare_func(entity0, entity1) else 1
        cls.set_tree_row_color(item, style)
        if style > 0:
            parent = item.parent()
            index = item.treeWidget().indexFromItem(parent, 0)
            cls.set_branch_color(item.treeWidget(), index, style_list[1][0])

        for child_index in range(item.childCount()):
            if not isinstance(entity0, SOMcreator.Attribute):
                cls.style_tree_item(item.child(child_index))

    @classmethod
    def set_header_labels(cls, trees: list[QTreeWidget], tables: list[QTableWidget], labels: list[str]):
        for tree in trees:
            tree.setHeaderLabels(labels)
        for table in tables:
            table.setHorizontalHeaderLabels(labels)

    @classmethod
    def export_existance_check(cls, file: TextIO, type_name: str, entity0, entity1, indent: int) -> bool:
        """
        Writes to File if one of 2 entities doesn't exist
        """
        if entity0 and not entity1:
            file.write(f"{'   ' * indent}{type_name} '{entity0.name}' {DELETE_TEXT}\n")
            return False
        elif entity1 and not entity0:
            file.write(f"{'   ' * indent}{type_name} '{entity1.name}' {ADD_TEXT}\n")
            return False
        return True

    @classmethod
    def export_name_check(cls, file: TextIO, type_name: str, entity0, entity1, indent: int) -> bool:
        """
        Writes differences between Names of entities to File
        """
        if entity0.name != entity1.name:
            file.write(f"{'   ' * indent}{type_name} '{entity0.name}' {RENAME_TEXT} '{entity1.name}'\n")
            return False
        return True

    @classmethod
    def export_attribute_check(cls, file: TextIO, type_name: str, attrib0, attrib1, indent: int) -> bool:
        """
        Writes differences between Attributes to File
        """
        change_list = list()
        if attrib0.get_own_values() != attrib1.get_own_values():
            change_list.append(['Values', attrib0.get_own_values(), attrib1.get_own_values()])
        if attrib0.data_type != attrib1.data_type:
            change_list.append(['Datatype', attrib0.data_type, attrib1.data_type])
        if attrib0.value_type != attrib1.value_type:
            change_list.append(['Datatype', attrib0.value_type, attrib1.value_type])
        if attrib0.child_inherits_values != attrib1.child_inherits_values:
            change_list.append(['Child Inheritance', attrib0.child_inherits_values, attrib1.child_inherits_values])
        for t, v0, v1 in change_list:
            file.write(f"{'   ' * indent}{type_name} '{attrib0.name}' {t} {CHANGED_FROM} '{v0}' to '{v1}'\n")
        return bool(change_list)

    @classmethod
    def get_name_path(cls, entity: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute) -> str:
        text = entity.name
        if isinstance(entity, SOMcreator.Object):
            return text
        if isinstance(entity, SOMcreator.PropertySet):
            obj = entity.object
            if obj is None:
                return text
            return f"{obj.name}:{text}"
        if isinstance(entity, SOMcreator.Attribute):
            pset = entity.property_set
            if pset is None:
                return text
            text = f"{pset.name}:{text}"
            obj = pset.object
            if obj is None:
                return text
            return f"{obj.name}:{text}"
        else:
            return ""

    @classmethod
    def export_child_check(cls, file: TextIO, type_name, entity0, entity1, indent: int) -> bool:
        child_matchup = cls.create_child_matchup(entity0, entity1)
        identical = True

        for c0, c1 in child_matchup:  # ALT,NEU
            if c0 is None:
                cn = cls.get_name_path(c1)
                file.write(f"{'   ' * indent}{type_name} '{entity0.name}' {ADD_CHILD} '{cn}'\n")
                identical = False
            elif c1 is None:
                cn = cls.get_name_path(c0)
                file.write(f"{'   ' * indent}{type_name} '{entity0.name}' {REMOVE_CHILD} '{cn}'\n")
                identical = False
        return identical

    @classmethod
    def export_object_differences(cls, file: TextIO):
        project0 = cls.get_project(0)
        object_dict = cls.get_object_dict()

        for obj0 in sorted(project0.get_objects(filter=False), key=lambda x: x.name):
            obj1 = object_dict[obj0]
            if cls.are_objects_identical(obj0, obj1):
                continue
            file.write(f"\n{obj0.name} ({obj0.ident_value}):\n")
            cls.export_pset_differences(file, cls.get_pset_list(obj0))

    @classmethod
    def export_pset_differences(cls, file: TextIO,
                                pset_list: list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]],
                                lb: bool = False):
        ps = "PropertySet"
        for pset0, pset1 in sorted(pset_list, key=lambda x: x[0].name if x[0] is not None else "aaa"):
            if cls.are_property_sets_identical(pset0, pset1):
                continue
            if lb:
                file.write("\n")
            both_exist = cls.export_existance_check(file, ps, pset0, pset1, 1)
            if not both_exist:
                continue
            file.write(f"   PropertySet '{pset0.name}':\n")
            cls.export_name_check(file, ps, pset0, pset1, 2)
            cls.export_child_check(file, ps, pset0, pset1, 2)

            attribute_list = cls.get_properties().attributes_lists[pset0]
            cls.export_attribute_differences(file, attribute_list)

    @classmethod
    def export_attribute_differences(cls, file: TextIO,
                                     attribute_list: list[tuple[SOMcreator.Attribute, SOMcreator.Attribute]]):
        at = "Attribute"
        for attrib0, attrib1 in sorted(attribute_list, key=lambda x: x[0].name if x[0] is not None else "aaa"):
            if cls.are_attributes_identical(attrib0, attrib1):
                continue

            both_exist = cls.export_existance_check(file, at, attrib0, attrib1, 2)
            if not both_exist:
                continue
            cls.export_child_check(file, at, attrib0, attrib1, 2)
            cls.export_name_check(file, at, attrib0, attrib1, 2)
            cls.export_attribute_check(file, at, attrib0, attrib1, 2)

    # GETTER & SETTER

    @classmethod
    def get_object_tree(cls, widget: ui.AttributeWidget):
        return widget.widget.tree_widget_object

    @classmethod
    def get_pset_tree(cls, widget: ui.AttributeWidget):
        return widget.widget.tree_widget_propertysets

    @classmethod
    def get_value_table(cls, widget: ui.AttributeWidget):
        return widget.widget.table_widget_values

    @classmethod
    def get_widget(cls):
        if cls.get_properties().widget is None:
            cls.get_properties().widget = ui.AttributeWidget()
        return cls.get_properties().widget

    @classmethod
    def get_project(cls, index=1) -> SOMcreator.Project:
        return cls.get_properties().projects[index]

    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_pset_list(cls, obj: SOMcreator.Object) -> list[
                                                          tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]] | None:
        return cls.get_properties().pset_lists.get(obj)

    @classmethod
    def set_pset_list(cls, obj: SOMcreator.Object,
                      pset_list: list[tuple[SOMcreator.PropertySet, SOMcreator.PropertySet]]):
        cls.get_properties().pset_lists[obj] = pset_list

    @classmethod
    def get_attribute_list(cls, property_set: SOMcreator.PropertySet) -> list[tuple[
        SOMcreator.Attribute, SOMcreator.Attribute]] | None:
        return cls.get_properties().attributes_lists.get(property_set)

    @classmethod
    def set_attribute_list(cls, property_set: SOMcreator.PropertySet,
                           attribute_list: list[tuple[SOMcreator.Attribute, SOMcreator.Attribute]]):
        cls.get_properties().attributes_lists[property_set] = attribute_list

    @classmethod
    def get_value_list(cls, attribute: SOMcreator.Attribute) -> list[tuple[str | None, str | None]] | None:
        return cls.get_properties().values_lists.get(attribute)

    @classmethod
    def set_value_list(cls, attribute: SOMcreator.Attribute | SOMcreator.PropertySet,
                       value_list: list[tuple[str | None, str | None]]):
        cls.get_properties().values_lists[attribute] = value_list

    @classmethod
    def get_branch_color(cls, index: QModelIndex):
        color = index.data(CLASS_REFERENCE + 1)
        return QColor(color) if isinstance(color, str) else None

    @classmethod
    def set_branch_color(cls, tree: QTreeWidget, index: QModelIndex, color: str | None):
        model = tree.model()
        model.setData(index, color, CLASS_REFERENCE + 1)
        if index.parent().isValid():
            cls.set_branch_color(tree, index.parent(), color)

    @classmethod
    def set_tree_row_color(cls, item: QTreeWidgetItem, style_index):
        item.setData(0, CLASS_REFERENCE + 1, style_index)
        color, column_list = style_list[style_index]
        for column in column_list:
            brush = QBrush(QColor(color)) if color is not None else QPalette().base()
            item.setBackground(column, brush)

    @classmethod
    def get_level(cls, index):
        parent = index.parent()
        level = 1
        while parent.isValid():
            parent = parent.parent()
            level += 1
        return level

    @classmethod
    def get_uuid_dict(cls, index=1) -> dict:
        if cls.get_properties().uuid_dicts[index] is None:
            project = cls.get_project(index)
            d = {hi.uuid: hi for hi in project.get_hirarchy_items(filter=False)}
            cls.get_properties().uuid_dicts[index] = d
        return cls.get_properties().uuid_dicts[index]

    @classmethod
    def get_ident_dict(cls, index=1) -> dict:
        if cls.get_properties().ident_dicts[index] is None:
            project = cls.get_project(index)
            d = {obj.ident_value: obj for obj in project.get_objects(filter=False)}
            cls.get_properties().ident_dicts[index] = d
        return cls.get_properties().ident_dicts[index]

    @classmethod
    def get_object_lists(cls) -> list[tuple[SOMcreator.Object | None, SOMcreator.Object | None]]:
        return cls.get_properties().object_lists

    @classmethod
    def get_missing_objects(cls, index: int) -> list[SOMcreator.Object]:
        ol = cls.get_object_lists()
        if cls.get_properties().missing_objects[index] is None:
            missing = [o[index] for o in ol if o[index - 1] is None]
            cls.get_properties().missing_objects[index] = missing
        return cls.get_properties().missing_objects[index]

    @classmethod
    def get_object_dict(cls) -> dict:
        return cls.get_properties().object_dict

    @classmethod
    def set_object_item_relation(cls, obj: SOMcreator.Object, item: QTreeWidgetItem):
        cls.get_properties().object_tree_item_dict[obj] = item

    @classmethod
    def get_item_from_object(cls, obj: SOMcreator.Object) -> QTreeWidgetItem | None:
        return cls.get_properties().object_tree_item_dict.get(obj)

    @classmethod
    def get_selected_item(cls, tree: QTreeWidget):
        selected_items = tree.selectedItems()
        if not selected_items:
            return None
        return selected_items[0]

    @classmethod
    def get_selected_entity(cls,
                            tree: QTreeWidget) -> SOMcreator.PropertySet | SOMcreator.Attribute | SOMcreator.Object | None:
        item = cls.get_selected_item(tree)
        d0, d1 = cls.get_entities_from_item(item)
        data = d0 or d1
        return data

    @classmethod
    def get_entities_from_item(cls, item: QTreeWidgetItem) -> tuple[
        SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute,
        SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute]:
        if item is None:
            return None, None
        entity0 = item.data(0, CLASS_REFERENCE)
        entity1 = item.data(1, CLASS_REFERENCE)
        return entity0, entity1

    @classmethod
    def get_header_name_from_project(cls, project: SOMcreator.Project):
        return f"{project.name} v{project.version}"

    @classmethod
    def get_info_table(cls, widget: ui.AttributeWidget):
        return widget.widget.table_infos
