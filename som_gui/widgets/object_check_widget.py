from __future__ import annotations

from typing import TYPE_CHECKING

import SOMcreator
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QStandardItem, QFont, QStandardItemModel
from PySide6.QtWidgets import QWidget, QTreeView, QTreeWidget
from SOMcreator import classes

from .. import icons
from ..qt_designs import ui_object_check_widget

if TYPE_CHECKING:
    from ..main_window import MainWindow

OBJECT_DATA_INDEX = 1312
OBJECT_ITEM_INDEX = 161


def checkstate_to_bool(check_state: Qt.CheckState) -> bool:
    return True if check_state == Qt.CheckState.Checked else False


class ObjectCheckWidget(QWidget):

    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            obj_tree = self.widget.object_tree
            pset_tree = self.widget.property_set_tree
            obj_tree.selectionModel().selectionChanged.connect(self.object_selection_changed)
            obj_tree.model().dataChanged.connect(self.update_data_model)

            pset_tree.expanded.connect(lambda: resize_tree_view(pset_tree))
            self.tree_model.itemChanged.connect(self.update_data_model)

        self.main_window = main_window
        super(ObjectCheckWidget, self).__init__(main_window)
        self.widget = ui_object_check_widget.Ui_Form()
        self.widget.setupUi(self)
        self.tree_model = PropertySetModel(main_window.project)
        self.object_model = ObjectModel(main_window.project)
        self.widget.property_set_tree.setModel(self.tree_model)
        self.setWindowIcon(icons.get_icon())
        self.data_model: dict[classes.Object | classes.PropertySet | classes.Attribute, bool] = dict()
        self.reset()
        connect()

    def reset(self) -> None:
        self.main_window.modelcheck_window = self
        self.tree_model.clear()
        self.data_model = self.fill_data_model()
        self.fill_object_tree()
        self.widget.label_object.hide()

    def resize_to_content(self) -> None:
        """resizes Tree to content so it allways looks fresh and tidy"""
        resize_tree(self.widget.object_tree)
        resize_tree_view(self.widget.property_set_tree)

    def fill_object_tree(self):
        def iter_objects(obj: SOMcreator.Object, parent_item):
            if obj.parent is not None:
                is_enabled = self.data_model[obj]
            else:
                is_enabled = True
            is_checked = self.data_model[obj]
            object_item = CheckBoxItem(obj, is_checked, is_enabled)
            parent_item.appendRow([object_item, IdentItem(obj)])

            for child in obj.children:
                iter_objects(child, object_item)

        tree = self.widget.object_tree
        self.object_model.clear()
        root = self.object_model.invisibleRootItem()
        tree.setModel(self.object_model)

        for o in self.main_window.project.objects:
            if o.parent is None:
                iter_objects(o, root)

        resize_tree_view(tree)
        tree.expandAll()

    def object_selection_changed(self):
        tree = self.widget.object_tree
        index = tree.selectionModel().selectedIndexes()[0].siblingAtColumn(0)
        obj = index.data(OBJECT_DATA_INDEX)
        self.widget.label_object.show()
        self.widget.label_object.setText(f"{obj.name} ({obj.ident_value})")
        self.fill_property_set_tree(obj)

    def fill_property_set_tree(self, selected_object: classes.Object):
        tree = self.widget.property_set_tree
        self.tree_model.clear()
        root = self.tree_model.invisibleRootItem()
        tree.setModel(self.tree_model)
        for property_set in selected_object.get_all_property_sets():
            pset_is_enabled = self.data_model[selected_object]
            pset_is_checked = self.data_model[property_set]
            pset_item = CheckBoxItem(property_set, pset_is_checked, pset_is_enabled)
            root.appendRow([pset_item])
            for attribute in property_set.get_all_attributes():
                pset_is_enabled = self.data_model[selected_object]
                attribute_is_enabled = self.data_model[property_set]
                attribute_is_checked = self.data_model[attribute]
                attribute_row = [
                    CheckBoxItem(attribute, attribute_is_checked, all((attribute_is_enabled, pset_is_enabled)))]
                pset_item.appendRow(attribute_row)
        resize_tree_view(tree)
        tree.expandAll()

    def update_data_model(self, model_index: QModelIndex):

        def modify_checkbox_data():
            self.data_model[data] = new_checkstate
            if isinstance(data, SOMcreator.PropertySet):
                for index in range(tree_item.rowCount()):
                    tree_item.child(index, model_index.column()).setEnabled(new_checkstate)

        tree_item = model_index.data(OBJECT_ITEM_INDEX)
        if tree_item is None:
            return
        new_checkstate = checkstate_to_bool(tree_item.checkState())
        data = model_index.data(OBJECT_DATA_INDEX)

        if isinstance(data, SOMcreator.Object):
            self.object_checked(tree_item)

        elif isinstance(tree_item, CheckBoxItem):
            modify_checkbox_data()

    def fill_data_model(self) -> dict:
        def add_to_model(entity: classes.Object | classes.PropertySet | classes.Attribute) -> None:
            data_model[entity] = True

        project = self.main_window.project
        data_model = dict()
        for obj in project.get_all_objects():
            add_to_model(obj)
            for pset in obj.get_all_property_sets():
                add_to_model(pset)
                for attribute in pset.get_all_attributes():
                    add_to_model(attribute)
        return data_model

    def object_checked(self, object_item: CheckBoxItem):
        def iter_child(item):
            for index in range(item.rowCount()):
                child = item.child(index, item.index().column())
                ident = item.child(index, item.index().column() + 1)
                ident.setEnabled(new_check_state)
                child.setEnabled(new_check_state)
                iter_child(child)

        data = object_item.data(OBJECT_DATA_INDEX)
        new_check_state = checkstate_to_bool(object_item.checkState())
        self.data_model[data] = new_check_state
        iter_child(object_item)
        self.fill_property_set_tree(data)


def resize_tree_view(tree: QTreeView):
    columns = tree.model().columnCount()
    for index in range(columns):
        tree.resizeColumnToContents(index)


def resize_tree(tree: QTreeWidget):
    for index in range(tree.columnCount()):
        tree.resizeColumnToContents(index)


class ObjectModel(QStandardItemModel):
    def __init__(self, project: classes.Project):
        super(ObjectModel, self).__init__()
        self.project = project

    def clear(self) -> None:
        super(ObjectModel, self).clear()
        self.setHorizontalHeaderLabels(["Objekt", "Identifier"])


class PropertySetModel(QStandardItemModel):
    def __init__(self, project: classes.Project):
        super(PropertySetModel, self).__init__()
        self.project = project

    def clear(self) -> None:
        super(PropertySetModel, self).clear()
        self.setHorizontalHeaderLabels(["PropertySet, Attribut"])


class CheckBoxItem(QStandardItem):
    def __init__(self, data: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute, is_checked: bool,
                 is_enabled: bool):
        super(CheckBoxItem, self).__init__()
        check_state = Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked
        self.setCheckState(check_state)
        self.setCheckable(True)
        self.setEnabled(is_enabled)
        self.setEditable(False)

        if isinstance(data, SOMcreator.PropertySet):
            font = QFont()
            font.setBold(True)
            self.setFont(font)

        self.setText(data.name)
        self.setData(data, OBJECT_DATA_INDEX)
        self.setData(self, OBJECT_ITEM_INDEX)


class IdentItem(QStandardItem):
    def __init__(self, obj: classes.Object):
        super(IdentItem, self).__init__()
        self.setText(obj.ident_value)
