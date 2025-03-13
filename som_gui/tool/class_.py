from __future__ import annotations

import copy as cp
import logging
import uuid
from typing import Callable, TYPE_CHECKING, TypedDict

from PySide6.QtCore import QPoint, Qt, QMimeData, QByteArray, QCoreApplication
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCompleter,
    QLineEdit,
    QMenu,
    QTreeWidgetItem,
    QComboBox,
)
import pickle
import SOMcreator
import som_gui
import som_gui.core.tool
import som_gui.tool as tool
import som_gui.module.class_
from som_gui.module.class_ import trigger, constants

if TYPE_CHECKING:
    from som_gui.module.class_.prop import ClassProperties, ContextMenuDict
    from som_gui.module.class_.ui import ClassTreeWidget
    from som_gui.module.class_info.prop import ClassDataDict


class Class(som_gui.core.tool.Class):
    @classmethod
    def get_properties(cls) -> ClassProperties:
        return som_gui.ClassProperties

    @classmethod
    def clear_tree(cls):
        tree = cls.get_class_tree()
        tree.clear()

    @classmethod
    def add_column_to_tree(cls, name_getter, index, getter_func, setter_func=None):
        tree = cls.get_class_tree()
        cls.get_properties().column_List.insert(
            index, (name_getter, getter_func, setter_func)
        )

        header = tree.headerItem()
        header_texts = cls.get_header_names()
        tree.setColumnCount(tree.columnCount() + 1)
        for col, name in enumerate(header_texts):
            header.setText(col, name)

        trigger.on_new_project()

    @classmethod
    def remove_column_from_tree(cls, column_name: str):
        tree = cls.get_class_tree()
        header = tree.headerItem()
        header_texts = cls.get_header_names()
        column_index = header_texts.index(column_name)
        cls.get_properties().column_List.pop(column_index)
        tree.setColumnCount(tree.columnCount() - 1)
        header_texts.pop(column_index)
        for col, name in enumerate(header_texts):
            header.setText(col, name)
        trigger.on_new_project()

    @classmethod
    def get_header_names(cls) -> list[str]:
        return [x[0]() for x in cls.get_properties().column_List]

    @classmethod
    def create_completer(cls, texts, widget: QLineEdit | QComboBox):
        completer = QCompleter(texts)
        widget.setCompleter(completer)

    @classmethod
    def get_item_from_class(cls, som_class: SOMcreator.SOMClass) -> QTreeWidgetItem:
        def iter_tree(item: QTreeWidgetItem):
            for child_index in range(item.childCount()):
                child = item.child(child_index)
                if cls.get_class_from_item(child) == som_class:
                    return child
                result = iter_tree(child)
                if result is not None:
                    return result
            return None

        tree = cls.get_class_tree()
        return iter_tree(tree.invisibleRootItem())

    @classmethod
    def select_class(cls, som_class: SOMcreator.SOMClass) -> None:
        item = cls.get_item_from_class(som_class)
        if item is None:
            return
        tree = cls.get_class_tree()
        for selected_item in tree.selectedItems():
            selected_item.setSelected(False)
        item.setSelected(True)
        cls.expand_to_item(item)
        cls.get_class_tree().scrollToItem(item)

    @classmethod
    def expand_to_item(cls, item: QTreeWidgetItem):
        item.setExpanded(True)
        if item.parent() is not None:
            cls.expand_to_item(item.parent())

    @classmethod
    def resize_tree(cls):
        tree = cls.get_class_tree()
        for col in reversed(range(tree.columnCount())):
            tree.resizeColumnToContents(col)

    @classmethod
    def group_classes(
        cls, parent: SOMcreator.SOMClass, children: set[SOMcreator.SOMClass]
    ):
        for child in children:
            parent.add_child(child)

    @classmethod
    def create_context_menu(cls):
        menu = QMenu()
        prop = cls.get_properties()
        selected_items = cls.get_selected_items()
        menu_list = prop.context_menu_list
        if len(selected_items) == 1:
            menu_list = filter(lambda d: d["on_single_select"], menu_list)
        if len(selected_items) > 1:
            menu_list = filter(lambda d: d["on_multi_select"], menu_list)
        for menu_entry in menu_list:
            menu_entry["action"] = menu.addAction(menu_entry["name_getter"]())
            menu_entry["action"].triggered.connect(menu_entry["function"])
        return menu

    @classmethod
    def get_selected_classes(cls) -> list[SOMcreator.SOMClass]:
        selected_items = cls.get_selected_items()
        return [cls.get_class_from_item(item) for item in selected_items]

    @classmethod
    def delete_class(cls, som_class: SOMcreator.SOMClass, recursive: bool = False):
        som_class.delete(recursive)

    @classmethod
    def delete_selection(cls):
        som_classes = cls.get_selected_classes()
        delete_request, recursive_deletion = tool.Popups.req_delete_items(
            [som_class.name for som_class in som_classes], item_type=1
        )
        if not delete_request:
            return
        for som_class in som_classes:
            cls.delete_class(som_class, recursive_deletion)

    @classmethod
    def expand_selection(cls):
        tree = cls.get_class_tree()
        for index in tree.selectedIndexes():
            tree.expandRecursively(index)

    @classmethod
    def collapse_selection(cls):
        tree = cls.get_class_tree()
        for item in tree.selectedItems():
            tree.collapseItem(item)

    @classmethod
    def group_selection(cls):
        pass

    @classmethod
    def clear_context_menu_list(cls):
        prop = cls.get_properties()
        prop.context_menu_list = list()

    @classmethod
    def add_context_menu_entry(
        cls, name_getter: Callable, function: Callable, single: bool, multi: bool
    ) -> ContextMenuDict:
        d: ContextMenuDict = dict()
        d["name_getter"] = name_getter
        d["function"] = function
        d["on_multi_select"] = multi
        d["on_single_select"] = single
        prop = cls.get_properties()
        prop.context_menu_list.append(d)
        return d

    @classmethod
    def handle_property_issue(cls, result: int):
        if result == constants.OK:
            return True
        if result == constants.IDENT_ISSUE:
            text = QCoreApplication.translate(
                "Class", "Identifier exists allready or is not allowed"
            )
        elif result == constants.IDENT_PROPERTY_ISSUE:
            text = QCoreApplication.translate(
                "Class", "Name of Property is not allowed"
            )
        elif result == constants.IDENT_PSET_ISSUE:
            text = QCoreApplication.translate(
                "Class", "Name of PropertySet is not allowed"
            )
        else:
            return False
        logging.debug(text)
        tool.Popups.create_warning_popup(text)
        return False

    @classmethod
    def set_ident_value(cls, som_class: SOMcreator.SOMClass, value: str):
        if som_class.is_concept:
            return
        som_class.identifier_property.allowed_values = [value]

    @classmethod
    def find_property(
        cls, som_class: SOMcreator.SOMClass, pset_name: str, property_name: str
    ):
        pset = som_class.get_property_set_by_name(pset_name)
        if pset is None:
            return None
        return pset.get_property_by_name(property_name)

    @classmethod
    def get_active_class(cls) -> SOMcreator.SOMClass | None:
        return cls.get_properties().active_class

    @classmethod
    def get_existing_ident_values(cls) -> set[str]:
        proj = tool.Project.get()
        ident_values = set()
        for som_class in proj.get_classes(filter=False):
            if som_class.ident_value:
                ident_values.add(som_class.ident_value)
        return ident_values

    @classmethod
    def is_identifier_allowed(
        cls, identifier, ignore: list[str] = None, is_group=False
    ):
        """
        identifier: value which will be checked against all identifiers
        ignore: list of values which will be ignored
        """
        if is_group:
            return True
        if identifier is None:
            return False
        identifiers = cls.get_existing_ident_values()
        if ignore is not None:
            identifiers = list(filter(lambda i: i not in ignore, identifiers))
        if identifier in identifiers or not identifier:
            return False
        else:
            return True

    @classmethod
    def drop_indication_pos_is_on_item(cls):

        widget = cls.get_class_tree()
        if (
            widget.dropIndicatorPosition()
            == QAbstractItemView.DropIndicatorPosition.OnItem
        ):
            return True
        else:
            return False

    @classmethod
    def get_item_from_pos(cls, pos: QPoint):

        widget = cls.get_class_tree()
        return widget.itemFromIndex(widget.indexAt(pos))

    @classmethod
    def get_selected_items(cls) -> list[QTreeWidgetItem]:
        widget = cls.get_class_tree()
        return widget.selectedItems()

    @classmethod
    def get_class_from_item(cls, item: QTreeWidgetItem) -> SOMcreator.SOMClass:
        return item.data(0, constants.CLASS_REFERENCE)

    @classmethod
    def add_class_activate_function(cls, func: Callable):
        cls.get_properties().class_activate_functions.append(func)

    @classmethod
    def fill_class_entry(cls, som_class: SOMcreator.SOMClass):
        for func in cls.get_properties().class_activate_functions:
            func(som_class)

    @classmethod
    def set_active_class(cls, som_class: SOMcreator.SOMClass):
        prop: ClassProperties = cls.get_properties()
        prop.active_class = som_class
        cls.fill_class_entry(som_class)

    @classmethod
    def update_check_state(cls, item: QTreeWidgetItem):
        som_class: SOMcreator.SOMClass = cls.get_class_from_item(item)
        if not som_class:
            return
        values = [
            [getter_func(som_class), setter_func]
            for n, getter_func, setter_func in cls.get_properties().column_List
        ]
        for column, [value, setter_func] in enumerate(values):
            if setter_func is not None:
                setter_func(item, column)

    @classmethod
    def get_class_tree(cls) -> ClassTreeWidget:
        return tool.MainWindow.get_class_tree_widget()

    @classmethod
    def create_item(cls, som_class: SOMcreator.SOMClass):
        item = QTreeWidgetItem()
        item.setData(0, constants.CLASS_REFERENCE, som_class)
        item.setText(0, som_class.name)
        item.setFlags(
            item.flags()
            | Qt.ItemFlag.ItemIsUserCheckable
            | Qt.ItemFlag.ItemIsSelectable
        )
        values = [
            getter_func(som_class)
            for n, getter_func, setter_func in cls.get_properties().column_List
        ]
        for column, value in enumerate(values):
            if isinstance(value, bool):
                item.setCheckState(column, Qt.CheckState.Unchecked)
        return item

    @classmethod
    def update_item(cls, item: QTreeWidgetItem, som_class: SOMcreator.SOMClass):
        values = [
            getter_func(som_class)
            for n, getter_func, setter_func in cls.get_properties().column_List
        ]

        for column, value in enumerate(values):
            if isinstance(value, bool):
                cs = Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
                if item.checkState(column) != cs:
                    item.setCheckState(column, cs)

            elif item.text(column) != value:
                item.setText(column, value)

    @classmethod
    def fill_class_tree(
        cls, classes: set[SOMcreator.SOMClass], parent_item: QTreeWidgetItem
    ) -> None:
        old_classes_dict = {
            cls.get_class_from_item(parent_item.child(i)): i
            for i in range(parent_item.childCount())
        }
        old_classes = set(old_classes_dict.keys())
        new_classes = classes.difference(old_classes)
        delete_classes = old_classes.difference(classes)
        for som_class in reversed(
            sorted(delete_classes, key=lambda o: old_classes_dict[o])
        ):
            row_index = old_classes_dict[som_class]
            parent_item.removeChild(parent_item.child(row_index))

        for new_classes in sorted(new_classes, key=lambda o: o.name):
            item = cls.create_item(new_classes)
            parent_item.addChild(item)

        for index in range(parent_item.childCount()):
            item = parent_item.child(index)
            som_class: SOMcreator.SOMClass = cls.get_class_from_item(item)
            cls.update_item(item, som_class)
            cls.fill_class_tree(set(som_class.get_children(filter=True)), item)

    @classmethod
    def add_class_creation_check(cls, key, check_function):
        cls.get_properties().class_add_checks.append((key, check_function))

    @classmethod
    def set_class_optional_by_tree_item_state(
        cls, item: QTreeWidgetItem, column_index: int
    ):
        som_class = cls.get_class_from_item(item)
        som_class.set_optional(
            True if item.checkState(column_index) == Qt.CheckState.Checked else False
        )

    @classmethod
    def trigger_class_creation(
        cls,
        data_dict: ClassDataDict,
    ):
        trigger.create_class_called(data_dict)

    @classmethod
    def trigger_class_copy(
        cls, som_class: SOMcreator.SOMClass, data_dict: ClassDataDict
    ):
        trigger.copy_class_called(som_class, data_dict)

    @classmethod
    def trigger_class_modification(
        cls, som_class: SOMcreator.SOMClass, data_dict: ClassDataDict
    ):
        trigger.modify_class_called(som_class, data_dict)

    @classmethod
    def modify_class(
        cls, som_class: SOMcreator.SOMClass, data_dict: ClassDataDict
    ) -> int:
        som_class.name = data_dict.get("name", som_class.name)
        som_class.ifc_mapping = data_dict.get("ifc_mappings", som_class.ifc_mapping)
        som_class.description = data_dict.get("description", "")

        if data_dict.get("is_group"):
            if not som_class.is_concept:
                som_class.identifier_property = str(uuid.uuid4())
            return

        pset_name = data_dict.get("ident_pset_name")
        identifier_name = data_dict.get("ident_property_name")
        if pset_name and identifier_name:
            ident_property = cls.find_property(som_class, pset_name, identifier_name)
            som_class.identifier_property = (
                ident_property or som_class.identifier_property
            )

        ident_value = data_dict.get("ident_value")
        if ident_value is not None:
            cls.set_ident_value(som_class, ident_value)

    @classmethod
    def create_class(
        cls,
        data_dict: ClassDataDict,
        property_set: SOMcreator.SOMPropertySet,
        identifier_property: SOMcreator.SOMProperty,
    ):
        if data_dict.get("is_group", False):
            ident = str(uuid.uuid4())
            new_class = SOMcreator.SOMClass(data_dict["name"], ident, uuid=ident)
        else:
            new_class = SOMcreator.SOMClass(data_dict["name"], identifier_property)
            new_class.add_property_set(property_set)

        new_class.ifc_mapping = data_dict.get("ifc_mappings") or new_class.ifc_mapping
        return new_class

    @classmethod
    def check_class_creation_input(cls, data_dict: ClassDataDict) -> bool:
        prop = cls.get_properties()
        for key, check_function in prop.class_add_checks:
            if not check_function(data_dict):
                return False
        return True

    @classmethod
    def write_classes_to_mimedata(
        cls, classes: list[SOMcreator.SOMClass], mime_data: QMimeData
    ):
        serialized = pickle.dumps(classes)
        mime_data.setData(constants.MIME_DATA_KEY, QByteArray(serialized))

    @classmethod
    def get_classes_from_mimedata(
        cls, mime_data: QMimeData
    ) -> list[SOMcreator.SOMClass]:
        serialized = mime_data.data(constants.MIME_DATA_KEY)
        if not serialized:
            return None
        return pickle.loads(serialized)

    @classmethod
    def handle_class_move(cls, dropped_on_item: QTreeWidgetItem):
        selected_items = cls.get_selected_items()
        dropped_classes = [cls.get_class_from_item(item) for item in selected_items]
        dropped_classes = [
            o
            for o in dropped_classes
            if o.parent not in dropped_classes or o.parent is None
        ]
        if dropped_on_item is None:
            for som_class in dropped_classes:
                som_class.remove_parent()
            return
        dropped_on_class = cls.get_class_from_item(dropped_on_item)

        if not cls.drop_indication_pos_is_on_item():
            dropped_on_class = dropped_on_class.parent

        for som_class in dropped_classes:
            if dropped_on_class is None:
                som_class.remove_parent()
            else:
                som_class.parent = dropped_on_class
