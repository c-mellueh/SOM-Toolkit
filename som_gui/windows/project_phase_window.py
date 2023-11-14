from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import SOMcreator
from PySide6.QtCore import Qt, QPoint, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont, QAction
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QTreeWidget, QTreeView, QMenu, QAbstractItemView, QInputDialog, \
    QLineEdit
from SOMcreator import classes

from .. import icons
from ..qt_designs import ui_project_phase_window

if TYPE_CHECKING:
    from ..main_window import MainWindow

CLASS_REFERENCE = Qt.ItemDataRole.UserRole + 1
PSET_MODEL = Qt.ItemDataRole.UserRole + 2


def resize_tree_view(tree: QTreeView):
    columns = tree.model().columnCount()
    for index in range(columns):
        tree.resizeColumnToContents(index)


def resize_tree(tree: QTreeView):
    for index in range(tree.model().columnCount()):
        tree.resizeColumnToContents(index)


class ProjectPhaseWindow(QWidget):
    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            self.object_tree.expanded.connect(lambda: resize_tree(self.object_tree))
            self.object_tree.clicked.connect(self.object_selection_changed)
            self.property_set_tree.expanded.connect(lambda: resize_tree_view(self.property_set_tree))
            self.property_set_tree.model().itemChanged.connect(self.property_set_checked)
            self.object_tree.model().itemChanged.connect(self.object_checked)
            self.widget.buttonBox.accepted.connect(self.accepted)
            self.widget.buttonBox.rejected.connect(self.close)
            header = self.widget.object_tree.header()
            header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            header.customContextMenuRequested.connect(self.header_context_menu)
            header.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

        super().__init__()
        self.main_window = main_window
        self.project = self.main_window.project

        self.widget = ui_project_phase_window.Ui_Form()
        self.widget.setupUi(self)

        self.object_tree = self.widget.object_tree
        self.property_set_tree = self.widget.property_set_tree
        self.object_tree.setModel(QStandardItemModel())
        self.property_set_tree.setModel(QStandardItemModel())

        self.setWindowIcon(icons.get_icon())
        self.object_tree.model().setHorizontalHeaderLabels(
            ["Objekt", "Identifier"] + self.project.get_project_phase_list())
        self.main_window.project_phase_window = self

        self.fill_property_set_tree()
        self.fill_object_tree()
        self.widget.label_object.hide()
        self.show()
        connect()

    def header_context_menu(self, pos: QPoint) -> None:
        """creates ContextMenu for renaming, adding and deletion of Project Phases"""
        header = self.widget.object_tree.header()
        column = header.logicalIndexAt(pos)
        object_header_menu = QMenu()
        action_add_project_phase = QAction("Leistungsphase hinzufügen")
        action_rename = QAction("Umbenennen")
        action_remove = QAction("Löschen")

        object_header_menu.addAction(action_add_project_phase)
        object_header_menu.addAction(action_rename)
        object_header_menu.addAction(action_remove)

        action_add_project_phase.triggered.connect(lambda: self.add_header())
        action_rename.triggered.connect(lambda: self.rename_header(column))
        action_remove.triggered.connect(lambda: self.remove_header(column))

        global_pos = self.widget.object_tree.header().mapToGlobal(pos)
        object_header_menu.exec(global_pos)

    def rename_header(self, column: int) -> None:
        """renames Header of ObjectTree and PsetTree -> this leads to the renaming of project phases"""
        if column < 2:
            return
        header = self.object_tree.header()
        old_name = header.model().headerData(column, Qt.Orientation.Horizontal)
        new_name, ok = QInputDialog.getText(self, "Leistungsphase umbenennen", "Neuer Name:", QLineEdit.EchoMode.Normal,
                                            old_name)
        if not ok:
            return
        header.model().setHeaderData(column, Qt.Orientation.Horizontal, new_name)
        self.property_set_tree.model().setHeaderData(column - 1, Qt.Orientation.Horizontal, new_name)

    def remove_header(self, column: int) -> None:
        """removes Header of ObjectTree and PsetTree -> this leads to the deletion of project phases"""

        def iter_tree(model: QStandardItemModel, parent_index: QModelIndex, shift=0):
            for row in range(model.rowCount(parent_index)):
                iter_tree(model, model.index(row, 0, parent_index))
            model.removeColumn(column + shift, parent_index)

        object_model = self.object_tree.model()
        iter_tree(object_model, self.object_tree.rootIndex())
        property_set_model = self.property_set_tree.model()
        iter_tree(property_set_model, self.property_set_tree.rootIndex(), -1)

    def add_header(self, standard_name: str = "Neu") -> None:
        """adds Header of ObjectTree and PsetTree -> this leads to the addition of project phases"""

        def create_check_items(item_count: int):
            cs_items = [QStandardItem() for _ in range(item_count)]
            for item in cs_items:
                item.setCheckState(Qt.CheckState.Checked)
                item.setCheckable(True)
            return cs_items

        def iter_objects(model: QStandardItemModel, parent_item: QStandardItem):
            parent_index = parent_item.index()
            check_items = create_check_items(model.rowCount(parent_index))
            parent_item.appendColumn(check_items)
            for row in range(model.rowCount(parent_index)):
                child_index = model.index(row, 0, parent_index)
                iter_objects(model, model.itemFromIndex(child_index))

        def loop_name(new_name):
            if new_name in existing_names:
                if new_name == standard_name:
                    return loop_name(f"{new_name}_1")
                index = int(new_name[-1])
                return loop_name(f"{new_name[:-1]}{index + 1}")
            return new_name

        object_model = self.object_tree.model()
        header_count = object_model.columnCount() - 2
        existing_names = [object_model.headerData(2 + column, Qt.Orientation.Horizontal) for column in
                          range(header_count)]
        project_phase_name = loop_name(standard_name)
        iter_objects(object_model, object_model.invisibleRootItem())
        object_model.setHeaderData(object_model.columnCount() - 1, Qt.Orientation.Horizontal, project_phase_name)

        property_set_model = self.property_set_tree.model()
        iter_objects(property_set_model, property_set_model.invisibleRootItem())
        property_set_model.setHeaderData(property_set_model.columnCount() - 1, Qt.Orientation.Horizontal,
                                         project_phase_name)

    def property_set_checked(self, item: QStandardItem):
        """gets called when a property-set checkbox is checked -> disables attribute checkboxes in existing project phase"""
        pset_index = item.index().siblingAtColumn(0)
        self.handle_attribute_states(pset_index)

    def create_state_list(self, model: QStandardItemModel, focus_index: QModelIndex, start=2) -> list[bool]:
        """creates a list for all project_phases that describes if the subobjects will be enabled or not"""
        c_list = list()
        for c in range(start, model.columnCount()):
            sibling_index = focus_index.siblingAtColumn(c)
            check_state = sibling_index.data(Qt.ItemDataRole.CheckStateRole)
            children_enabled = True if check_state in (2, Qt.CheckState.Checked) else False
            if model.itemFromIndex(sibling_index) is None:
                continue
            children_enabled = False if not model.itemFromIndex(sibling_index).isEnabled() else children_enabled
            c_list.append(children_enabled)
        return c_list

    def object_checked(self, obj_item: QStandardItem):
        """gets callend if the data of an objectItem is changed (usually if the item is checked or unchecked)"""

        def iter_tree(parent_index: QModelIndex):
            state_list = self.create_state_list(self.object_tree.model(), parent_index)
            for row in range(model.rowCount(parent_index)):
                for column, state in enumerate(state_list, 2):
                    child_index = model.index(row, column, index)
                    item = model.itemFromIndex(child_index)
                    if item is None:  # while creating new project_phases this is necessary
                        continue
                    item.setEnabled(state)
                new_focus_index = model.index(row, 0, parent_index)
                iter_tree(new_focus_index)

        model: QStandardItemModel = self.object_tree.model()
        index = model.indexFromItem(obj_item)
        index = model.sibling(index.row(), 0, index)
        iter_tree(index)



    def fill_object_tree(self) -> None:
        """Adds all objects to objectTree"""

        def iter_tree(object_list, parent_item: QStandardItem):
            for obj in object_list:
                item_list = list()
                new_item = QStandardItem(obj.name)
                new_item.setData(obj, CLASS_REFERENCE)
                item_list.append(new_item)
                item_list.append(QStandardItem(obj.ident_value))

                for project_phase in project.get_project_phase_list():
                    phase_item = QStandardItem()
                    phase_item.setCheckable(True)
                    cs = Qt.CheckState.Checked if obj.get_project_phase_state(
                        project_phase) else Qt.CheckState.Unchecked
                    phase_item.setCheckState(cs)
                    item_list.append(phase_item)
                parent_item.appendRow(item_list)
                iter_tree(obj.children, new_item)

        project: classes.Project = self.main_window.project
        tree = self.widget.object_tree
        objects = list(project.get_all_objects())
        root_objects = [obj for obj in sorted(objects) if obj.parent is None]
        model: QStandardItemModel = tree.model()
        iter_tree(root_objects, model.invisibleRootItem())
        resize_tree(tree)

    def fill_property_set_tree(self):
        """adds all propertySetObjects to PropertySetTree and Hides them.
        When an object is clicked only the relating PropertySets will be shown"""

        def format_pset_item(item):
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            item.setEditable(False)

        def handle_phases(item: QStandardItem):
            item_list = [item]
            item_class = item.data(CLASS_REFERENCE)
            for phase in project_phases:
                phase_item = QStandardItem()
                phase_item.setCheckable(True)
                cs = Qt.CheckState.Checked if item_class.get_project_phase_state(phase) else Qt.CheckState.Unchecked
                phase_item.setCheckState(cs)
                item_list.append(phase_item)
            return item_list

        model = self.property_set_tree.model()

        project_phases = self.project.get_project_phase_list()

        model.setHorizontalHeaderLabels(["PropertySet, Attribut"] + project_phases)

        for obj in self.main_window.project.get_all_objects():
            obj: classes.Object
            pset: classes.PropertySet
            for pset in obj.get_all_property_sets():
                pset_item = QStandardItem(pset.name)
                format_pset_item(pset_item)
                pset_item.setData(pset, CLASS_REFERENCE)
                items = handle_phases(pset_item)
                model.appendRow(items)
                for attribute in pset.get_all_attributes():
                    attribute_item = QStandardItem(attribute.name)
                    attribute_item.setData(attribute, CLASS_REFERENCE)
                    items = handle_phases(attribute_item)
                    pset_item.appendRow(items)
                self.property_set_tree.setRowHidden(pset_item.row(), model.invisibleRootItem().index(), True)

    def object_selection_changed(self):
        """gets called when an objectItem is clicked"""
        object_indexes = self.widget.object_tree.selectedIndexes()
        if not object_indexes:
            return
        index: QModelIndex = object_indexes[0]
        obj = index.data(CLASS_REFERENCE)
        self.show_property_sets(index)
        self.widget.label_object.show()
        self.widget.label_object.setText(f"{obj.name} ({obj.ident_value})")

    def handle_attribute_states(self, property_set_index: QModelIndex):
        """checks for state of propertySetItem and disables attributes as needed"""
        model = property_set_index.model()
        attribute_states = self.create_state_list(model, property_set_index, start=1)
        for attribute_row in range(model.rowCount(property_set_index)):
            for col, state in enumerate(attribute_states, start=1):
                model.itemFromIndex(model.index(attribute_row, col, property_set_index)).setEnabled(state)

    def show_property_sets(self, object_index: QStandardItem):
        """shows propertySetItems which match the selected object"""
        def handle_enable_status(property_set_indexes: list[QModelIndex]):
            for pset_index in property_set_indexes:
                for col, state in enumerate(state_list, start=1):
                    model.itemFromIndex(pset_index.sibling(pset_index.row(), col)).setEnabled(
                        state)  # set Checkmark enabled
                self.handle_attribute_states(pset_index)

        selected_object = object_index.data(CLASS_REFERENCE)
        state_list = self.create_state_list(self.object_tree.model(), object_index, 2)
        tree = self.property_set_tree
        model: QStandardItemModel = tree.model()
        shown_property_sets = list()

        for row in range(model.rowCount()):
            index = model.index(row, 0)
            pset: classes.PropertySet = index.data(CLASS_REFERENCE)
            if pset.object == selected_object:
                shown_property_sets.append(index)
                tree.setRowHidden(row, tree.rootIndex(), False)
            else:
                tree.setRowHidden(row, tree.rootIndex(), True)
        handle_enable_status(shown_property_sets)
        resize_tree_view(tree)
        tree.expandAll()

    def accepted(self):
        # TODO
        for item, project_phase_dict in self.data_model.items():
            for project_phase_name, value in project_phase_dict.items():
                if item.get_project_phase_state(project_phase_name) != value:
                    logging.info(f"{item}: Projektphase {project_phase_name} geändert")
                    item.set_project_phase(project_phase_name, value)
        self.hide()
        self.main_window.reload()
