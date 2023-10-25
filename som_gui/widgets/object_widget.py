from __future__ import annotations

import copy as cp
import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QShortcut, QKeySequence, QDropEvent
from PySide6.QtWidgets import QMenu, QTreeWidget, QAbstractItemView, QTreeWidgetItem, QDialog, QLineEdit, QCompleter
from SOMcreator import classes, value_constants
from SOMcreator.Template import IFC_4_1

from ..icons import get_icon
from ..qt_designs import ui_mainwindow, ui_object_info_widget
from ..widgets import property_widget
from ..windows import popups

if TYPE_CHECKING:
    from ..main_window import MainWindow

CHECK_POS = 3


class CustomTree(QTreeWidget):
    def __init__(self, layout) -> None:
        if layout is not None:
            super(CustomTree, self).__init__(layout)
        else:
            super(CustomTree, self).__init__()

    def dropEvent(self, event: QDropEvent) -> None:
        selected_items = self.selectedItems()
        droped_on_item = self.itemFromIndex(self.indexAt(event.pos()))
        if self.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:
            super(CustomTree, self).dropEvent(event)
            parent: classes.Object = droped_on_item.object

        else:
            super(CustomTree, self).dropEvent(event)
            parent: classes.Object = droped_on_item.object.parent

        for el in selected_items:
            obj: classes.Object = el.object
            if parent is not None:
                obj.parent = parent
            else:
                obj.parent = None

    def object_dict(self) -> dict[classes.Object, CustomObjectTreeItem]:
        obj_dict = dict()

        def add_to_dict(item: CustomObjectTreeItem):
            obj_dict[item.object] = item
            for k in range(item.childCount()):
                add_to_dict(item.child(k))

        for i in range(self.topLevelItemCount()):
            add_to_dict(self.topLevelItem(i))
        return obj_dict


class CustomObjectTreeItem(QTreeWidgetItem):
    def __init__(self, obj: classes.Object) -> None:
        super(CustomObjectTreeItem, self).__init__()
        self._object = obj
        self.refresh()

    def addChild(self, child: CustomObjectTreeItem) -> None:
        super(CustomObjectTreeItem, self).addChild(child)
        if child.object not in self.object.children:
            self.object.add_child(child.object)

    @property
    def object(self) -> classes.Object:
        return self._object

    def refresh(self) -> None:
        """
        set Values
        index 0: name
        index 1: ident_value
        index 2: abbreviation
        index 3: optional
        """

        values = [self.object.name, self.object.ident_value, self.object.abbreviation]

        for index, value in enumerate(values):
            self.setText(index, value)

        if self.object.optional:

            self.setCheckState(CHECK_POS, Qt.CheckState.Checked)
        else:
            self.setCheckState(CHECK_POS, Qt.CheckState.Unchecked)

    def update(self) -> None:
        logging.debug(f"Item toggled if item is not Toggled contact me")
        check_state = self.checkState(CHECK_POS)

        if check_state == Qt.CheckState.Checked:
            check_bool = True
        elif check_state == Qt.CheckState.Unchecked:
            check_bool = False
        elif check_state == Qt.CheckState.PartiallyChecked:
            logging.error("Partially Checking not Allowed")
            check_bool = True
        else:
            check_bool = True
        self.object.optional = check_bool

    def expand_to_me(self) -> None:
        self.setExpanded(True)
        if self.parent() is not None:
            self.parent().expand_to_me()


class ObjectInfoWidget(QDialog):
    def __init__(self, main_window: MainWindow, obj: classes.Object):
        super(ObjectInfoWidget, self).__init__()

        def connect():
            self.widget.line_edit_attribute_value.textChanged.connect(self.ident_edited)
            self.widget.line_edit_abbreviation.textChanged.connect(self.abbrev_edited)
            self.widget.combo_box_pset.currentIndexChanged.connect(self.pset_combobox_change)

        self.object = obj
        self.main_window = main_window
        self.main_window.object_info_widget = self

        self.widget = ui_object_info_widget.Ui_ObjectInfo()
        self.widget.setupUi(self)
        connect()

        self.setWindowTitle(f"bearbeite Objektvorgabe '{self.object.name}'")
        self.setWindowIcon(get_icon())

        self.widget.button_add_ifc.clicked.connect(self.add_line)

        self.ifc_lines: list[QLineEdit] = [self.widget.line_edit_ifc]
        self.completer = QCompleter(IFC_4_1)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.widget.line_edit_ifc.setCompleter(self.completer)
        self.fill_with_values()

    def ident_edited(self, val):
        if val in [o.ident_value for o in self.main_window.project.get_all_objects() if o != self.object]:
            style = "color:red"
        else:
            style = "color:black"
        self.widget.line_edit_attribute_value.setStyleSheet(style)

    def abbrev_edited(self, val):
        if val in [o.abbreviation for o in self.main_window.project.get_all_objects() if o != self.object]:
            style = "color:red"
        else:
            style = "color:black"
        self.widget.line_edit_abbreviation.setStyleSheet(style)

    def pset_combobox_change(self, item_index):
        self.widget.combo_box_attribute.clear()
        text = self.widget.combo_box_pset.itemText(item_index)
        pset = self.object.get_property_set_by_name(text)
        attribute_list = [attribute.name for attribute in pset.attributes if
                          attribute.data_type == value_constants.XS_STRING]
        self.widget.combo_box_attribute.addItems(attribute_list)

    def fill_with_values(self):
        self.widget.line_edit_abbreviation.setText(self.object.abbreviation)
        self.widget.line_edit_name.setText(self.object.name)
        ifc_mappings = len(self.object.ifc_mapping)

        for _ in range(ifc_mappings - 1):
            self.add_line()

        for index, ifc_mapping in enumerate(self.object.ifc_mapping):
            self.ifc_lines[index].setText(ifc_mapping)

        if self.object.is_concept:
            self.widget.layout_ident_attribute.hide()
            return

        self.widget.combo_box_pset.addItems(sorted([pset.name for pset in self.object.property_sets]))
        self.widget.combo_box_pset.setCurrentText(self.object.ident_attrib.property_set.name)
        self.widget.combo_box_attribute.setCurrentText(self.object.ident_attrib.name)
        self.widget.line_edit_attribute_value.setText(self.object.ident_value)

    @property
    def ifc_values(self) -> set[str]:
        return {line.text() for line in self.ifc_lines if line and line is not None}

    def add_line(self):
        line_edit = QLineEdit()
        line_edit.setCompleter(self.completer)
        self.ifc_lines.append(line_edit)
        self.widget.vertical_layout_ifc.addWidget(line_edit)
        line_edit.show()


def object_double_clicked(main_window: MainWindow, obj: classes.Object):
    object_widget = ObjectInfoWidget(main_window, obj)
    is_ok = object_widget.exec()
    old_ident_attribute = obj.ident_attrib
    if not is_ok:
        return

    abbreviation = object_widget.widget.line_edit_abbreviation.text()
    ident_value = object_widget.widget.line_edit_attribute_value.text()

    abbreviations = [o.abbreviation for o in main_window.project.get_all_objects() if o != obj]
    ident_values = [o.ident_value for o in main_window.project.get_all_objects() if o != obj]
    print(abbreviations)
    print(ident_values)

    if abbreviation in abbreviations:
        popups.msg_abbrev_already_exists()
        return

    if ident_value in ident_values:
        popups.msg_ident_already_exists()
        return

    obj.ifc_mapping = object_widget.ifc_values
    obj.name = object_widget.widget.line_edit_name.text()
    obj.abbreviation = abbreviation

    ident_pset_name = object_widget.widget.combo_box_pset.currentText()
    ident_attribute_name = object_widget.widget.combo_box_attribute.currentText()

    ident_attribute = obj.get_property_set_by_name(ident_pset_name).get_attribute_by_name(ident_attribute_name)
    obj.ident_attrib = ident_attribute
    obj.ident_attrib.value = [ident_value]
    main_window.reload()


def init(main_window: MainWindow):
    def init_tree(tree: CustomTree):
        # Design Tree
        tree.setObjectName(u"treeWidget_objects")
        tree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        tree.setDefaultDropAction(Qt.MoveAction)
        tree.setAlternatingRowColors(False)
        tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        tree.setSortingEnabled(True)
        tree.setExpandsOnDoubleClick(False)
        tree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        tree.setContextMenuPolicy(Qt.CustomContextMenu)
        tree.viewport().setAcceptDrops(True)

        ___qtreewidgetitem = tree.headerItem()
        ___qtreewidgetitem.setText(0, "Objektvorgaben")
        ___qtreewidgetitem.setText(1, "Identifier")
        ___qtreewidgetitem.setText(2, "Abkürzung")
        ___qtreewidgetitem.setText(3, "Optional")

    def connect_items():
        ui: ui_mainwindow.Ui_MainWindow = main_window.ui
        ui.tree_object.itemClicked.connect(lambda item: single_click(main_window, item))
        ui.tree_object.itemChanged.connect(lambda item: item.update())
        ui.tree_object.itemExpanded.connect(lambda: resize_tree(main_window))
        ui.tree_object.customContextMenuRequested.connect(lambda pos: right_click(main_window, pos))
        ui.tree_object.itemDoubleClicked.connect(lambda item: object_double_clicked(main_window, item.object))
        ui.button_search.clicked.connect(lambda: search_object(main_window))
        ui.button_objects_add.clicked.connect(lambda: add_object(main_window))
        main_window.group_shortcut.activated.connect(lambda: rc_group_items(main_window))
        main_window.delete_shortcut.activated.connect(lambda: rc_delete(main_window))
        main_window.search_shortcut.activated.connect(lambda: search_object(main_window))

    main_window.ui.verticalLayout_objects.removeWidget(main_window.ui.tree_object)
    main_window.ui.tree_object.close()
    main_window.ui.tree_object = CustomTree(main_window.ui.verticalLayout_main)
    main_window.ui.verticalLayout_objects.addWidget(main_window.ui.tree_object)
    init_tree(main_window.ui.tree_object)

    main_window.ui.verticalLayout_objects.addWidget(main_window.ui.tree_object)

    main_window.delete_shortcut = QShortcut(QKeySequence('Ctrl+X'), main_window)
    main_window.group_shortcut = QShortcut(QKeySequence('Ctrl+G'), main_window)
    main_window.search_shortcut = QShortcut(QKeySequence('Ctrl+F'), main_window)
    connect_items()


def update_completer(main_window: MainWindow):
    completer = QCompleter(property_widget.predefined_pset_list(main_window), main_window)
    main_window.ui.lineEdit_ident_pSet.setCompleter(completer)
    main_window.ui.lineEdit_pSet_name.setCompleter(completer)


def fill_tree(object_list: list[classes.Object], tree: QTreeWidget, tree_object_class) -> None:
    object_list = list(object_list)
    root_item = tree.invisibleRootItem()
    item_dict: dict[classes.Object, tree_object_class] = \
        {obj: add_object_to_tree(tree, obj, root_item, tree_object_class) for obj in
         object_list}  # add all Objects to Tree without Order

    for obj in object_list:
        tree_item = item_dict[obj]
        parent_is_none = obj.parent is None
        parent_in_dict = obj.parent in item_dict
        if not parent_is_none and parent_in_dict:
            parent_item = item_dict[obj.parent]
            root = tree_item.treeWidget().invisibleRootItem()
            item = root.takeChild(root.indexOfChild(tree_item))
            parent_item.addChild(item)


def resize_tree(main_window: MainWindow):
    for column in range(main_window.object_tree.columnCount()):
        main_window.object_tree.resizeColumnToContents(column)


def selected_object(main_window: MainWindow) -> CustomObjectTreeItem | None:
    tree: CustomTree = main_window.ui.tree_object
    sel_items = tree.selectedItems()
    if len(sel_items) == 1:
        return sel_items[0]
    else:
        return None


def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)


def clear_object_input(main_window: MainWindow):
    obj_line_edit_list = [main_window.ui.line_edit_object_name,
                          main_window.ui.lineEdit_ident_value,
                          main_window.ui.lineEdit_ident_attribute,
                          main_window.ui.lineEdit_ident_pSet,
                          main_window.ui.line_edit_abbreviation]
    for el in obj_line_edit_list:
        el.clear()


def clear_all(main_window: MainWindow):
    # Clean Widget
    clear_object_input(main_window)
    main_window.ui.tree_object.clear()

    # Delete Attributes & Objects
    for obj in classes.Object:
        obj.delete(False)


def search_object(main_window: MainWindow):
    sw = popups.ObjectSearchWindow(main_window)
    if not sw.exec():
        return
    obj = sw.selected_object
    tree: CustomTree = main_window.object_tree

    for selected_item in tree.selectedItems():
        selected_item.setSelected(False)

    tree_item = tree.object_dict()[obj]
    tree_item.setSelected(True)
    tree_item.expand_to_me()

    single_click(main_window, tree_item)
    tree.scrollToItem(tree_item)


def right_click(main_window: MainWindow, position: QPoint):
    menu = QMenu()

    selected_items = main_window.ui.tree_object.selectedItems()
    if len(selected_items) == 1:
        main_window.action_copy = menu.addAction("Copy")
        main_window.action_copy.triggered.connect(lambda: copy(main_window))

    if len(selected_items) != 0:
        main_window.action_delete_attribute = menu.addAction("Delete")
        main_window.action_expand_selection = menu.addAction("Expand")
        main_window.action_collapse_selection = menu.addAction("Collapse")
        main_window.action_delete_attribute.triggered.connect(lambda: rc_delete(main_window))
        main_window.action_expand_selection.triggered.connect(lambda: rc_expand(main_window.ui.tree_object))
        main_window.action_collapse_selection.triggered.connect(lambda: rc_collapse(main_window.ui.tree_object))

    main_window.action_group_objects = menu.addAction("Group")
    main_window.action_group_objects.triggered.connect(lambda: rc_group_items(main_window))

    if logging.root.level <= logging.DEBUG:
        main_window.action_info = menu.addAction("Info")
        main_window.action_info.triggered.connect(lambda: info(main_window))
    menu.exec(main_window.ui.tree_object.viewport().mapToGlobal(position))


def info(main_window: MainWindow):
    item = selected_object(main_window).object
    logging.debug(item.name)
    logging.debug(f"parent: {item.parent}")

    if item.children:
        logging.debug("children:")
        for child in item.children:
            logging.debug(f"  {child}")
    else:
        logging.debug("no children")

    if item.aggregations:
        logging.debug("nodes:")
        for node in item.aggregations:
            logging.debug(f"   {node}")
    else:
        logging.debug("no nodes")


def rc_collapse(tree: QTreeWidget):
    for item in tree.selectedItems():
        tree.collapseItem(item)


def rc_expand(tree: QTreeWidget):
    for item in tree.selectedIndexes():
        tree.expandRecursively(item)


def copy(main_window: MainWindow):
    selected_items = main_window.ui.tree_object.selectedItems()
    item: CustomObjectTreeItem = selected_items[0]
    old_obj = item.object

    if old_obj.is_concept:
        prefil = None
    else:
        prefil = [old_obj.name,
                  old_obj.ident_attrib.property_set.name,
                  old_obj.ident_attrib.name,
                  old_obj.ident_attrib.value[0]]

    input_fields, is_concept = popups.req_group_name(main_window, prefil)
    [obj_name, ident_pset_name, ident_attrib_name, ident_value] = input_fields

    if obj_name:
        psets = list()

        for pset in old_obj.property_sets:
            new_pset = cp.copy(pset)
            psets.append(new_pset)

        if is_concept:
            new_object = classes.Object(name=obj_name, ident_attrib="Group", project=main_window.project)
        else:
            is_empty = [True for text in input_fields if not bool(text)]
            if is_empty:
                popups.msg_missing_input()
                return
            else:
                ident_attribute = None

                for pset in psets:

                    # ident pset finden
                    if pset.name == ident_pset_name:
                        merk_attrib = None
                        for attribute in pset.attributes:

                            # ident Attrib finden
                            if attribute.name == ident_attrib_name:
                                merk_attrib = attribute
                        if merk_attrib is not None:
                            ident_attribute = merk_attrib
                            ident_attribute.value = [ident_value]
                        else:
                            ident_name = ident_attrib_name
                            ident_attribute = classes.Attribute(pset, ident_name, [ident_value], value_constants.LIST)

                if ident_attribute is None:
                    ident_pset = classes.PropertySet(ident_pset_name)
                    ident_attribute = classes.Attribute(ident_pset, ident_attrib_name, [ident_value],
                                                        value_constants.LIST)
                    psets.append(ident_pset)
                new_object = classes.Object(name=obj_name, ident_attrib=ident_attribute, project=main_window.project)

        for pset in psets:
            new_object.add_property_set(pset)
        if item.parent() is None:
            parent = item.treeWidget().invisibleRootItem()
        else:
            parent = item.parent()
        add_object_to_tree(main_window.object_tree, new_object, parent)
        if old_obj.parent is not None:
            new_object.parent = old_obj.parent


def rc_group_items(main_window: MainWindow):
    input_fields, is_concept = popups.req_group_name(main_window)
    [group_name, ident_pset, ident_attrib, ident_value, abbreviation] = input_fields
    if not group_name:
        popups.msg_missing_input()
        return

    if not is_concept:
        is_empty = [True for text in input_fields if not bool(text)]
        if is_empty:
            popups.msg_missing_input()
            return

    selected_items = main_window.ui.tree_object.selectedItems()
    if len(selected_items) == 0:
        parent_classes = list()
        parent: QTreeWidgetItem = main_window.ui.tree_object.invisibleRootItem()
    else:
        parent_classes = [item for item in selected_items if item.parent() not in selected_items]
        parent = parent_classes[0].parent()
        if parent is None:
            parent: QTreeWidgetItem = main_window.ui.tree_object.invisibleRootItem()

    if is_concept:
        group_obj = classes.Object(name=group_name, ident_attrib="Group", project=main_window.project)
    else:

        pset_parent: classes.PropertySet | None = None
        if check_for_predefined_psets(ident_pset, main_window):
            result = popups.req_merge_pset()  # ask if you want to merge
            if result is True:
                pset_parent = property_widget.get_parent_by_name(main_window.active_object, ident_pset)
            elif result is None:
                return
        if pset_parent is not None:
            pset = pset_parent.create_child(ident_pset)
        else:
            pset = classes.PropertySet(ident_pset)
        identifier = create_ident(pset, ident_attrib, [ident_value])
        group_obj = classes.Object(name=group_name, ident_attrib=identifier, abbreviation=abbreviation,
                                   project=main_window.project)
        group_obj.add_property_set(pset)

    group_item: CustomObjectTreeItem = add_object_to_tree(main_window.object_tree, group_obj, parent)

    for item in parent_classes:
        child: CustomObjectTreeItem = parent.takeChild(parent.indexOfChild(item))
        group_obj.add_child(child.object)
        group_item.addChild(child)


def single_click(main_window: MainWindow, item: CustomObjectTreeItem):
    property_widget.clear_attribute_table(main_window)

    if len(main_window.ui.tree_object.selectedItems()) > 1:
        multi_selection(main_window)
        return

    obj: classes.Object = item.object
    main_window.active_object = obj
    property_widget.fill_table(main_window, obj)
    update_completer(main_window)
    fill_line_inputs(main_window, obj)

    if obj.is_concept:
        return
    table_widget = main_window.ui.table_pset

    if obj.property_sets:
        property_widget.left_click(main_window, table_widget.item(0, 0))


def fill_line_inputs(main_window: MainWindow, obj: classes.Object):
    if obj is None:
        return
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    ui.line_edit_object_name.setText(obj.name)
    if not obj.is_concept:
        text = "|".join(obj.ident_attrib.value)
        ui.lineEdit_ident_value.setText(text)
        ui.lineEdit_ident_pSet.setText(obj.ident_attrib.property_set.name)
        ui.lineEdit_ident_attribute.setText(obj.ident_attrib.name)
    else:
        ui.lineEdit_ident_value.clear()
        ui.lineEdit_ident_pSet.clear()
        ui.lineEdit_ident_attribute.clear()
    ui.line_edit_abbreviation.setText(obj.abbreviation)
    text = main_window.ui.lineEdit_pSet_name.text()
    property_widget.text_changed(main_window, text)


def set_ident_line_enable(main_window, value: bool):
    main_window.ui.lineEdit_ident_pSet.setEnabled(value)
    main_window.ui.lineEdit_ident_attribute.setEnabled(value)
    main_window.ui.lineEdit_ident_value.setEnabled(value)

    main_window.ui.lineEdit_ident_pSet.setText(" ")
    main_window.ui.lineEdit_ident_attribute.setText(" ")
    main_window.ui.lineEdit_ident_value.setText(" ")
    main_window.ui.label_Ident.setVisible(value)


def multi_selection(main_window: MainWindow):
    property_widget.set_enable(main_window, False)

    items: list[CustomObjectTreeItem] = main_window.ui.tree_object.selectedItems()

    is_concept = [item.object for item in items if item.object.is_concept]
    if is_concept:
        clear_object_input(main_window)
        if all_equal(is_concept):
            main_window.ui.line_edit_object_name.setText(is_concept[0].name)

    else:
        set_ident_line_enable(main_window, True)
        object_names = [item.object.name for item in items]
        ident_psets = [item.object.ident_attrib.property_set.name for item in items if
                       isinstance(item.object.ident_attrib, classes.Attribute)]
        ident_attributes = [item.object.ident_attrib.name for item in items]
        ident_values = [item.object.ident_attrib.value for item in items]

        line_assignment = {
            main_window.ui.line_edit_object_name: object_names,
            main_window.ui.lineEdit_ident_pSet: ident_psets,
            main_window.ui.lineEdit_ident_attribute: ident_attributes,
        }

        for key, item in line_assignment.items():

            if all_equal(item):
                key.setText(item[0])
            else:
                key.setText("*")

        if all_equal(ident_values):
            value_list = [value for value in ident_values][0]

            text = "|".join(value_list)

        else:
            text = "*"
        main_window.ui.lineEdit_ident_value.setText(text)


def check_for_predefined_psets(property_set_name, main_window):
    if property_set_name in property_widget.predefined_pset_list(
            main_window):  # if PropertySet allready predefined
        return True
    return False


def create_ident(pset: classes.PropertySet, ident_name: str, ident_value: [str]) -> classes.Attribute:
    ident_attrib: classes.Attribute = pset.get_attribute_by_name(ident_name)
    if ident_attrib is None:
        ident_attrib = classes.Attribute(pset, ident_name, ident_value, value_constants.LIST)
    else:
        ident_attrib.value = ident_value
    return ident_attrib


def add_object(main_window: MainWindow):
    def missing_input():
        for el in input_list:
            if el == "" or el is None:
                return True
        return False

    def allready_exists():
        """checks if abbreviation allready exists or if there is an object with the same ident Attribute"""
        ident_attrib_list = input_list[1:-1]
        abbreviation = input_list[-1]
        for iter_obj in classes.Object:
            ident_attrib: classes.Attribute = iter_obj.ident_attrib
            if iter_obj.is_concept:
                continue
            ident_list = [ident_attrib.property_set.name,
                          ident_attrib.name,
                          ident_attrib.value,
                          ]
            if ident_list == ident_attrib_list:
                return True
            if abbreviation == iter_obj.abbreviation:
                return True
        return False  #

    name = main_window.ui.line_edit_object_name.text()
    p_set_name = main_window.ui.lineEdit_ident_pSet.text()
    ident_attrib_name = main_window.ui.lineEdit_ident_attribute.text()
    ident_attrib_value = [main_window.ui.lineEdit_ident_value.text()]
    abbreviation = main_window.ui.line_edit_abbreviation.text()
    input_list = [name, p_set_name, ident_attrib_name, ident_attrib_value]

    if missing_input():
        popups.msg_missing_input()
        return
    if "*" in input_list:
        popups.msg_missing_input()
        return

    if allready_exists():
        popups.msg_already_exists()
        return

    parent = None
    if check_for_predefined_psets(p_set_name, main_window):
        result = popups.req_merge_pset()  # ask if you want to merge
        if result is True:
            parent = property_widget.get_parent_by_name(main_window.active_object, p_set_name)
        elif result is None:
            return

    if parent is not None:
        property_set = parent.create_child(p_set_name)
    else:
        property_set = classes.PropertySet(p_set_name)

    ident = create_ident(property_set, ident_attrib_name, ident_attrib_value)
    obj = classes.Object(name=name, ident_attrib=ident, abbreviation=abbreviation, project=main_window.project)
    obj.add_property_set(ident.property_set)
    add_object_to_tree(main_window.object_tree, obj, main_window.object_tree.invisibleRootItem())
    clear_object_input(main_window)


def add_object_to_tree(tree: QTreeWidget, obj: classes.Object, parent: QTreeWidgetItem = None,
                       treeObjectClass=CustomObjectTreeItem):
    item = treeObjectClass(obj)
    if parent is None:
        tree.invisibleRootItem().addChild(item)
    else:
        parent.addChild(item)
    return item


def rc_delete(main_window: MainWindow):
    def delete_nodes(obj: classes.Object, recursive: bool):
        for aggregation in list(obj.aggregations):
            node = main_window.graph_window.aggregation_dict().get(aggregation)
            node.delete(recursive)
        if not recursive:
            return
        for child in obj.children:
            delete_nodes(child, recursive)

    selected_tree_items = main_window.ui.tree_object.selectedItems()
    selected_objects: list[classes.Object] = [item.object for item in selected_tree_items]
    string_list = [obj.name for obj in selected_objects]

    delete_request, recursive_deletion = popups.msg_del_items(string_list, item_type=1)
    if delete_request:
        for obj in selected_objects:
            delete_nodes(obj, recursive_deletion)  # Nodes need to be deleted before object
            # because the aggregations will be deleted together with the object
            obj.delete(recursive_deletion)
    main_window.reload()


def reload(main_window: MainWindow) -> None:
    main_window.object_tree.clear()
    fill_tree(main_window.project.objects, main_window.object_tree, CustomObjectTreeItem)
    resize_tree(main_window)
    obj = main_window.active_object
    if obj is None:
        return
    fill_line_inputs(main_window, obj)
