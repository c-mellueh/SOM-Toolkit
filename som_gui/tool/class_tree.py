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
import som_gui.module.class_tree
from som_gui.module.class_tree import trigger, constants

if TYPE_CHECKING:
    from som_gui.module.class_tree.prop import ClassTreeProperties, ContextMenuDict
    from som_gui.module.class_tree.ui import ClassTreeWidget
    from som_gui.module.class_.prop import ClassDataDict
    from som_gui.module.class_tree import ui


class ClassTree(som_gui.core.tool.ClassTree):
    @classmethod
    def get_properties(cls) -> ClassTreeProperties:
        return som_gui.ClassTreeProperties

    @classmethod
    def reset_tree(cls,tree: ui.ClassTreeWidget):
        cls.set_first_paint(tree,False)
    @classmethod
    def get_trees(cls) -> set[ui.ClassTreeWidget]:
        return cls.get_properties().existing_trees

    @classmethod
    def add_tree(cls, tree: ui.ClassTreeWidget):
        cls.get_properties().existing_trees.add(tree)
        cls.get_properties().active_class[tree] = None
        cls.get_properties().context_menu_list[tree] = list()
        cls.get_properties().first_paint[tree] = True
        cls.set_column_list(tree,[])

    @classmethod
    def remove_tree(cls, tree: ui.ClassTreeWidget):
        cls.get_properties().existing_trees.remove(tree)
        cls.get_properties().active_class.pop(tree)
        cls.get_properties().context_menu_list.pop(tree)
        cls.get_properties().first_paint.pop(tree)
        cls.get_properties().column_List.pop(tree)

    @classmethod
    def is_first_paint(cls, tree: ui.ClassTreeWidget):
        return cls.get_properties().first_paint[tree]

    @classmethod
    def set_first_paint(cls, tree: ui.ClassTreeWidget, value: bool):
        cls.get_properties().first_paint[tree] = value

    @classmethod
    def add_column_to_tree(
        cls, tree: ui.ClassTreeWidget, name_getter, index, getter_func, setter_func=None
    ):
        if tree not in cls.get_trees():
            return

        cl = cls.get_column_list(tree)
        cl.insert(index, (name_getter, getter_func, setter_func))
        cls.set_column_list(tree,cl)

        header_texts = cls.get_header_names(tree)
        tree.setColumnCount(tree.columnCount() + 1)
        for col, name in enumerate(header_texts):
            tree.headerItem().setText(col, name)
        cls.reset_tree(tree)

    @classmethod
    def remove_column_from_tree(cls, tree: ui.ClassTreeWidget, column_name: str):
        header = tree.headerItem()
        header_texts = cls.get_header_names(tree)
        column_index = header_texts.index(column_name)
        cls.get_column_list(tree).pop(column_index)
        tree.setColumnCount(tree.columnCount() - 1)
        header_texts.pop(column_index)
        for col, name in enumerate(header_texts):
            header.setText(col, name)
        cls.reset_tree(tree)

    @classmethod
    def get_header_names(cls, tree: ui.ClassTreeWidget) -> list[str]:
        return [x[0]() for x in cls.get_column_list(tree) or []]

    @classmethod
    def create_completer(cls, texts, widget: QLineEdit | QComboBox):
        completer = QCompleter(texts)
        widget.setCompleter(completer)

    @classmethod
    def get_item_from_class(
        cls, tree: ui.ClassTreeWidget, som_class: SOMcreator.SOMClass
    ) -> QTreeWidgetItem:
        def iter_tree(item: QTreeWidgetItem):
            for child_index in range(item.childCount()):
                child = item.child(child_index)
                if cls.get_class_from_item(child) == som_class:
                    return child
                result = iter_tree(child)
                if result is not None:
                    return result
            return None

        return iter_tree(tree.invisibleRootItem())

    @classmethod
    def select_class(
        cls, tree: ui.ClassTreeWidget, som_class: SOMcreator.SOMClass
    ) -> None:
        item = cls.get_item_from_class(tree, som_class)
        if item is None:
            return
        for selected_item in cls.get_selected(tree):
            selected_item.setSelected(False)
        item.setSelected(True)
        cls.expand_to_item(item)
        tree.scrollToItem(item)

    @classmethod
    def expand_to_item(cls, item: QTreeWidgetItem):
        item.setExpanded(True)
        if item.parent() is not None:
            cls.expand_to_item(item.parent())

    @classmethod
    def resize_tree(cls, tree: ui.ClassTreeWidget):
        for col in reversed(range(tree.columnCount())):
            tree.resizeColumnToContents(col)

    @classmethod
    def group_classes(
        cls, parent: SOMcreator.SOMClass, children: set[SOMcreator.SOMClass]
    ):
        for child in children:
            parent.add_child(child)

    @classmethod
    def create_context_menu(cls, tree: ui.ClassTreeWidget):
        menu = QMenu()
        prop = cls.get_properties()
        selected_items = cls.get_selected(tree)
        menu_list = prop.context_menu_list[tree]
        if len(selected_items) < 1:
            menu_list = filter(lambda d: not d["on_selection"], menu_list)
        elif len(selected_items) == 1:
            menu_list = filter(lambda d: d["on_single_select"], menu_list)
        elif len(selected_items) > 1:
            menu_list = filter(lambda d: d["on_multi_select"], menu_list)
        for menu_entry in menu_list:
            menu_entry["action"] = menu.addAction(menu_entry["name_getter"]())
            menu_entry["action"].triggered.connect(menu_entry["function"])
        return menu

    @classmethod
    def get_selected_classes(
        cls, tree: ui.ClassTreeWidget
    ) -> list[SOMcreator.SOMClass]:
        selected_items = cls.get_selected(tree)
        return [cls.get_class_from_item(item) for item in selected_items]

    @classmethod
    def delete_class(cls, som_class: SOMcreator.SOMClass, recursive: bool = False):
        som_class.delete(recursive)

    @classmethod
    def delete_selection(cls, tree: ui.ClassTreeWidget):
        som_classes = cls.get_selected_classes(tree)
        delete_request, recursive_deletion = tool.Popups.req_delete_items(
            [som_class.name for som_class in som_classes], item_type=1
        )
        if not delete_request:
            return
        for som_class in som_classes:
            cls.delete_class(som_class, recursive_deletion)

    @classmethod
    def expand_selection(cls, tree: ui.ClassTreeWidget):
        for index in tree.selectedIndexes():
            tree.expandRecursively(index)

    @classmethod
    def collapse_selection(cls, tree: ui.ClassTreeWidget):
        for item in cls.get_selected(tree):
            tree.collapseItem(item)

    @classmethod
    def group_selection(cls, tree: ui.ClassTreeWidget):
        trigger.group_selection(tree)

    @classmethod
    def clear_context_menu_list(cls, tree: ui.ClassTreeWidget):
        prop = cls.get_properties()
        prop.context_menu_list[tree] = list()

    @classmethod
    def add_context_menu_entry(
        cls,
        tree: ui.ClassTreeWidget,
        name_getter: Callable,
        function: Callable,
        on_selection: bool,
        single: bool,
        multi: bool,
    ) -> ContextMenuDict:
        """
        Adds an entry to the context menu.

        :param name_getter: A callable that returns the name for the context menu entry.
        :param function: A callable that defines the function to be executed when the context menu entry is selected.
        :param on_selection: A boolean indicating if the entry shold be only availible if class is selected
        :param single: A boolean indicating if the entry should be available for single selection.
        :param multi: A boolean indicating if the entry should be available for multi-selection.
        :return: A dictionary representing the context menu entry.
        :rtype: ContextMenuDict
        """
        d: ContextMenuDict = dict()
        d["name_getter"] = name_getter
        d["function"] = function
        d["on_multi_select"] = multi
        d["on_single_select"] = single
        d["on_selection"] = on_selection
        prop = cls.get_properties()
        prop.context_menu_list[tree].append(d)
        return d



    @classmethod
    def is_drop_indication_pos_on_item(cls, tree: ui.ClassTreeWidget):

        if (
            tree.dropIndicatorPosition()
            == QAbstractItemView.DropIndicatorPosition.OnItem
        ):
            return True
        else:
            return False

    @classmethod
    def get_item_from_pos(cls, tree: ui.ClassTreeWidget, pos: QPoint):
        return tree.itemFromIndex(tree.indexAt(pos))

    @classmethod
    def get_selected(cls, tree: ui.ClassTreeWidget) -> list[QTreeWidgetItem]:
        return tree.selectedItems()

    @classmethod
    def get_class_from_item(cls, item: QTreeWidgetItem) -> SOMcreator.SOMClass:
        return item.data(0, constants.CLASS_REFERENCE)

    @classmethod
    def update_check_state(cls, tree: ui.ClassTreeWidget, item: QTreeWidgetItem):
        som_class: SOMcreator.SOMClass = cls.get_class_from_item(item)
        if not som_class:
            return
        values = [
            [getter_func(som_class), setter_func]
            for n, getter_func, setter_func in cls.get_column_list(tree)
        ]
        for column, [value, setter_func] in enumerate(values):
            if setter_func is not None:
                setter_func(item, column)

    @classmethod
    def create_item(cls,tree:ui.ClassTreeWidget, som_class: SOMcreator.SOMClass):
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
            for n, getter_func, setter_func in cls.get_column_list(tree)
        ]
        for column, value in enumerate(values):
            if isinstance(value, bool):
                item.setCheckState(column, Qt.CheckState.Unchecked)
        return item

    @classmethod
    def update_item(cls,tree:ui.ClassTreeWidget, item: QTreeWidgetItem, som_class: SOMcreator.SOMClass):
        values = [
            getter_func(som_class)
            for n, getter_func, setter_func in cls.get_column_list(tree)
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
        cls,tree:ui.ClassTreeWidget, classes: set[SOMcreator.SOMClass], parent_item: QTreeWidgetItem
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
            item = cls.create_item(tree,new_classes)
            parent_item.addChild(item)

        for index in range(parent_item.childCount()):
            item = parent_item.child(index)
            som_class: SOMcreator.SOMClass = cls.get_class_from_item(item)
            cls.update_item(tree,item, som_class)
            cls.fill_class_tree(tree,set(som_class.get_children(filter=True)), item)

    @classmethod
    def set_class_optional_by_tree_item_state(
        cls, item: QTreeWidgetItem, column_index: int
    ):
        som_class = cls.get_class_from_item(item)
        som_class.set_optional(
            True if item.checkState(column_index) == Qt.CheckState.Checked else False
        )

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
    def handle_class_move(
        cls, tree: ui.ClassTreeWidget, dropped_on_item: QTreeWidgetItem
    ):
        selected_items = cls.get_selected(tree)
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

        if not cls.is_drop_indication_pos_on_item(tree):
            dropped_on_class = dropped_on_class.parent

        for som_class in dropped_classes:
            if dropped_on_class is None:
                som_class.remove_parent()
            else:
                som_class.parent = dropped_on_class
    @classmethod
    def trigger_tree_init(cls,tree: ui.ClassTreeWidget):
        trigger.init_tree(tree)
    @classmethod
    def trigger_search(cls,tree: ui.ClassTreeWidget):
        trigger.search_class(tree)

    @classmethod
    def get_column_list(cls,tree:ui.ClassTreeWidget) ->list[tuple[Callable, Callable, Callable]] :
        return cls.get_properties().column_List[tree]
    @classmethod
    def set_column_list(cls,tree:ui.ClassTreeWidget,value):
        cls.get_properties().column_List[tree] = value