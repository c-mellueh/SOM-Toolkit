from __future__ import annotations

import os
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QTreeWidgetItem, QMenu, QMainWindow, QFileDialog
from SOMcreator import classes, revit, json_constants, value_constants

from .. import icons
from ..qt_designs import ui_mapping_window
from ..widgets import object_widget
from ..windows import popups

if TYPE_CHECKING:
    from ..main_window import MainWindow


class MappingWindow(QMainWindow):

    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            self.pset_tree.itemDoubleClicked.connect(pset_double_clicked)
            self.object_tree.itemDoubleClicked.connect(self.object_double_clicked)
            self.object_tree.itemClicked.connect(self.object_clicked)
            self.object_tree.itemChanged.connect(item_checked)
            self.pset_tree.itemChanged.connect(item_checked)
            self.object_tree.customContextMenuRequested.connect(self.object_context_menu)
            self.widget.action_ifc.triggered.connect(self.export_if_mapping)
            self.widget.action_shared_parameters.triggered.connect(self.export_shared_parameters)

        super().__init__()

        self.widget = ui_mapping_window.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.setWindowTitle("Mapping Window")
        self.main_window = main_window
        self.pset_tree = self.widget.pset_tree
        self.object_tree = self.widget.object_tree
        self.object_name_label = self.widget.label_object_name
        self.export_folder = None

        self._active_object_item: None | object_widget.CustomObjectTreeItem = None
        self.active_object: None | classes.Object = None
        self.pset_trees: dict[classes.Object:list[PsetTreeItem]] = dict()

        self.object_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        connect()
        self.fill_object_table()
        attrib: classes.Attribute

    @property
    def active_object_item(self) -> object_widget.CustomObjectTreeItem:
        return self._active_object_item

    @active_object_item.setter
    def active_object_item(self, value: object_widget.CustomObjectTreeItem) -> None:
        self._active_object_item = value
        self.active_object = value.object
        self.object_name_label.setText(self.active_object.name)

    def fill_object_table(self) -> None:
        def copy_children(orig_item: object_widget.CustomObjectTreeItem, new_item: ObjectTreeItem):
            for index in range(orig_item.childCount()):
                child = orig_item.child(index)
                new_child = ObjectTreeItem(child.object)
                new_item.addChild(new_child)
                copy_children(child, new_child)

                if child.object.mapping_dict[json_constants.IFC_MAPPING]:
                    new_child.setCheckState(0, Qt.Checked)
                else:
                    new_child.setCheckState(0, Qt.Unchecked)

        orig_root = self.main_window.object_tree.invisibleRootItem()
        new_root = self.object_tree.invisibleRootItem()
        copy_children(orig_root, new_root)

    def object_clicked(self, item: object_widget.CustomObjectTreeItem):
        self.active_object_item = item
        if self.pset_trees.get(self.active_object) is None:
            self.new_pset_table(item.object)
        else:
            self.fill_pset_table(self.pset_trees[self.active_object])

    def clear_pset_tree(self):
        root = self.pset_tree.invisibleRootItem()
        for i in reversed(range(root.childCount())):
            root.removeChild(root.child(i))

    def new_pset_table(self, _object: classes.Object) -> None:
        self.clear_pset_tree()
        root = self.pset_tree.invisibleRootItem()

        self.pset_trees[_object] = list()
        for pset in _object.property_sets:
            pset_item = PsetTreeItem(pset)
            root.addChild(pset_item)
            self.pset_trees[_object].append(pset_item)
            for attribute in pset.attributes:
                AttributeTreeItem(pset_item, attribute)
            if pset.mapping_dict[json_constants.IFC_MAPPING]:
                pset_item.setCheckState(0, Qt.Checked)
            else:
                pset_item.setCheckState(0, Qt.Unchecked)

    def fill_pset_table(self, pset_list: list[PsetTreeItem]) -> None:
        self.clear_pset_tree()
        root = self.pset_tree.invisibleRootItem()
        for pset_item in pset_list:
            root.addChild(pset_item)

    def object_context_menu(self, position: QPoint) -> None:

        def recursive_expand(item: object_widget.CustomObjectTreeItem, expand: bool):
            item.setExpanded(expand)
            for i in range(item.childCount()):
                child = item.child(i)
                recursive_expand(child, expand)

        def expand_objects():
            for root_items in selected_items:
                recursive_expand(root_items, True)

        def collaps_objects():
            for root_items in selected_items:
                recursive_expand(root_items, False)

        def check_objects():
            for item in selected_items:
                item.setCheckState(0, Qt.Checked)

        def uncheck_objects():
            for item in selected_items:
                item.setCheckState(0, Qt.Unchecked)

        def modify_ifc_mapping():
            item = selected_items[0]
            self.object_double_clicked(item)

        menu = QMenu()

        selected_items = self.object_tree.selectedItems()
        action_expand = menu.addAction("Expand")
        action_collapse = menu.addAction("Collapse")
        action_check = menu.addAction("Check")
        action_uncheck = menu.addAction("Uncheck")
        if len(selected_items) == 1:
            action_modify_ifc = menu.addAction("Modify IFC Mapping")
            action_modify_ifc.triggered.connect(modify_ifc_mapping)

        action_expand.triggered.connect(expand_objects)
        action_collapse.triggered.connect(collaps_objects)
        action_check.triggered.connect(check_objects)
        action_uncheck.triggered.connect(uncheck_objects)
        menu.exec(self.object_tree.viewport().mapToGlobal(position))

    def get_export_data(self) -> (str, dict[str, (list[classes.Attribute], set[str])]):
        def iterate(item: object_widget.CustomObjectTreeItem):
            nonlocal pset_dict

            def compare_property_sets():
                for property_set in child.object.property_sets:
                    if property_set.mapping_dict[json_constants.IFC_MAPPING]:
                        if pset_dict.get(property_set.name) is None:
                            saved_attributes: list[classes.Attribute] = list()
                            for attribute in property_set.attributes:
                                if attribute.mapping_dict[json_constants.IFC_MAPPING]:
                                    saved_attributes.append(attribute)
                            ifc_mapping = child.object.ifc_mapping
                        else:
                            (saved_attributes, ifc_mapping) = pset_dict.get(property_set.name)
                            for attribute in property_set.attributes:
                                mapping_bool = attribute.mapping_dict[json_constants.IFC_MAPPING]
                                if attribute.name not in [x.name for x in saved_attributes] and mapping_bool:
                                    saved_attributes.append(attribute)
                            ifc_mapping = set.union(ifc_mapping, child.object.ifc_mapping)

                        pset_dict[property_set.name] = (saved_attributes, ifc_mapping)

            for index in range(item.childCount()):
                child = item.child(index)
                if child.checkState(0) == Qt.Checked:
                    compare_property_sets()
                    iterate(child)

        pset_dict: dict[str, (list[classes.Attribute], set[str])] = dict()

        root = self.object_tree.invisibleRootItem()
        iterate(root)

        file_text = "txt Files (*.txt);;"
        if self.export_folder is None:
            self.export_folder = str(os.getcwd() + "/")
        path = QFileDialog.getSaveFileName(self, "Safe IFC Template", self.export_folder, file_text)[0]
        return path, pset_dict

    def export_if_mapping(self):
        path, pset_dict = self.get_export_data()
        if path:
            revit.export_ifc_template(path, pset_dict)

    def export_shared_parameters(self) -> None:
        path, pset_dict = self.get_export_data()
        if path:
            revit.export_shared_parameters(path, pset_dict)

    def object_double_clicked(self, item: ObjectTreeItem) -> None:
        object_widget.object_double_clicked(self.main_window, item.object)


class ObjectTreeItem(QTreeWidgetItem):
    def __init__(self, obj: classes.Object, parent: QTreeWidgetItem | ObjectTreeItem = None) -> None:
        if parent is None:
            super(ObjectTreeItem, self).__init__()
        else:
            super(ObjectTreeItem, self).__init__(parent)
        self.object = obj
        self.update()

    def update(self) -> None:
        self.setText(0, self.object.name)
        self.setText(1, ";".join(self.object.ifc_mapping))


class PsetTreeItem(QTreeWidgetItem):
    def __init__(self, property_set: classes.PropertySet, parent: QTreeWidgetItem | PsetTreeItem = None) -> None:

        if parent is None:
            super(PsetTreeItem, self).__init__()
        else:
            super(PsetTreeItem, self).__init__(parent)

        self.property_set = property_set
        self.update()

    def update(self) -> None:
        self.setText(0, self.property_set.name)
        self.setText(1, "")


class AttributeTreeItem(QTreeWidgetItem):
    def __init__(self, parent: QTreeWidgetItem | AttributeTreeItem, attribute: classes.Attribute) -> None:
        super(AttributeTreeItem, self).__init__(parent)
        self.attribute = attribute
        if self.attribute.mapping_dict[json_constants.IFC_MAPPING]:
            self.setCheckState(0, Qt.Checked)
        else:
            self.setCheckState(0, Qt.Unchecked)
        self.update()

    def update(self) -> None:
        self.setText(0, self.attribute.name)
        self.setText(1, self.attribute.revit_name)


def item_checked(item: ObjectTreeItem | PsetTreeItem | AttributeTreeItem) -> None:
    check = bool(item.checkState(0))

    linked_data = None
    if isinstance(item, ObjectTreeItem):
        linked_data = item.object

    if isinstance(item, PsetTreeItem):
        linked_data = item.property_set

    if isinstance(item, AttributeTreeItem):
        linked_data = item.attribute

    linked_data.mapping_dict[json_constants.IFC_MAPPING] = check
    linked_data.mapping_dict[value_constants.SHARED_PARAMETERS] = check

    disable = not check
    for index in range(item.childCount()):
        child = item.child(index)
        child.setDisabled(disable)


def pset_double_clicked(item: PsetTreeItem | AttributeTreeItem):
    if not isinstance(item, PsetTreeItem):
        popups.attribute_mapping(item.attribute)
    item.update()
