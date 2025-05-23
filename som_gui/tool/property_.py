from __future__ import annotations

import logging
from typing import Any, Callable, TYPE_CHECKING, TextIO, Union, Type, Sequence, TypeVar

from PySide6.QtCore import QModelIndex, Qt,QObject,Signal,QCoreApplication
from PySide6.QtGui import QBrush, QColor, QPalette
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QListWidget,
)

import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.module.property_ import trigger, ui, constants
from som_gui.module.project.constants import CLASS_REFERENCE
from ifcopenshell.util.unit import unit_names, prefixes

if TYPE_CHECKING:
    from som_gui.module.property_.prop import (
        PropertyProperties,
        ComparePropertyProperties,
    )

SOMType = Union[SOMcreator.SOMProperty, SOMcreator.SOMPropertySet]

T = TypeVar("T", SOMcreator.SOMProperty, SOMcreator.SOMPropertySet, SOMcreator.SOMClass)


style_list = [
    [None, [0, 1]],
    ["#897e00", [0, 1]],  # Yellow  ->  Data changed
    ["#006605", [1]],  # green      ->  Data stayed The same
    ["#840002", [0]],  # red         ->  Data was deleted
]

class Signaller(QObject):
    empty_property_requested = Signal(SOMcreator.SOMPropertySet)
    property_created = Signal(SOMcreator.SOMProperty)
class Property(som_gui.core.tool.Property):
    signaller = Signaller()
    @classmethod
    def get_properties(cls) -> PropertyProperties:
        return som_gui.PropertyProperties  # type: ignore

    @classmethod
    def connect_signals(cls):
        cls.signaller.empty_property_requested.connect(trigger.create_empty_property)
        
    @classmethod
    def add_property_data_value(
        cls, name: str, getter: Callable, setter: Callable
    ) -> None:
        """
        Add value to PropertyDataDict
        :param name: Key of Data
        :param getter: getter func to get data
        :param setter: setter funct to set Property Value
        """
        prop = cls.get_properties()
        prop.property_data_dict[name] = {"getter": getter, "setter": setter}

    @classmethod
    def get_property_data(cls, som_property: SOMcreator.SOMProperty) -> dict[str, Any]:
        """
        creates dictionary of property with Data_name as Key and getter/setter as Value
        :param som_property:
        :return: PropertyData dictionary {Data_name:{'getter':Callable, 'setter':Callable},...}
        """
        prop = cls.get_properties()
        d = dict()
        for name, data_dict in prop.property_data_dict.items():
            value = data_dict["getter"](som_property)
            d[name] = value
        return d

    @classmethod
    def set_data_by_dict(
        cls, som_property: SOMcreator.SOMProperty, data_dict: dict[str, str | list]
    ) -> None:
        """
        fill Property Values by an Property Datadict
        :param som_property: Property of class SOMcreator.SOMProperty
        :param data_dict: PropertyData dictionary {Data_name:{'getter':Callable, 'setter':Callable},...}
        """
        prop = cls.get_properties()
        for name, value in data_dict.items():
            d = prop.property_data_dict.get(name)
            if not d:
                logging.warning(f"data {name} not found")
                continue
            d["setter"](value, som_property)

    @classmethod
    def create_by_dict(
        cls, property_data: dict[str, str | list]
    ) -> SOMcreator.SOMProperty:
        """
        create SOMcreator.SOMProperty from Datadict
        :param property_data: dictionary {Data_name:{'getter':Callable, 'setter':Callable},...}
        :return:
        """
        som_property = SOMcreator.SOMProperty()
        cls.set_data_by_dict(som_property, property_data)
        return som_property

    @classmethod
    def set_unit_settings_widget(cls, widget: ui.UnitSettings):
        cls.get_properties().unit_settings_widget = widget

    @classmethod
    def get_unit_settings_widget(
        cls,
    ) -> ui.UnitSettings | None:
        return cls.get_properties().unit_settings_widget

    @classmethod
    def get_allowed_units(cls, appdata: Type[tool.Appdata]):
        """
        Search Appdata for allowed units. If no allowed units are saved, return all existing units.

        :param appdata: The application data instance to retrieve settings from.
        :type appdata: Type[tool.Appdata]
        :return: A list of allowed units.
        :rtype: list[str]
        """
        all_units = [un.capitalize() for un in unit_names]
        allowed_units = appdata.get_list_setting(
            constants.UNITS_SECTION, constants.ALLOWED_UNITS, None
        )
        if allowed_units is None:
            allowed_units = list(all_units)
        return allowed_units

    @classmethod
    def get_allowed_unit_prefixes(cls, appdata: Type[tool.Appdata]):
        """
        Retrieve the list of allowed unit prefixes from the application data.
        :param appdata: The application data instance to retrieve settings from.
        :type appdata: Type[tool.Appdata]
        :return: A list of allowed unit prefixes.
        :rtype: list[str]
        """
        all_prefixes = [pf.capitalize() for pf in prefixes.keys()]
        allowed_prefixes = appdata.get_list_setting(
            constants.UNITS_SECTION, constants.ALLOWED_PREFIXES, None
        )
        if allowed_prefixes is None:
            allowed_prefixes = list(all_prefixes)
        return allowed_prefixes

    @classmethod
    def get_checked_texts_from_list_widget(cls, list_widget: QListWidget) -> list[str]:
        items = [list_widget.item(i) for i in range(list_widget.count())]
        return [i.text() for i in items if i.checkState() == Qt.CheckState.Checked]


class PropertyCompare(som_gui.core.tool.PropertyCompare):
    @classmethod
    def get_properties(cls) -> ComparePropertyProperties:
        return som_gui.ComparePropertyProperties  # type: ignore

    @classmethod
    def reset(cls) -> None:
        """
        reset all saved settings and values for new Run
        :return: None
        """
        prop = cls.get_properties()
        prop.projects = [None, None]
        prop.uuid_dicts = [None, None]
        prop.ident_dicts = [None, None]
        prop.class_dict = dict()
        prop.class_lists = list()
        prop.missing_classes = [None, None]
        prop.class_tree_item_dict = dict()
        prop.pset_lists = dict()
        prop.properties_lists = dict()
        prop.values_lists = dict()
        prop.widget = None

    @classmethod
    def create_tree_selection_trigger(cls, widget: ui.PropertyWidget):
        """
        create trigger if ClassTree and PropertySetTree are selected
        :param widget:
        :return:
        """
        widget.ui.tree_widget_class.itemSelectionChanged.connect(
            lambda: trigger.class_tree_selection_changed(widget)
        )
        widget.ui.tree_widget_propertysets.itemSelectionChanged.connect(
            lambda: trigger.pset_tree_selection_changed(widget)
        )

    @classmethod
    def find_matching_class(
        cls, som_class: SOMcreator.SOMClass, index=1
    ) -> SOMcreator.SOMClass | None:
        """
        find class that matches to input. The function searches for the UUID and Identifier if not class is found return None
        :param som_class: class for which a match is to be found
        :param index: defines if class should  be searched in Project 0 or Project 1
        :return:
        """
        uuid_dict = cls.get_uuid_dict(index)
        ident_dict = cls.get_ident_dict(index)
        uuid_match = uuid_dict.get(som_class.uuid)
        if uuid_match:
            return uuid_match
        ident_match = ident_dict.get(som_class.ident_value)

        if ident_match:
            return ident_match
        return None

    @classmethod
    def find_matching_entity(
        cls,
        search_element: T,
        uuid_dict1: dict[str, T],
        name_dict1: dict[str, T],
    ) -> T | None:
        """
        find property/propertySet that mathches to input. The function searches for the UUID and Identifier if no Element is found return None
        :param search_element: Property/PropertySet for which a match is to be found
        :param uuid_dict1: Dictiorary of UUIDs to search for Element UUID
        :param name_dict1: Dictiorary of UUIDs to search for Element Name
        :return:
        """
        if search_element.uuid in uuid_dict1:
            return uuid_dict1[search_element.uuid]
        if search_element.name in name_dict1:
            return name_dict1[search_element.name]
        return None

    @classmethod
    def generate_uuid_dict(cls, element_list: Sequence[T]) -> dict[str, T]:
        """
        create dictionary of UUIDs of all Elements in element_list
        :param element_list: list of all Elements for which a UUID entry is needed
        :return: Dictionary of UUIDs of all Elements in element_list
        """
        return {p.uuid: p for p in element_list if p.uuid}

    @classmethod
    def generate_name_dict(cls, element_list: Sequence[T]) -> dict[str, T]:
        """
        create dictionary of Names of all Elements in element_list
        :param element_list: list of all Elements for which a Names entry is needed
        :return: Dictionary of UUIDs of all Elements in element_list
        """
        return {p.name: p for p in element_list if p.name}

    @classmethod
    def compare_classes(
        cls, class_0: None | SOMcreator.SOMClass, class_1: None | SOMcreator.SOMClass
    ) -> list[
        tuple[SOMcreator.SOMPropertySet | None, SOMcreator.SOMPropertySet | None]
    ]:
        """
        Compare two SOMcreator classes by their property sets.
        This method generates a list of matched and unmatched property sets (match_list)
        for both classes and assigns it to them using the set_pset_list function
        :param class_0: First class to compare, or None.
        :param class_1: Second class to compare, or None.
        :return:
        """
        # Create Match Dictionaries
        psets_1 = list(class_1.get_property_sets(filter=False)) if class_1 is not None else []
        property_set_uuid_dict1 = cls.generate_uuid_dict(psets_1)
        property_set_name_dict1 = cls.generate_name_dict(psets_1)

        match_list = list()
        missing_property_sets_1 = list(
            psets_1
        )  # copy list of Psets to substract every found Pset

        if class_0 is not None:
            for property_set0 in class_0.get_property_sets(filter=False):
                # Search for Matching PropertySet
                match = cls.find_matching_entity(
                    property_set0, property_set_uuid_dict1, property_set_name_dict1
                )
                if match is not None:
                    if match in missing_property_sets_1:
                        missing_property_sets_1.remove(match)
                    else:
                        # This happens if for one Property in the Search-Project multiple Properties in the Start-Project exist
                        # Because we're using a 1:1 Match the second time the same Pset is found it will be saved as an Empty Math
                        match_list.append((property_set0, None))
                        cls.compare_property_sets(property_set0, None)
                        continue
                cls.compare_property_sets(
                    property_set0, match
                )  # Compares Properties in PropertySets
                match_list.append((property_set0, match))

        # Handle PropertySets in the Search-Project that doesn't match to any PropertySet in the Start-Project
        for property_set1 in missing_property_sets_1:
            match_list.append((None, property_set1))
        if class_0 is not None:
            cls.set_pset_list(class_0, match_list)
        if class_1 is not None:
            cls.set_pset_list(class_1, match_list)

        return match_list

    @classmethod
    def compare_property_sets(
        cls,
        pset_0: SOMcreator.SOMPropertySet | None,
        pset_1: SOMcreator.SOMPropertySet | None,
    ) -> Sequence[tuple[SOMcreator.SOMProperty, SOMcreator.SOMProperty]]:
        """
        Compare two SOMcreator PropertySets by their Properties.
        This method generates a list of matched and unmatched Properties (match_list)
        for both PropertySets and assigns it to them using the set_property_list function
        :param pset0: First PropertySet to compare, or None.
        :param pset1: Second PropertySet to compare, or None.
        :return:
        """
        result_list = cls.create_child_matchup(pset_0, pset_1)
        if pset_0 is not None:
            cls.set_value_list(pset_0, result_list)
        if pset_1 is not None:
            cls.set_value_list(pset_1, result_list)

        if pset_0 is None or pset_1 is None:
            return []
        # Generate Match Dicts
        properties_1 = list(pset_1.get_properties(filter=False))
        property_uuid_dict_1 = cls.generate_uuid_dict(properties_1)
        property_name_dict_1 = cls.generate_name_dict(properties_1)

        missing_properties_1 = list(properties_1)
        match_list = list()

        for property_0 in pset_0.get_properties(filter=False):
            match = cls.find_matching_entity(
                property_0, property_uuid_dict_1, property_name_dict_1
            )
            if match is not None:
                missing_properties_1.remove(match)
                match_list.append((property_0, match))
            else:
                match_list.append((property_0, None))

        for property_1 in missing_properties_1:
            match_list.append((None, property_1))

        for a1, a2 in match_list:
            cls.compare_properties(a1, a2)
        cls.set_property_list(pset_0, match_list)
        cls.set_property_list(pset_1, match_list)
        return match_list

    @classmethod
    def compare_properties(
        cls, property_0: SOMcreator.SOMProperty, property_1: SOMcreator.SOMProperty
    ):
        """
        compare two SOMcreator Properties by their Values
        :param property_0:
        :param property_1:
        :return:
        """
        values0 = set(property_0.allowed_values) if property_0 is not None else set()
        values1 = set(property_1.allowed_values) if property_1 is not None else set()

        unique0 = values0.difference(values1)
        main = values0.intersection(values1)
        unique1 = values1.difference(values0)

        value_list = (
            [(v, v) for v in main]
            + [(v, None) for v in unique0]
            + [(None, v) for v in unique1]
        )
        if property_0 is not None:
            cls.set_value_list(property_0, value_list)
        if property_1 is not None:
            cls.set_value_list(property_1, value_list)

    @classmethod
    def create_class_lists(cls) -> None:
        class_list = cls.get_class_list()
        if class_list:
            return
        project_0, project_1 = cls.get_project(0), cls.get_project(1)
        found_classes = list()
        for class_0 in project_0.get_classes(filter=False):
            match = cls.find_matching_class(class_0, 1)
            if match is None:
                class_list.append((class_0, None))
                cls.compare_classes(class_0, None)
            else:
                class_list.append((class_0, match))
                found_classes.append(match)
                cls.compare_classes(class_0, match)

        for class_1 in [
            o for o in project_1.get_classes(filter=False) if o not in found_classes
        ]:
            class_list.append((None, class_1))
            cls.compare_classes(None, class_1)

        cls.create_class_dicts()

    @classmethod
    def create_class_dicts(cls) -> None:
        od = dict()
        for o0, o1 in cls.get_class_list():
            if o0 is not None:
                od[o0] = o1
            if o1 is not None:
                od[o1] = o1
        cls.get_properties().class_dict = od

    @classmethod
    def add_class_to_item(
        cls, som_class: SOMcreator.SOMClass, item: QTreeWidgetItem, index: int
    ):
        start_index = index
        ident_text = f"({som_class.ident_value})" if som_class.ident_value else ""
        text = f"{som_class.name} {ident_text}"
        item.setText(start_index, text)
        item.setData(start_index, CLASS_REFERENCE, som_class)
        cls.set_class_item_relation(som_class, item)

    @classmethod
    def fill_class_tree_layer(
        cls,
        classes: list[SOMcreator.SOMClass],
        parent_item: QTreeWidgetItem,
        add_missing: bool,
    ):
        class_dict = cls.get_class_dict()

        for som_class in classes:
            match_class = class_dict.get(som_class)
            item = QTreeWidgetItem()
            cls.add_class_to_item(som_class, item, 0)
            if match_class:
                cls.add_class_to_item(match_class, item, 1)

            if match_class is not None or add_missing:
                parent_item.addChild(item)
            cls.fill_class_tree_layer(
                list(som_class.get_children(filter=False)), item, add_missing
            )

    @classmethod
    def fill_class_tree(cls, tree: QTreeWidget, add_missing: bool = True):
        proj0, proj1 = cls.get_project(0), cls.get_project(1)
        tree_root = tree.invisibleRootItem()
        root_classes = tool.Project.get_root_classes(False, proj0)
        cls.fill_class_tree_layer(root_classes, tree_root, add_missing)
        if add_missing:
            cls.add_missing_classes_to_tree(
                tree, tool.Project.get_root_classes(False, proj1)
            )

    @classmethod
    def fill_value_table_pset(cls, widget: ui.PropertyWidget):
        pset_tree = cls.get_pset_tree(widget)
        item = cls.get_selected_item(pset_tree)
        table = cls.get_value_table(widget)
        cls.clear_table(table)
        pset0, pset1 = cls.get_entities_from_item(item)
        if not isinstance(pset0, SOMcreator.SOMPropertySet | None):
            return
        if not isinstance(pset1, SOMcreator.SOMPropertySet | None):
            return
        target = pset0 or pset1
        if target is None:
            return
        val = cls.get_value_list(target)
        for property_sets in val:
            table.insertRow(table.rowCount())
            for index, p in enumerate(property_sets):
                item = QTableWidgetItem(p.som_class.name if p else "")
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
        name_text = QCoreApplication.translate("PropertyCompare", "Name")
        c_count_text = QCoreApplication.translate("PropertyCompare", "Child Count")
        info_list.append((name_text, lambda p: getattr(p, "name")))
        info_list.append(
            (
                c_count_text,
                lambda p: len(list(p.get_children(filter=True))) if p else "",
            )
        )
        return info_list

    @classmethod
    def get_property_info_list(cls):
        info_list = list()
        name_text = QCoreApplication.translate("PropertyCompare", "Name")
        iv_text = QCoreApplication.translate("PropertyCompare", "Inheriting values")
        datatype_text = QCoreApplication.translate("PropertyCompare", "Datatype")
        value_type_text = QCoreApplication.translate("PropertyCompare", "Valuetype")

        info_list.append((name_text, lambda a: getattr(a, "name")))
        info_list.append((iv_text, lambda a: getattr(a, "child_inherits_values")))
        info_list.append((datatype_text, lambda a: getattr(a, "data_type")))
        info_list.append((value_type_text, lambda a: getattr(a, "value_type")))
        return info_list

    @classmethod
    def find_existing_parent_item(
        cls, som_class: SOMcreator.SOMClass
    ) -> QTreeWidgetItem | None:
        parent = som_class.parent
        while parent is not None:
            parent_item = cls.get_item_from_class(parent)
            if parent_item is not None:
                return parent_item
            parent = parent.parent
        return None

    @classmethod
    def add_missing_classes_to_tree(
        cls, tree: QTreeWidget, root_classes: list[SOMcreator.SOMClass]
    ):
        missing_classes = cls.get_missing_classes(1)
        for som_class in root_classes:
            if som_class in missing_classes:
                parent = cls.find_existing_parent_item(som_class)
                parent = parent if parent is not None else tree.invisibleRootItem()
                item = QTreeWidgetItem()
                cls.add_class_to_item(som_class, item, 1)
                parent.addChild(item)
            cls.add_missing_classes_to_tree(tree, list(som_class.get_children(filter=False)))

    @classmethod
    def clear_tree(cls, tree: QTreeWidget):
        root = tree.invisibleRootItem()
        for child_index in reversed(range(root.childCount())):
            root.removeChild(root.child(child_index))

    @classmethod
    def clear_table(cls, table: QTableWidget):
        table.setRowCount(0)

    @classmethod
    def fill_pset_tree(
        cls,
        tree: QTreeWidget,
        pset_list: (
            list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]] | None
        ),
        add_missing: bool = True,
    ) -> None:
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
    def add_properties_to_pset_tree(cls, tree: QTreeWidget, add_missing: bool):
        root = tree.invisibleRootItem()
        logging.debug(f"{root.childCount()} items in pset tree")
        for index in range(root.childCount()):
            logging.debug(f"Check index {index}")
            item = root.child(index)
            pset0, pset1 = cls.get_entities_from_item(item)
            property_list = cls.get_property_list(pset0) or cls.get_property_list(pset1)
            if property_list is None:
                logging.debug(f"Property List is None for {pset0}")
                continue
            for property_0, property_1 in property_list:
                property_item = QTreeWidgetItem()
                if property_0 is not None:
                    property_item.setText(0, property_0.name)
                    property_item.setData(0, CLASS_REFERENCE, property_0)
                if property_1 is not None:
                    property_item.setText(1, property_1.name)
                    property_item.setData(1, CLASS_REFERENCE, property_1)

                if (property_0 and property_1) or add_missing:
                    item.addChild(property_item)

    @classmethod
    def fill_value_table(
        cls, table: QTableWidget, som_property: SOMcreator.SOMProperty | None
    ):
        cls.clear_table(table)
        if som_property is None:
            return
        if cls.get_value_list(som_property) is None:
            return

        for value0, value1 in cls.get_value_list(som_property):
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
    def create_child_matchup(
        cls,
        entity0: T | None,
        entity1: T | None,
    ) -> Sequence[tuple[T | None, T | None]]:

        if entity0 is None and entity1 is not None:
            return [(None, p) for p in entity1.get_children(filter=False)]
        elif entity1 is None and entity0 is not None:
            return [(p, None) for p in entity0.get_children(filter=False)]

        if entity0 is None or entity1 is None:
            return []

        children0 = list(entity0.get_children(filter=False))
        children1 = list(entity1.get_children(filter=False))
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
                if match in missing:
                    missing.remove(match)
                else:
                    result_list.append((pset, None))
                    continue
            result_list.append((pset, match))
        for pset in missing:
            result_list.append((None, pset))
        return result_list

    @classmethod
    def children_are_identical(cls, entity0, entity1):
        child_matchup = cls.create_child_matchup(entity0, entity1)
        return all(None not in x for x in child_matchup)

    @classmethod
    def are_classes_identical(
        cls, class_0: SOMcreator.SOMClass, class_1: SOMcreator.SOMClass, check_pset=True
    ) -> bool:
        if class_0 is None or class_1 is None:
            return False
        names_are_identical = class_0.name == class_1.name
        identifiers_are_identical = class_0.ident_value == class_1.ident_value
        property_set_list = cls.get_pset_list(class_0)
        if not property_set_list:
            return False

        if check_pset:
            psets_are_identical = all(
                cls.are_property_sets_identical(p0, p1) for p0, p1 in property_set_list
            )
        else:
            psets_are_identical = True
        return all(
            (names_are_identical, identifiers_are_identical, psets_are_identical)
        )

    @classmethod
    def are_property_sets_identical(
        cls,
        property_set0: SOMcreator.SOMPropertySet,
        property_set1: SOMcreator.SOMPropertySet,
        check_properties=True,
    ) -> bool:
        if property_set0 is None or property_set1 is None:
            return False
        property_list = cls.get_property_list(property_set0)
        if not property_list:
            return False

        checks = list()

        checks.append(property_set0.name == property_set1.name)  # names_are_identical

        if check_properties:
            checks.append(
                all(cls.are_properties_identical(a0, a1) for a0, a1 in property_list)
            )  # are properties identical
        checks.append(cls.children_are_identical(property_set0, property_set1))
        return all(checks)

    @classmethod
    def are_properties_identical(
        cls, property_0: SOMcreator.SOMProperty, property_1: SOMcreator.SOMProperty
    ) -> bool:

        if property_0 is None or property_1 is None:
            return False

        checks = list()
        checks.append(
            set(property_0.allowed_values) == set(property_1.allowed_values)
        )  # values_are_identical
        if not (
            property_0.parent and property_1.parent
        ):  # If Datatype is changed by parent dont show in Table
            checks.append(
                property_0.data_type == property_1.data_type
            )  # datatypes_are_identical
            checks.append(
                property_0.value_type == property_1.value_type
            )  # valuetypes_are_identical
        checks.append(property_0.name == property_1.name)  # names_are_identical
        checks.append(
            property_0.child_inherits_values == property_1.child_inherits_values
        )  # Inherits Values
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
            if isinstance(entity0, SOMcreator.SOMClass):
                compare_func = cls.are_classes_identical
            elif isinstance(entity0, SOMcreator.SOMPropertySet):
                compare_func = lambda p1, p2: cls.are_property_sets_identical(
                    p1, p2, False
                )
            else:
                compare_func = cls.are_properties_identical

            style = 0 if compare_func(entity0, entity1) else 1
        cls.set_tree_row_color(item, style)
        if style > 0:
            parent = item.parent()
            index = item.treeWidget().indexFromItem(parent, 0)
            cls.set_branch_color(item.treeWidget(), index, style_list[1][0])

        for child_index in range(item.childCount()):
            if not isinstance(entity0, SOMcreator.SOMProperty):
                cls.style_tree_item(item.child(child_index))

    @classmethod
    def set_header_labels(
        cls, trees: list[QTreeWidget], tables: list[QTableWidget], labels: list[str]
    ):
        for tree in trees:
            tree.setHeaderLabels(labels)
        for table in tables:
            table.setHorizontalHeaderLabels(labels)

    @classmethod
    def export_existance_check(
        cls, file: TextIO, type_name: str, entity0, entity1, indent: int
    ) -> bool:
        """
        Writes to File if one of 2 entities doesn't exist
        """
        was_deleted = QCoreApplication.translate("PropertyCompare", "was deleted.")
        was_added = QCoreApplication.translate("PropertyCompare", "was added.")
        if entity0 and not entity1:
            file.write(f"{'   ' * indent}{type_name} '{entity0.name}' {was_deleted}\n")
            return False
        elif entity1 and not entity0:
            file.write(f"{'   ' * indent}{type_name} '{entity1.name}' {was_added}\n")
            return False
        return True

    @classmethod
    def export_name_check(
        cls, file: TextIO, type_name: str, entity0, entity1, indent: int
    ) -> bool:
        """
        Writes differences between Names of entities to File
        """
        rename_text = QCoreApplication.translate("PropertyCompare", "was renamed to")

        if entity0.name != entity1.name:
            file.write(
                f"{'   ' * indent}{type_name} '{entity0.name}' {rename_text} '{entity1.name}'\n"
            )
            return False
        return True

    @classmethod
    def export_property_check(
        cls, file: TextIO, type_name: str, attrib0, attrib1, indent: int
    ) -> bool:
        """
        Writes differences between Properties to File
        """
        change_list = list()
        if attrib0.get_own_values() != attrib1.get_own_values():
            change_list.append(
                ["Values", attrib0.get_own_values(), attrib1.get_own_values()]
            )
        if attrib0.data_type != attrib1.data_type:
            change_list.append(["Datatype", attrib0.data_type, attrib1.data_type])
        if attrib0.value_type != attrib1.value_type:
            change_list.append(["Datatype", attrib0.value_type, attrib1.value_type])
        if attrib0.child_inherits_values != attrib1.child_inherits_values:
            change_list.append(
                [
                    "Child Inheritance",
                    attrib0.child_inherits_values,
                    attrib1.child_inherits_values,
                ]
            )

        changed = QCoreApplication.translate("PropertyCompare", "was changed from")
        for t, v0, v1 in change_list:
            file.write(
                f"{'   ' * indent}{type_name} '{attrib0.name}' {t} {changed} '{v0}' to '{v1}'\n"
            )
        return bool(change_list)

    @classmethod
    def get_name_path(
        cls,
        entity: (
            SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty
        ),
    ) -> str:
        text = entity.name
        if isinstance(entity, SOMcreator.SOMClass):
            return text
        if isinstance(entity, SOMcreator.SOMPropertySet):
            som_class = entity.som_class
            if som_class is None:
                return text
            return f"{som_class.name}:{text}"
        if isinstance(entity, SOMcreator.SOMProperty):
            pset = entity.property_set
            if pset is None:
                return text
            text = f"{pset.name}:{text}"
            som_class = pset.som_class
            if som_class is None:
                return text
            return f"{som_class.name}:{text}"
        else:
            return ""

    @classmethod
    def export_child_check(
        cls, file: TextIO, type_name, entity0, entity1, indent: int
    ) -> bool:
        child_matchup = cls.create_child_matchup(entity0, entity1)
        identical = True
        add_child = QCoreApplication.translate("PropertyCompare", "added child")
        remove_child = QCoreApplication.translate("PropertyCompare", "removed child")
        for c0, c1 in child_matchup:  # ALT,NEU
            if c0 is None:
                cn = cls.get_name_path(c1)
                file.write(
                    f"{'   ' * indent}{type_name} '{entity0.name}' {add_child} '{cn}'\n"
                )
                identical = False
            elif c1 is None:
                cn = cls.get_name_path(c0)
                file.write(
                    f"{'   ' * indent}{type_name} '{entity0.name}' {remove_child} '{cn}'\n"
                )
                identical = False
        return identical

    @classmethod
    def export_class_differences(cls, file: TextIO):
        project_0 = cls.get_project(0)
        class_dict = cls.get_class_dict()

        for class_0 in sorted(project_0.get_classes(filter=False), key=lambda x: x.name):
            class_1 = class_dict[class_0]
            if cls.are_classes_identical(class_0, class_1):
                continue
            file.write(f"\n{class_0.name} ({class_0.ident_value}):\n")
            cls.export_pset_differences(file, cls.get_pset_list(class_0))

    @classmethod
    def export_pset_differences(
        cls,
        file: TextIO,
        pset_list: list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]],
        lb: bool = False,
    ):
        ps = "PropertySet"
        for pset0, pset1 in sorted(
            pset_list, key=lambda x: x[0].name if x[0] is not None else "aaa"
        ):
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

            property_list = cls.get_properties().properties_lists[pset0]
            cls.export_property_differences(file, property_list)

    @classmethod
    def export_property_differences(
        cls,
        file: TextIO,
        property_list: list[tuple[SOMcreator.SOMProperty, SOMcreator.SOMProperty]],
    ):
        at = "Property"
        for attrib0, attrib1 in sorted(
            property_list, key=lambda x: x[0].name if x[0] is not None else "aaa"
        ):
            if cls.are_properties_identical(attrib0, attrib1):
                continue

            both_exist = cls.export_existance_check(file, at, attrib0, attrib1, 2)
            if not both_exist:
                continue
            cls.export_child_check(file, at, attrib0, attrib1, 2)
            cls.export_name_check(file, at, attrib0, attrib1, 2)
            cls.export_property_check(file, at, attrib0, attrib1, 2)

    # GETTER & SETTER

    @classmethod
    def get_class_tree(cls, widget: ui.PropertyWidget):
        return widget.ui.tree_widget_class

    @classmethod
    def get_pset_tree(cls, widget: ui.PropertyWidget):
        return widget.ui.tree_widget_propertysets

    @classmethod
    def get_value_table(cls, widget: ui.PropertyWidget):
        return widget.ui.table_widget_values

    @classmethod
    def create_widget(cls):
        if cls.get_properties().widget is None:
            cls.get_properties().widget = ui.PropertyWidget()
        return cls.get_properties().widget

    @classmethod
    def get_widget(cls):
        return cls.get_properties().widget

    @classmethod
    def get_project(cls, index=1) -> SOMcreator.SOMProject:
        return cls.get_properties().projects[index]

    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_pset_list(
        cls, som_class: SOMcreator.SOMClass
    ) -> list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]] | None:
        return cls.get_properties().pset_lists.get(som_class)

    @classmethod
    def set_pset_list(
        cls,
        som_class: SOMcreator.SOMClass,
        pset_list: list[tuple[SOMcreator.SOMPropertySet, SOMcreator.SOMPropertySet]],
    ):
        cls.get_properties().pset_lists[som_class] = pset_list

    @classmethod
    def get_property_list(
        cls, property_set: SOMcreator.SOMPropertySet
    ) -> list[tuple[SOMcreator.SOMProperty, SOMcreator.SOMProperty]] | None:
        return cls.get_properties().properties_lists.get(property_set)

    @classmethod
    def set_property_list(
        cls,
        property_set: SOMcreator.SOMPropertySet,
        property_list: list[tuple[SOMcreator.SOMProperty, SOMcreator.SOMProperty]],
    ):
        cls.get_properties().properties_lists[property_set] = property_list

    @classmethod
    def get_value_list(cls, entity: T) -> Sequence[tuple[T | None, T | None]]:
        v = cls.get_properties().values_lists.get(entity)
        return list() if v is None else v  # type: ignore

    @classmethod
    def set_value_list(
        cls, entity: SOMType, value_list: Sequence[tuple[T | None, T | None]]
    ):
        cls.get_properties().values_lists[entity] = value_list

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
            d = {hi.uuid: hi for hi in project.get_items(filter=False)}
            cls.get_properties().uuid_dicts[index] = d
        return cls.get_properties().uuid_dicts[index]

    @classmethod
    def get_ident_dict(cls, index=1) -> dict:
        if cls.get_properties().ident_dicts[index] is None:
            project = cls.get_project(index)
            d = {som_class.ident_value: som_class for som_class in project.get_classes(filter=False)}
            cls.get_properties().ident_dicts[index] = d
        return cls.get_properties().ident_dicts[index]

    @classmethod
    def get_class_list(
        cls,
    ) -> list[tuple[SOMcreator.SOMClass | None, SOMcreator.SOMClass | None]]:
        return cls.get_properties().class_lists

    @classmethod
    def get_missing_classes(cls, index: int) -> list[SOMcreator.SOMClass]:
        ol = cls.get_class_list()
        if cls.get_properties().missing_classes[index] is None:
            missing = [o[index] for o in ol if o[index - 1] is None]
            cls.get_properties().missing_classes[index] = missing
        return cls.get_properties().missing_classes[index]

    @classmethod
    def get_class_dict(cls) -> dict:
        return cls.get_properties().class_dict

    @classmethod
    def set_class_item_relation(cls, som_class: SOMcreator.SOMClass, item: QTreeWidgetItem):
        cls.get_properties().class_tree_item_dict[som_class] = item

    @classmethod
    def get_item_from_class(cls, som_class: SOMcreator.SOMClass) -> QTreeWidgetItem | None:
        return cls.get_properties().class_tree_item_dict.get(som_class)

    @classmethod
    def get_selected_item(cls, tree: QTreeWidget):
        selected_items = tree.selectedItems()
        if not selected_items:
            return None
        return selected_items[0]

    @classmethod
    def get_selected_entity(
        cls, tree: QTreeWidget
    ) -> (
        SOMcreator.SOMPropertySet | SOMcreator.SOMProperty | SOMcreator.SOMClass | None
    ):
        item = cls.get_selected_item(tree)
        d0, d1 = cls.get_entities_from_item(item)
        data = d0 or d1
        return data

    @classmethod
    def get_entities_from_item(cls, item: QTreeWidgetItem | None) -> tuple[
        SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty,
        SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty,
    ]:
        if item is None:
            return None, None
        entity0 = item.data(0, CLASS_REFERENCE)
        entity1 = item.data(1, CLASS_REFERENCE)
        return entity0, entity1

    @classmethod
    def get_header_name_from_project(cls, project: SOMcreator.SOMProject):
        return f"{project.name} v{project.version}"

    @classmethod
    def get_info_table(cls, widget: ui.PropertyWidget):
        return widget.ui.table_infos
