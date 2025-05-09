from __future__ import annotations

import copy as cp
import logging
import uuid
from typing import Callable, TYPE_CHECKING, TypedDict

from PySide6.QtCore import (
    QPoint,
    Qt,
    QMimeData,
    QByteArray,
    QObject,
    QCoreApplication,
    Signal,
    QModelIndex,
    QItemSelection,
)
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
    from som_gui.module.class_.prop import ClassDataDict
from som_gui.module.class_tree import ui


class Signaller(QObject):
    search = Signal(ui.ClassView)
    selected_class_changed = Signal(ui.ClassView, SOMcreator.SOMClass)
    request_class_deletion = Signal(SOMcreator.SOMClass, bool)
    request_group_selection = Signal(ui.ClassView)


class ClassTree(som_gui.core.tool.ClassTree):
    signaller = Signaller()

    @classmethod
    def get_properties(cls) -> ClassTreeProperties:
        return som_gui.ClassTreeProperties

    @classmethod
    def connect_trigger(cls):
        cls.signaller.search.connect(trigger.search_class)
        cls.signaller.request_group_selection.connect(trigger.group_selection)

    @classmethod
    def reset_tree(cls, tree: ui.ClassView):
        tree.model().reset_required.emit("tool.class_tree.reset_tree")

    @classmethod
    def get_trees(cls) -> set[ui.ClassView]:
        return cls.get_properties().existing_trees

    @classmethod
    def add_tree(cls, tree: ui.ClassView):
        cls.get_properties().existing_trees.add(tree)
        cls.get_properties().context_menu_list[tree] = list()
        cls.set_column_list(tree, [])

    @classmethod
    def connect_tree(cls, tree: ui.ClassView):
        model = tree.model()
        sort_model = tree.sort_model()
        tree.update_requested.connect(tree.update_view)

        def trigger_selection(selected: QItemSelection, deselected: QItemSelection):
            for index in selected.indexes():
                index = sort_model.mapToSource(index) if sort_model else index
                tree.selected_class_changed.emit(index.internalPointer())
                return

        def trigger_double(index: QModelIndex):
            index = sort_model.mapToSource(index) if sort_model else index
            tree.class_double_clicked.emit(index.internalPointer())

        tree.selectionModel().selectionChanged.connect(trigger_selection)
        tree.doubleClicked.connect(trigger_double)
        tree.customContextMenuRequested.connect(
            lambda p: trigger.create_context_menu(tree, p)
        )
        tree.expanded.connect(lambda: cls.resize_tree(tree))

    @classmethod
    def remove_tree(cls, tree: ui.ClassView):
        cls.get_properties().existing_trees.remove(tree)
        cls.get_properties().context_menu_list.pop(tree)

    @classmethod
    def add_column_to_tree(
        cls,
        tree: ui.ClassView,
        name_getter,
        logical_index,
        getter_func,
        setter_func=None,
        role=Qt.ItemDataRole.DisplayRole,
    ):
        if tree not in cls.get_trees():
            return
        if setter_func is None:
            setter_func = lambda *a: None
        model = tree.model()
        if logical_index < 0:
            logical_index = model.old_column_count + logical_index
        model.insertColumn(
            logical_index, QModelIndex(), (name_getter, getter_func, setter_func, role)
        )

    @classmethod
    def remove_column_from_tree(cls, tree: ui.ClassView, column_name: str):
        header_texts = cls.get_header_names(tree)
        column_index = header_texts.index(column_name)
        tree.model().removeColumn(column_index)

    @classmethod
    def get_header_names(cls, tree: ui.ClassView) -> list[str]:
        return [x[0]() for x in cls.get_column_list(tree) or []]

    @classmethod
    def create_completer(cls, texts, widget: QLineEdit | QComboBox):
        completer = QCompleter(texts)
        widget.setCompleter(completer)

    @classmethod
    def expand_to_class(cls, tree: ui.ClassView, som_class: SOMcreator.SOMClass):
        parent_list = [som_class]
        parent = som_class.parent
        model = tree.model()
        while parent is not None:
            parent_list.append(parent)
            parent = parent.parent
        # needs to happen top down. DataModel creates children only if parent is already created
        # You can't combine the parent search with expanding the Tree it needs to happen in two steps
        for item in reversed(parent_list):
            index: QModelIndex = model.class_index_dict.get(item)
            if sort_model := tree.sort_model():
                index = sort_model.mapFromSource(index)
            tree.expand(index)
        flags = (
            tree.selectionModel().SelectionFlag.ClearAndSelect
            | tree.selectionModel().SelectionFlag.Rows
        )
        tree.selectionModel().select(index, flags)
        tree.scrollTo(index.sibling(index.row(), 0), tree.ScrollHint.EnsureVisible)

    @classmethod
    def resize_tree(cls, tree: ui.ClassView):
        for col in reversed(range(tree.model().columnCount())):
            tree.resizeColumnToContents(col)

    @classmethod
    def group_classes(
        cls, parent: SOMcreator.SOMClass, children: set[SOMcreator.SOMClass]
    ):
        for child in children:
            parent.add_child(child)
        for tree in cls.get_trees():
            tree.update_requested.emit()

    @classmethod
    def create_context_menu(cls, tree: ui.ClassView):
        menu = QMenu()
        prop = cls.get_properties()
        selected_indexes = cls.get_selected(tree)
        menu_list = prop.context_menu_list[tree]
        if len(selected_indexes) < 1:
            menu_list = filter(lambda d: not d["on_selection"], menu_list)
        elif len(selected_indexes) == 1:
            menu_list = filter(lambda d: d["on_single_select"], menu_list)
        elif len(selected_indexes) > 1:
            menu_list = filter(lambda d: d["on_multi_select"], menu_list)
        for menu_entry in menu_list:
            menu_entry["action"] = menu.addAction(menu_entry["name_getter"]())
            menu_entry["action"].triggered.connect(menu_entry["function"])
        return menu

    @classmethod
    def get_selected_classes(cls, tree: ui.ClassView) -> list[SOMcreator.SOMClass]:
        selected_indexes = cls.get_selected(tree)
        return [cls.get_class_from_index(index) for index in selected_indexes]

    @classmethod
    def delete_selection(cls, tree: ui.ClassView):
        som_classes = cls.get_selected_classes(tree)
        delete_request, recursive_deletion = tool.Popups.req_delete_items(
            [som_class.name for som_class in som_classes], item_type=1
        )
        if not delete_request:
            return
        for som_class in som_classes:
            cls.signaller.request_class_deletion.emit(som_class, recursive_deletion)

    @classmethod
    def expand_selection(cls, tree: ui.ClassView):
        for index in tree.selectedIndexes():
            tree.expandRecursively(index)

    @classmethod
    def collapse_selection(cls, tree: ui.ClassView):
        for index in cls.get_selected(tree):
            tree.collapse(index)

    @classmethod
    def clear_context_menu_list(cls, tree: ui.ClassView):
        prop = cls.get_properties()
        prop.context_menu_list[tree] = list()

    @classmethod
    def add_context_menu_entry(
        cls,
        tree: ui.ClassView,
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
    def is_drop_indication_pos_on_item(cls, tree: ui.ClassView):

        if (
            tree.dropIndicatorPosition()
            == QAbstractItemView.DropIndicatorPosition.OnItem
        ):
            return True
        else:
            return False

    @classmethod
    def get_index_from_pos(cls, tree: ui.ClassView, pos: QPoint) -> QModelIndex:
        return tree.indexAt(pos)

    @classmethod
    def get_selected(cls, tree: ui.ClassView) -> list[QModelIndex]:
        indexes = [
            i for i in tree.selectionModel().selectedIndexes() if i.column() == 0
        ]
        if not indexes:
            return indexes
        model = indexes[0].model()
        return [model.mapToSource(i) for i in indexes]

    @classmethod
    def get_class_from_index(cls, index: QModelIndex) -> SOMcreator.SOMClass:
        model = index.model()
        if not isinstance(model, ui.ClassModel):
            index = model.mapToSource(index)
        return index.internalPointer()

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
    def handle_class_move(cls, tree: ui.ClassView, dropped_on_index=QModelIndex()):
        model = tree.model()
        selected_indexes = cls.get_selected(tree)
        dropped_classes = {
            cls.get_class_from_index(index): index for index in selected_indexes
        }
        dropped_classes = {
            o: index
            for o, index in dropped_classes.items()
            if o.parent not in dropped_classes or o.parent is None
        }

        if not cls.is_drop_indication_pos_on_item(tree):
            dropped_on_index = dropped_on_index.parent()

        if sort_model := tree.sort_model():
            dropped_on_index = sort_model.mapToSource(dropped_on_index)

        for som_class, index in dropped_classes.items():
            model.moveRow(
                index.parent(),
                index.row(),
                dropped_on_index,
                model.rowCount(dropped_on_index),
            )

    @classmethod
    def get_column_list(
        cls, tree: ui.ClassView
    ) -> list[tuple[Callable, Callable, Callable]]:
        model = tree.model()
        if model is None:
            return None
        return model.columns

    @classmethod
    def set_column_list(
        cls, tree: ui.ClassView, value: list[tuple[Callable, Callable, Callable]]
    ):
        model = tree.model()
        if model is None:
            return None
        model.columns = value

    @classmethod
    def insert_row_by_class(cls, tree: ui.ClassView, som_class: SOMcreator.SOMClass):
        model = tree.model()
        parent = som_class.parent
        if not parent:
            parent_index = QModelIndex()
            insert_row_index = model.get_row_count(QModelIndex())
            model.root_classes.append(som_class)
            logging.info(f"INsert at {insert_row_index}")
            model.insertRow(insert_row_index)
        else:
            parent_index = model.class_index_dict.get(parent)
            if not parent_index:
                return
            insert_row_index = model.get_row_count(parent_index) - 1
            model.insertRow(insert_row_index, parent_index)
        tree.update_requested.emit()

    @classmethod
    def remove_row_by_class(cls, tree: ui.ClassView, som_class: SOMcreator.SOMClass):
        model = tree.model()
        parent = som_class.parent
        class_index = model.class_index_dict.get(som_class)
        if not class_index:
            return
        if not parent:
            if not som_class in model.root_classes:
                return
            parent_index = QModelIndex()
        else:
            parent_index = model.class_index_dict.get(parent)
            if not parent_index:
                return
        for child_logical_index in reversed(range(model.get_row_count(class_index))):
            model.moveRow(
                class_index,
                child_logical_index,
                parent_index,
                model.get_row_count(parent_index),
            )

        model.class_index_dict.pop(som_class)
        model.row_count_dict[class_index] = 0
        model.removeRow(class_index.row(), parent_index)
