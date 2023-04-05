from __future__ import annotations

import copy as cp
import logging
from typing import TYPE_CHECKING
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QShortcut, QKeySequence, QDropEvent
from PySide6.QtWidgets import QMenu, QTreeWidget, QAbstractItemView, QTreeWidgetItem,QWidget,QTableWidgetItem
from SOMcreator import classes, constants

from ..qt_designs import ui_mainwindow,ui_search
from ..widgets import script_widget, property_widget
from ..windows import popups
from ..icons import get_icon
if TYPE_CHECKING:
    from ..main_window import MainWindow

from fuzzywuzzy import fuzz

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

    def object_dict(self) -> dict[classes.Object,CustomObjectTreeItem]:
        obj_dict = dict()
        def add_to_dict(item:CustomObjectTreeItem):
            obj_dict[item.object]=item
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
            self.setCheckState(3, Qt.CheckState.Checked)
        else:
            self.setCheckState(3, Qt.CheckState.Unchecked)

    def update(self) -> None:
        logging.debug(f"Item toggled if item is not Toggled contact me")
        check_state = self.checkState(2)
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

def init(main_window: MainWindow):
    def init_tree(tree: CustomTree):
        # Design Tree
        tree.setObjectName(u"treeWidget_objects")
        tree.setDragDropMode(QAbstractItemView.InternalMove)
        tree.setDefaultDropAction(Qt.MoveAction)
        tree.setAlternatingRowColors(False)
        tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        tree.setSortingEnabled(True)
        tree.setExpandsOnDoubleClick(False)
        tree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        tree.setContextMenuPolicy(Qt.CustomContextMenu)
        tree.viewport().setAcceptDrops(True)

        ___qtreewidgetitem = tree.headerItem()
        ___qtreewidgetitem.setText(0, "Objects")
        ___qtreewidgetitem.setText(1, "Identifier")
        ___qtreewidgetitem.setText(2, "Abbreviation")
        ___qtreewidgetitem.setText(3, "Optional")

    def connect_items():
        ui: ui_mainwindow.Ui_MainWindow = main_window.ui
        ui.tree_object.itemClicked.connect(main_window.object_clicked)
        ui.tree_object.itemChanged.connect(main_window.item_changed)
        ui.tree_object.itemExpanded.connect(main_window.resize_tree)
        ui.tree_object.customContextMenuRequested.connect(main_window.right_click)
        ui.button_objects_add.clicked.connect(main_window.add_object)
        main_window.grpSc.activated.connect(main_window.rc_group)
        main_window.delSc.activated.connect(main_window.delete_object)
        main_window.srchSc.activated.connect(main_window.search_object)

    main_window.ui.verticalLayout_objects.removeWidget(main_window.ui.tree_object)
    main_window.ui.tree_object.close()
    main_window.ui.tree_object = CustomTree(main_window.ui.verticalLayout_main)
    main_window.ui.verticalLayout_objects.addWidget(main_window.ui.tree_object)
    init_tree(main_window.ui.tree_object)

    main_window.ui.verticalLayout_objects.addWidget(main_window.ui.tree_object)
    main_window.object_buttons = [main_window.ui.button_objects_add]

    main_window.delSc = QShortcut(QKeySequence('Ctrl+X'), main_window)
    main_window.grpSc = QShortcut(QKeySequence('Ctrl+G'), main_window)
    main_window.srchSc = QShortcut(QKeySequence('Ctrl+F'),main_window)
    connect_items()


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
    for el in main_window.obj_line_edit_list:
        el.clear()


def clear_all(main_window: MainWindow):
    # Clean Widget
    clear_object_input(main_window)
    main_window.ui.tree_object.clear()

    # Delete Attributes & Objects
    for obj in classes.Object:
        obj.delete()

class SearchItem(QTableWidgetItem):
    def __init__(self,object:classes.Object,text:str|None):
        super(SearchItem, self).__init__()
        self.object = object
        if text is None:
            text = ""
        self.setFlags(self.flags().ItemIsSelectable|self.flags().ItemIsEnabled)
        self.setText(text)


class SearchWindow(QWidget):
    def __init__(self, main_window:MainWindow,):
        super(SearchWindow, self).__init__()

        def connect_items():
            self.widget.lineEdit.textChanged.connect(self.update_table)
            self.widget.tableWidget.itemDoubleClicked.connect(self.item_clicked)

        self.widget = ui_search.Ui_Search()
        self.widget.setupUi(self)
        self.setWindowTitle("Search")
        self.setWindowIcon(get_icon())
        self.main_window = main_window
        self.main_window.search_ui = self
        self.project:classes.Project = self.main_window.project
        self.show()
        self.widget.tableWidget.verticalHeader().setVisible(False)
        self.row_dict = dict()
        self.item_dict: dict[classes.Object,list[SearchItem]] = {obj:[SearchItem(obj,obj.name),SearchItem(obj,obj.ident_value),SearchItem(obj,"100")] for obj in self.project.objects}

        self.fill_table()
        table_header = self.widget.tableWidget.horizontalHeader()
        table_header.setStretchLastSection(True)
        table_header.setSectionResizeMode(0,table_header.ResizeMode.ResizeToContents)
        self.widget.tableWidget.setColumnHidden(2,True)
        self.widget.tableWidget.sortByColumn(2,Qt.SortOrder.AscendingOrder)
        self.widget.tableWidget.setSortingEnabled(True)
        self.objects = set(obj for obj in self.project.objects)
        connect_items()

    def get_row(self,obj):
        return self.item_dict[obj][0].row()

    def fill_table(self):

        table = self.widget.tableWidget
        table.setRowCount(len(self.item_dict))
        for row,(obj,items) in enumerate(self.item_dict.items()):
            for column,item in enumerate(items):
                table.setItem(row,column,item)
            self.row_dict[obj] = row



    def item_clicked(self,table_item:SearchItem):
        obj = table_item.object
        tree:CustomTree = self.main_window.object_tree

        for selected_item in tree.selectedItems():
            selected_item.setSelected(False)

        tree_item = tree.object_dict()[obj]
        tree_item.setSelected(True)
        tree_item.expand_to_me()
        self.main_window.object_clicked(tree_item)
        tree.scrollToItem(tree_item)
        self.hide()

    def update_table(self):
        table = self.widget.tableWidget
        text = self.widget.lineEdit.text().lower()
        possible_objects = set()
        for obj in self.objects:
            value1 = fuzz.partial_ratio(text.lower(),obj.name.lower())
            value2 = fuzz.partial_ratio(text.lower(),str(obj.ident_value))
            value = max(value2,value1)
            row = self.get_row(obj)
            table.item(row,2).setText(str(value))
            if value>75:
                possible_objects.add(obj)

        forbidden_objects = self.objects.difference(possible_objects)
        for obj in possible_objects:
            table.showRow(self.get_row(obj))
        for obj in forbidden_objects:
            table.hideRow(self.get_row(obj))

def search_object(main_window:MainWindow):
    sw = SearchWindow(main_window)

def right_click(main_window: MainWindow, position: QPoint):
    menu = QMenu()

    selected_items = main_window.ui.tree_object.selectedItems()
    if len(selected_items) == 1:
        main_window.action_copy = menu.addAction("Copy")
        main_window.action_copy.triggered.connect(main_window.copy_object)

    if len(selected_items) != 0:
        main_window.action_delete_attribute = menu.addAction("Delete")
        main_window.action_expand_selection = menu.addAction("Expand")
        main_window.action_collapse_selection = menu.addAction("Collapse")
        main_window.action_delete_attribute.triggered.connect(main_window.delete_object)
        main_window.action_expand_selection.triggered.connect(main_window.rc_expand)
        main_window.action_collapse_selection.triggered.connect(main_window.rc_collapse)

    main_window.action_group_objects = menu.addAction("Group")
    main_window.action_group_objects.triggered.connect(main_window.rc_group)

    if logging.root.level <= logging.DEBUG:
        main_window.action_info = menu.addAction("Info")
        main_window.action_info.triggered.connect(main_window.info)
    menu.exec(main_window.ui.tree_object.viewport().mapToGlobal(position))


def info(main_window: MainWindow):
    item = selected_object(main_window).object
    print(item.name)
    print(f"parent: {item.parent}")

    if item.children:
        print("children:")
        for child in item.children:
            print(f"  {child}")
    else:
        print("no children")

    if item.aggregation_representations:
        print("nodes:")
        for node in item.aggregation_representations:
            print(f"   {node}")
    else:
        print("no nodes")


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
            new_object = classes.Object(obj_name, "Group")
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
                            ident_attribute = classes.Attribute(pset, ident_name, [ident_value], constants.LIST)

                if ident_attribute is None:
                    ident_pset = classes.PropertySet(ident_pset_name)
                    ident_attribute = classes.Attribute(ident_pset, ident_attrib_name, [ident_value], constants.LIST)
                    psets.append(ident_pset)
                new_object = classes.Object(obj_name, ident_attribute)

        for pset in psets:
            new_object.add_property_set(pset)
        if item.parent() is None:
            parent = item.treeWidget().invisibleRootItem()
        else:
            parent = item.parent()
        main_window.add_object_to_tree(new_object, parent)
        if old_obj.parent is not None:
            new_object.parent = old_obj.parent


def rc_group_items(main_window: MainWindow):
    input_fields, is_concept = popups.req_group_name(main_window)
    [group_name, ident_pset, ident_attrib, ident_value] = input_fields

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
        group_obj = classes.Object(group_name, "Group")
    else:
        pset = classes.PropertySet(ident_pset)
        identifier = classes.Attribute(pset, ident_attrib, [ident_value], constants.LIST)
        group_obj = classes.Object(group_name, identifier)
        group_obj.add_property_set(pset)

    group_item: CustomObjectTreeItem = main_window.add_object_to_tree(group_obj, parent)

    for item in parent_classes:
        child: CustomObjectTreeItem = parent.takeChild(parent.indexOfChild(item))
        group_obj.add_child(child.object)
        group_item.addChild(child)


def single_click(main_window: MainWindow, item: CustomObjectTreeItem):
    property_widget.clear_attribute_table(main_window)

    if len(main_window.ui.tree_object.selectedItems()) > 1:
        main_window.multi_selection()
        return

    obj: classes.Object = item.object
    main_window.active_object = obj
    property_widget.fill_table(main_window, obj)
    script_widget.show(main_window)
    main_window.update_completer()
    fill_line_inputs(main_window, obj)

    if obj.is_concept:
        return
    table_widget = main_window.ui.table_pset
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
    main_window.text_changed(main_window.ui.lineEdit_pSet_name.text())


def set_ident_line_enable(main_window, value: bool):
    main_window.ui.lineEdit_ident_pSet.setEnabled(value)
    main_window.ui.lineEdit_ident_attribute.setEnabled(value)
    main_window.ui.lineEdit_ident_value.setEnabled(value)

    main_window.ui.lineEdit_ident_pSet.setText(" ")
    main_window.ui.lineEdit_ident_attribute.setText(" ")
    main_window.ui.lineEdit_ident_value.setText(" ")
    main_window.ui.label_Ident.setVisible(value)


def multi_selection(main_window: MainWindow):
    main_window.set_right_window_enable(False)

    items = main_window.ui.tree_object.selectedItems()

    is_concept = [item.object for item in items if item.object.is_concept]
    if is_concept:
        main_window.clear_object_input()
        if all_equal(is_concept):
            main_window.ui.line_edit_object_name.setText(is_concept[0].name)

    else:

        main_window.set_ident_line_enable(True)
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

    def create_ident(pset: classes.PropertySet, ident_name: str, ident_value: [str]) -> classes.Attribute:
        ident_attrib: classes.Attribute = pset.get_attribute_by_name(ident_name)
        if ident_attrib is None:
            ident_attrib = classes.Attribute(pset, ident_name, ident_value, constants.LIST)
        else:
            ident_attrib.value = ident_value  #

        return ident_attrib

    name = main_window.ui.line_edit_object_name.text()
    p_set_name = main_window.ui.lineEdit_ident_pSet.text()
    ident_attrib_name = main_window.ui.lineEdit_ident_attribute.text()
    ident_attrib_value = [main_window.ui.lineEdit_ident_value.text()]
    abbreviation = main_window.ui.line_edit_abbreviation.text()
    input_list = [name, p_set_name, ident_attrib_name, ident_attrib_value, abbreviation]

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
    if p_set_name in property_widget.predefined_pset_list(
            main_window):  # if PropertySet allready predefined
        result = popups.req_merge_pset()  # ask if you want to merge
        if result:
            parent = property_widget.get_parent_by_name(main_window.active_object, p_set_name)
        elif result is None:
            return

    if parent is not None:
        property_set = parent.create_child(p_set_name)
    else:
        property_set = classes.PropertySet(p_set_name)

    ident = create_ident(property_set, ident_attrib_name, ident_attrib_value)
    obj = classes.Object(name, ident, abbreviation=abbreviation)
    obj.add_property_set(ident.property_set)
    main_window.add_object_to_tree(obj)
    main_window.clear_object_input()


def add_object_to_tree(main_window: MainWindow, obj: classes.Object, parent: QTreeWidgetItem = None):
    item = CustomObjectTreeItem(obj)
    if parent is None:
        main_window.object_tree.invisibleRootItem().addChild(item)
    else:
        parent.addChild(item)
    return item


def rc_delete(main_window: MainWindow):
    def delete_item(item: CustomObjectTreeItem) -> None:
        parent = item.parent()
        invisible_root = main_window.ui.tree_object.invisibleRootItem()
        item.object.delete()
        for index in reversed(range(item.childCount())):
            child = item.child(index)
            delete_item(child)
        (parent or invisible_root).removeChild(item)

    def append_string_list(obj: classes.Object) -> None:
        nonlocal string_list
        string_list.append(str(obj.name))
        print(f"{obj.name} : {len(obj.children)}")
        for child in obj.children:
            child: classes.Object
            print(f"{obj.name} -> {child.name}")
            append_string_list(child)
        pass

    string_list = list()

    loop_item: CustomObjectTreeItem
    for loop_item in main_window.ui.tree_object.selectedItems():
        print(f"selected_item: {loop_item.object.name}")
        append_string_list(loop_item.object)

    delete_request = popups.msg_del_items(string_list)

    if delete_request:
        for loop_item in main_window.ui.tree_object.selectedItems():
            delete_item(loop_item)
        main_window.project.changed = True


def reload_tree(main_window):
    def loop(item: CustomObjectTreeItem):
        for i in range(item.childCount()):
            child = item.child(i)
            child.refresh()
            loop(child)

    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    root = ui.tree_object.invisibleRootItem()
    loop(root)


def reload(main_window):
    reload_tree(main_window)
    obj = main_window.active_object
    fill_line_inputs(main_window, obj)
