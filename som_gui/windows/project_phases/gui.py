from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPoint, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont, QAction
from PySide6.QtWidgets import QWidget, QMenu, QAbstractItemView, QInputDialog, QLineEdit
from SOMcreator import classes

from som_gui import icons
from som_gui.qt_designs import ui_project_phase_window
from . import object_tree
from .object_tree import CLASS_REFERENCE, OBJECT_TITLES, PSET_TITLES

if TYPE_CHECKING:
    from som_gui.main_window import MainWindow


def create_state_list(model: QStandardItemModel, focus_index: QModelIndex, start: int) -> list[bool]:
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


def handle_attribute_states(property_set_index: QModelIndex):
    """checks for state of propertySetItem and disables attributes as needed"""
    model = property_set_index.model()
    attribute_states = create_state_list(model, property_set_index, start=len(PSET_TITLES))
    for attribute_row in range(model.rowCount(property_set_index)):
        for col, state in enumerate(attribute_states, start=len(PSET_TITLES)):
            model.itemFromIndex(model.index(attribute_row, col, property_set_index)).setEnabled(state)


def property_set_checked(item: QStandardItem):
    """gets called when a property-set checkbox is checked ->
    disables attribute checkboxes in existing project phase"""
    pset_index = item.index().siblingAtColumn(0)
    handle_attribute_states(pset_index)


class ProjectPhaseWindow(QWidget):
    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            self.object_tree.expanded.connect(lambda: object_tree.resize_tree(self.object_tree))
            self.object_tree.clicked.connect(self.object_selection_changed)
            self.property_set_tree.expanded.connect(lambda: object_tree.resize_tree_view(self.property_set_tree))
            self.property_set_tree.model().itemChanged.connect(property_set_checked)
            self.object_tree.model().itemChanged.connect(self.object_checked)
            self.widget.buttonBox.accepted.connect(self.accepted)
            self.widget.buttonBox.rejected.connect(self.close)
            header = self.widget.object_tree.header()
            header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            header.customContextMenuRequested.connect(self.header_context_menu)
            #header.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

        super().__init__()
        self.main_window = main_window
        self.project = self.main_window.project

        self.widget = ui_project_phase_window.Ui_Form()
        self.widget.setupUi(self)

        self.object_tree = self.widget.object_tree
        self.object_tree.title_count = len(OBJECT_TITLES)
        self.property_set_tree = self.widget.property_set_tree
        self.property_set_tree.title_count = len(PSET_TITLES)
        self.object_tree.setModel(QStandardItemModel())
        self.property_set_tree.setModel(QStandardItemModel())

        self.setWindowIcon(icons.get_icon())
        self.object_tree.model().setHorizontalHeaderLabels(
            OBJECT_TITLES + self.project.get_project_phase_list())
        self.main_window.project_phase_window = self
        self.project_phase_dict = {name: index + self.object_tree.title_count for index, name in
                                   enumerate(self.project.get_project_phase_list())}

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
        if column < self.object_tree.title_count:
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
        s = self.object_tree.title_count - self.property_set_tree.title_count
        iter_tree(property_set_model, self.property_set_tree.rootIndex(), -s)
        for project_phase, index in self.project_phase_dict.items():
            if index is None:
                continue
            if index < column:
                continue
            elif index == column:
                self.project_phase_dict[project_phase] = None
            else:
                self.project_phase_dict[project_phase] = index - 1

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
        header_count = object_model.columnCount() - self.object_tree.title_count
        existing_names = [object_model.headerData(self.object_tree.title_count + column, Qt.Orientation.Horizontal) for
                          column in
                          range(header_count)]
        project_phase_name = loop_name(standard_name)
        iter_objects(object_model, object_model.invisibleRootItem())
        object_model.setHeaderData(object_model.columnCount() - 1, Qt.Orientation.Horizontal, project_phase_name)

        property_set_model = self.property_set_tree.model()
        iter_objects(property_set_model, property_set_model.invisibleRootItem())
        property_set_model.setHeaderData(property_set_model.columnCount() - 1, Qt.Orientation.Horizontal,
                                         project_phase_name)

    def object_checked(self, obj_item: QStandardItem):
        """gets callend if the data of an objectItem is changed (usually if the item is checked or unchecked)"""

        def iter_tree(parent_index: QModelIndex):
            state_list = create_state_list(self.object_tree.model(), parent_index, self.object_tree.title_count)
            for row in range(model.rowCount(parent_index)):
                for column, state in enumerate(state_list, self.object_tree.title_count):
                    child_index = model.index(row, column, parent_index)
                    item = model.itemFromIndex(child_index)
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
                self.object_checked(new_item)

        project: classes.Project = self.main_window.project
        tree = self.widget.object_tree
        objects = list(project.get_all_objects())
        root_objects = [obj for obj in sorted(objects) if obj.parent is None]
        model: QStandardItemModel = tree.model()
        iter_tree(root_objects, model.invisibleRootItem())
        object_tree.resize_tree(tree)

    def fill_property_set_tree(self):
        """adds all propertySetObjects to PropertySetTree and Hides them.
        When an objects is clicked only the relating PropertySets will be shown"""

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

        model.setHorizontalHeaderLabels(PSET_TITLES + project_phases)

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
        self.object_index_clicked(index)

    def object_index_clicked(self, object_index: QStandardItem):
        """shows propertySetItems which match the selected objects"""

        def handle_enable_status(property_set_indexes: list[QModelIndex]):
            for pset_index in property_set_indexes:
                for col, state in enumerate(state_list, start=self.property_set_tree.title_count):
                    model.itemFromIndex(pset_index.sibling(pset_index.row(), col)).setEnabled(
                        state)  # set Checkmark enabled
                handle_attribute_states(pset_index)

        selected_object = object_index.data(CLASS_REFERENCE)
        self.widget.label_object.show()
        self.widget.label_object.setText(f"{selected_object.name} ({selected_object.ident_value})")

        state_list = create_state_list(self.object_tree.model(), object_index, self.object_tree.title_count)
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
        object_tree.resize_tree_view(tree)
        tree.expandAll()

    def get_project_phase_titles(self) -> list[str]:
        object_model = self.object_tree.model()
        titles = [object_model.headerData(c, Qt.Orientation.Horizontal) for c in range(object_model.columnCount())]
        return titles[len(OBJECT_TITLES):]

    def accepted(self):
        def iter_tree(model: QStandardItemModel, parent_index: QModelIndex, header_titles):
            for row in range(model.rowCount(parent_index)):
                index = model.index(row, 0, parent_index)
                class_item: classes.Object | classes.PropertySet | classes.Attribute = index.data(CLASS_REFERENCE)
                for column in range(len(header_titles), model.columnCount()):
                    check_state = index.sibling(index.row(), column).data(Qt.ItemDataRole.CheckStateRole)
                    check_bool = True if check_state in (2, Qt.CheckState.Checked) else False
                    project_phase_name = model.headerData(column, Qt.Orientation.Horizontal)
                    class_item.set_project_phase(project_phase_name, check_bool)
                iter_tree(model, index, header_titles)

        def handle_project_phases():
            # Handle deletion,creation and renaming of project_phases
            for project_phase_name, index in self.project_phase_dict.items():
                if index is None:
                    self.project.remove_project_phase(project_phase_name)
                    continue
                new_name = self.object_tree.model().headerData(index, Qt.Orientation.Horizontal)
                if new_name != project_phase_name:
                    self.project.rename_project_phase(project_phase_name, new_name)

            new_project_phase_names = set(self.get_project_phase_titles())
            existing_project_phase_names = set(self.project.get_project_phase_list())
            for new_project_phase in new_project_phase_names - existing_project_phase_names:
                self.project.add_project_phase(new_project_phase)

        handle_project_phases()
        object_model = self.object_tree.model()
        root_index = self.object_tree.rootIndex()
        iter_tree(object_model, root_index, OBJECT_TITLES)

        pset_model = self.property_set_tree.model()
        root_index = self.property_set_tree.rootIndex()
        iter_tree(pset_model, root_index, PSET_TITLES)
        self.close()
        self.main_window.reload()
