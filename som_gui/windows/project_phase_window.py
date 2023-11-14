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


class PropertySetModel(QStandardItemModel):
    def __init__(self, project: SOMcreator.Project):
        super(PropertySetModel, self).__init__()
        self.project = project

    def clear(self) -> None:
        super(PropertySetModel, self).clear()
        texte = list(self.project.get_project_phase_list())
        self.setHorizontalHeaderLabels(["PropertySet, Attribut"] + texte)


class CheckBoxItem(QStandardItem):
    def __init__(self, is_checked: bool, is_enabled: bool):
        super(CheckBoxItem, self).__init__()
        check_state = Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked
        self.setCheckState(check_state)
        self.setCheckable(True)
        self.setEnabled(is_enabled)


class AttributeItem(QStandardItem):
    def __init__(self, attribute: classes.Attribute):
        super(AttributeItem, self).__init__()
        self.attribute = attribute
        self.setText(attribute.name)
        self.setEditable(False)


def checkstate_to_bool(check_state: Qt.CheckState) -> bool:
    return True if check_state == Qt.CheckState.Checked else False


class ProjectPhaseWindow(QWidget):
    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            self.object_tree.expanded.connect(lambda: resize_tree(self.object_tree))
            self.object_tree.clicked.connect(self.object_selection_changed)
            self.property_set_tree.expanded.connect(lambda: resize_tree_view(self.property_set_tree))
            self.property_set_tree.model().itemChanged.connect(self.property_set_checked)
            self.object_tree.model().itemChanged.connect(self.modify_data_model)
            self.widget.buttonBox.accepted.connect(self.accepted)
            self.widget.buttonBox.rejected.connect(self.close)

        super().__init__()
        self.project = main_window.project
        self.widget = ui_project_phase_window.Ui_Form()
        self.widget.setupUi(self)
        self.object_tree = self.widget.object_tree
        self.property_set_tree = self.widget.property_set_tree

        self.widget.object_tree.setModel(QStandardItemModel())

        self.tree_model = PropertySetModel(main_window.project)
        self.widget.property_set_tree.setModel(self.tree_model)
        self.setWindowIcon(icons.get_icon())
        self.main_window = main_window
        connect()
        self.data_model: dict[classes.Object | classes.PropertySet | classes.Attribute, dict[str, bool]] = dict()
        self.set_object_tree_header()
        header = self.widget.object_tree.header()
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.header_context_menu)
        header.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

    def header_context_menu(self, pos: QPoint):
        header = self.widget.object_tree.header()
        column = header.logicalIndexAt(pos)
        header_item = self.widget.object_tree.headerItem()
        phase_name = header_item.text(column)

        object_header_menu = QMenu()
        action_add_project_phase = QAction("Leistungsphase hinzufügen")
        action_rename = QAction("Umbenennen")
        action_remove = QAction("Löschen")

        object_header_menu.addAction(action_add_project_phase)
        object_header_menu.addAction(action_rename)
        object_header_menu.addAction(action_remove)

        action_add_project_phase.triggered.connect(lambda: self.add_header())
        action_rename.triggered.connect(lambda: self.rename_header(column))
        action_remove.triggered.connect(lambda: self.remove_header(phase_name))

        global_pos = self.widget.object_tree.header().mapToGlobal(pos)
        object_header_menu.exec(global_pos)

    def rename_header(self, column: int) -> None:
        if column < 2:
            return
        header_item = self.widget.object_tree.headerItem()
        old_name = header_item.text(column)
        new_name, ok = QInputDialog.getText(self, "Leistungsphase umbenennen", "Neuer Name:", QLineEdit.EchoMode.Normal,
                                            old_name)
        if not ok:
            return
        header_item.setText(column, new_name)
        self.main_window.project.rename_project_phase(old_name, new_name)
        for entity, project_phase_dict in self.data_model.items():
            value = project_phase_dict[old_name]
            project_phase_dict[new_name] = value
            project_phase_dict.pop(old_name)
        self.tree_model.clear()

    def remove_header(self, phase_name: str) -> None:
        self.main_window.project.remove_project_phase(phase_name)
        self.set_object_tree_header()
        self.fill_object_tree()
        for entity, project_phase_dict in self.data_model.items():
            project_phase_dict.pop(phase_name)
        self.tree_model.clear()

    def add_header(self, standard_name: str = "Neu") -> None:
        def loop_name(new_name):
            if new_name in self._project_phases:
                if new_name == standard_name:
                    return loop_name(f"{new_name}_1")
                index = int(new_name[-1])
                return loop_name(f"{new_name[:-1]}{index + 1}")
            return new_name

        project_phase_name = loop_name(standard_name)
        self.main_window.project.add_project_phase(project_phase_name)
        self.set_object_tree_header()
        # self.fill_object_tree()
        for entity, project_phase_dict in self.data_model.items():
            project_phase_dict[project_phase_name] = True
        self.tree_model.clear()

    @property
    def _project_phases(self) -> list[str]:
        return self.main_window.project.get_project_phase_list()

    def set_object_tree_header(self):
        model: QStandardItemModel = self.object_tree.model()
        model.setHorizontalHeaderLabels(["Objekt", "Identifier"] + self.project.get_project_phase_list())

    def property_set_checked(self, item:QStandardItem):
        pset_index = item.index().siblingAtColumn(0)
        self.handle_attribute_states(pset_index)


    def create_state_list(self, model, focus_index: QModelIndex, start=2):
        c_list = list()
        for c in range(start, start + len(self._project_phases)):
            sibling_index = focus_index.siblingAtColumn(c)
            check_state = sibling_index.data(Qt.ItemDataRole.CheckStateRole)
            children_enabled = True if check_state in (2, Qt.CheckState.Checked) else False
            children_enabled = False if not model.itemFromIndex(sibling_index).isEnabled() else children_enabled
            c_list.append(children_enabled)
        return c_list

    def modify_data_model(self, obj_item: QStandardItem):
        def iter_tree(parent_index: QModelIndex):
            state_list = self.create_state_list(self.object_tree.model(), parent_index)
            for row in range(model.rowCount(parent_index)):
                for column, state in enumerate(state_list, 2):
                    child_index = model.index(row, column, index)
                    item = model.itemFromIndex(child_index)
                    if item is None:
                        continue
                    item.setEnabled(state)
                new_focus_index = model.index(row, 0, parent_index)
                iter_tree(new_focus_index)

        model: QStandardItemModel = self.object_tree.model()
        index = model.indexFromItem(obj_item)
        index = model.sibling(index.row(), 0, index)
        iter_tree(index)
        # self.fill_property_set_tree(index)

    def show(self) -> None:
        self.clear_tree(self.object_tree)
        self.clear_tree(self.property_set_tree)
        self.set_object_tree_header()
        self.fill_pset_model()
        self.fill_object_tree()

        self.widget.label_object.hide()
        super(ProjectPhaseWindow, self).show()

    def accepted(self):
        #TODO
        for item, project_phase_dict in self.data_model.items():
            for project_phase_name, value in project_phase_dict.items():
                if item.get_project_phase_state(project_phase_name) != value:
                    logging.info(f"{item}: Projektphase {project_phase_name} geändert")
                    item.set_project_phase(project_phase_name, value)
        self.hide()
        self.main_window.reload()

    def resize_to_content(self) -> None:
        """resizes Tree to content so it allways looks fresh and tidy"""
        resize_tree(self.widget.object_tree)
        resize_tree_view(self.widget.property_set_tree)

    def clear_tree(self, tree: QTreeView):
        for row in reversed(range(tree.model().rowCount())):
            self.object_tree.model().removeRow(row)

    def fill_object_tree(self) -> None:
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
        self.clear_tree(tree)
        objects = list(project.get_all_objects())
        root_objects = [obj for obj in sorted(objects) if obj.parent is None]
        model: QStandardItemModel = tree.model()
        self.set_object_tree_header()

        iter_tree(root_objects, model.invisibleRootItem())
        resize_tree(tree)

    def fill_pset_model(self):
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
        object_indexes = self.widget.object_tree.selectedIndexes()
        if not object_indexes:
            return
        index: QModelIndex = object_indexes[0]
        obj = index.data(CLASS_REFERENCE)
        self.fill_property_set_tree(index)
        self.widget.label_object.show()
        self.widget.label_object.setText(f"{obj.name} ({obj.ident_value})")

    def handle_attribute_states(self, property_set_index: QModelIndex):
        model = property_set_index.model()
        attribute_states = self.create_state_list(model, property_set_index, start=1)
        for attribute_row in range(model.rowCount(property_set_index)):
            for col, state in enumerate(attribute_states, start=1):
                model.itemFromIndex(model.index(attribute_row, col, property_set_index)).setEnabled(state)

    def fill_property_set_tree(self, object_index: QStandardItem):
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

        # for property_set in selected_object.get_all_property_sets():
        #     pset_item = QStandardItem(property_set.name)
        #     pset_item.setData(property_set, CLASS_REFERENCE)
        #     # format_pset_item(pset_item)
        #     pset_row = [pset_item]
        #     for index, project_phase_name in enumerate(self._project_phases):
        #         pset_is_enabled = self.data_model[selected_object][project_phase_name]
        #         pset_is_checked = self.data_model[property_set][project_phase_name]
        #         pset_row.append(CheckBoxItem(pset_is_checked, pset_is_enabled))
        #     root.appendRow(pset_row)
        #     for attribute in property_set.get_all_attributes():
        #         attribute_row = [AttributeItem(attribute)]
        #         for index, project_phase_name in enumerate(self._project_phases):
        #             pset_is_enabled = self.data_model[selected_object][project_phase_name]
        #             attribute_is_enabled = self.data_model[property_set][project_phase_name]
        #             attribute_is_checked = self.data_model[attribute][project_phase_name]
        #             attribute_row.append(
        #                 CheckBoxItem(attribute_is_checked, all((attribute_is_enabled, pset_is_enabled))))
        #         pset_item.appendRow(attribute_row)

        resize_tree_view(tree)
        tree.expandAll()
