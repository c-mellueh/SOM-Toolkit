from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QTableWidgetItem, QListWidgetItem, QAbstractScrollArea, QMenu, QCompleter, QWidget
from SOMcreator import classes, constants

from ..qt_designs import ui_mainwindow
from ..windows import popups, propertyset_window
from ..windows.popups import msg_del_ident_pset, msg_del_items
from ..windows.propertyset_window import PropertySetWindow
from . import object_widget
if TYPE_CHECKING:
    from ..main_window import MainWindow


def get_parent_by_name(active_object: classes.Object, name: str) -> classes.PropertySet | None:
    """find Propertyset which has the same name and is not from the same object"""

    for pset in classes.PropertySet:
        is_master = pset.parent is None
        correct_name = pset.name == name
        if active_object is not None:
            is_same_obj = pset.object == active_object
        else:
            is_same_obj = False

        if is_master and correct_name and not is_same_obj:
            return pset


def init(main_window: MainWindow) -> None:
    def connect() -> None:
        main_window.pset_table.itemClicked.connect(lambda item: left_click(main_window, item))
        main_window.pset_table.itemDoubleClicked.connect(lambda item: double_click(main_window,item))
        main_window.ui.table_attribute.itemDoubleClicked.connect(lambda item: attribute_double_click(main_window, item))
        main_window.ui.lineEdit_pSet_name.textChanged.connect(lambda text: text_changed(main_window,text))
        main_window.pset_table.customContextMenuRequested.connect(lambda position: open_menu(main_window, position))
        main_window.ui.button_Pset_add.clicked.connect(lambda: create_new_pset(main_window))

    main_window.pset_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
    main_window.ui.box_layout_pset.setEnabled(False)
    set_enable(main_window,False)
    connect()


def open_menu(main_window: MainWindow, position: QPointF) -> None:
    menu = QMenu()
    main_window.action_pset_delete_attribute = menu.addAction("Delete")
    main_window.action_pset_rename_attribute = menu.addAction("Rename")
    main_window.action_pset_delete_attribute.triggered.connect(lambda: delete_selection(main_window))
    main_window.action_pset_rename_attribute.triggered.connect(lambda: rename(main_window))
    menu.exec(main_window.pset_table.viewport().mapToGlobal(position))


def predefined_pset_list(main_window: MainWindow) -> set[str]:
    def iterate_parents(parent: classes.Object) -> None:
        if parent is not None:
            for property_set in parent.property_sets:
                property_list.add(property_set.name)
            iterate_parents(parent.parent)

    property_list = {pset.name for pset in classes.PropertySet if pset.object is None}

    if main_window.active_object is not None:
        iterate_parents(main_window.active_object.parent)
        completer = QCompleter(property_list)
        main_window.ui.lineEdit_pSet_name.setCompleter(completer)
    return property_list


def modify_title(main_window: MainWindow, tab: QWidget, text: str = None) -> None:
    main_window.ui.tabWidget.setTabText(main_window.ui.tabWidget.indexOf(tab), text)


def clear_all(main_window: MainWindow) -> None:
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    for row in range(main_window.pset_table.rowCount()):
        main_window.pset_table.removeRow(row)

    for row in range(ui.table_attribute.rowCount()):
        ui.table_attribute.removeRow(row)

    main_window.ui.lineEdit_pSet_name.clear()
    set_enable(main_window,False)
    modify_title(main_window, main_window.ui.tab_code, "Code")
    modify_title(main_window, main_window.ui.tab_property_set, "PropertySet")


def delete_selection(main_window: MainWindow) -> None:
    list_item: list[propertyset_window.CustomTableItem] = main_window.pset_table.selectedItems()
    property_sets: list[classes.PropertySet] = [item.linked_data for item in list_item if item.column() == 0]
    row_list = [item.row() for item in list_item if item.column() == 0]

    obj = main_window.active_object
    delete_request = msg_del_items([pset.name for pset in property_sets],item_type=3)

    if not delete_request:
        return

    if obj.ident_attrib.property_set in property_sets:
        msg_del_ident_pset()
        return

    for property_set in property_sets:
        if property_set.is_child:
            property_set.parent.remove_child(property_set)
        else:
            property_set.delete()

    for i in sorted(row_list, reverse=True):
        main_window.pset_table.removeRow(i)


def rename(main_window: MainWindow) -> None:
    list_item: propertyset_window.CustomTableItem = main_window.pset_table.selectedItems()[0]
    selected_pset: classes.PropertySet = list_item.linked_data
    return_str = popups.req_pset_name(main_window, selected_pset.name)

    if return_str[1]:
        new_name = return_str[0]
        if new_name in [pset.name for pset in main_window.active_object.property_sets]:
            popups.msg_already_exists()
            return
        list_item.setText(new_name)
        main_window.pset_table.resizeColumnsToContents()
        selected_pset.name = new_name
        object_widget.reload(main_window)


def text_changed(main_window: MainWindow, text: str) -> None:
    """if name of pset allready exists -> disable add button"""
    if main_window.pset_table.findItems(text, Qt.MatchFlag.MatchExactly):
        main_window.ui.button_Pset_add.setEnabled(False)
    else:
        main_window.ui.button_Pset_add.setEnabled(True)


def set_enable(main_window: MainWindow, value: bool) -> None:
    main_window.ui.box_layout_pset.setEnabled(value)

    if not value:
        main_window.pset_table.setRowCount(0)
        main_window.ui.table_attribute.setRowCount(0)
        main_window.ui.lineEdit_pSet_name.setText("")


def left_click(main_window: MainWindow, item: QListWidgetItem) -> None:
    item: propertyset_window.CustomTableItem = main_window.pset_table.item(
        main_window.pset_table.row(item), 0)

    property_set: classes.PropertySet = item.linked_data
    propertyset_window.fill_attribute_table(main_window.active_object, main_window.ui.table_attribute, property_set)
    main_window.ui.lineEdit_pSet_name.setText(property_set.name)


def attribute_double_click(main_window: MainWindow, item: propertyset_window.CustomTableItem) -> None:
    item: propertyset_window.CustomTableItem = item.tableWidget().item(item.row(), 0)
    attribute: classes.Attribute = item.linked_data
    property_set = attribute.property_set
    open_pset_window(main_window, property_set, main_window.active_object, None)
    main_window.property_set_window.table_clicked(item)


def double_click(main_window: MainWindow, item: QTableWidgetItem) -> None:
    left_click(main_window, item)
    item: propertyset_window.CustomTableItem = main_window.pset_table.item(item.row(), 0)
    property_set: classes.PropertySet = item.linked_data

    # Open New Window
    open_pset_window(main_window, property_set, main_window.active_object, None)

def open_pset_window(main_window: MainWindow, property_set: classes.PropertySet,
                     active_object: classes.Object, window_title=None, ) -> None:
    if window_title is None:
        window_title = f"{property_set.object.name}:{property_set.name}"

    window = PropertySetWindow(main_window, property_set, active_object, window_title)
    main_window.property_set_window = window


def fill_table(main_window: MainWindow, obj: classes.Object) -> None:
    set_enable(main_window,True)
    main_window.pset_table.setRowCount(0)
    property_sets = main_window.active_object.property_sets
    # find inherited Psets
    for pset in property_sets:
        add_pset_to_table(main_window, pset)


def add_pset_to_table(main_window: MainWindow, pset: str | classes.PropertySet, parent=None) -> None:
    row_index = main_window.pset_table.rowCount()
    main_window.pset_table.setRowCount(row_index + 1)
    if isinstance(pset, str):
        name = pset
        if parent is not None:
            property_set = parent.create_child(name)
        else:
            property_set = classes.PropertySet(name)
        main_window.active_object.add_property_set(property_set)

    else:
        property_set = pset

    if property_set.is_child:
        if property_set.parent.object is not None:
            inherit_table_item = propertyset_window.CustomTableItem(pset, pset.parent.object.name)
        else:
            inherit_table_item = propertyset_window.CustomTableItem(pset, constants.INHERITED_TEXT)
        main_window.pset_table.setItem(row_index, 1, inherit_table_item)

    pset_table_item = propertyset_window.CustomTableItem(property_set, property_set.name)
    main_window.pset_table.setItem(row_index, 0, pset_table_item)
    check_item = propertyset_window.CustomCheckItem(property_set)

    if property_set.optional:
        check_item.setCheckState(Qt.CheckState.Checked)
    else:
        check_item.setCheckState(Qt.CheckState.Unchecked)
    main_window.pset_table.setItem(row_index, 2, check_item)

    main_window.pset_table.resizeColumnsToContents()


def create_new_pset(main_window: MainWindow) -> None:
    name = main_window.ui.lineEdit_pSet_name.text()
    inherited = False
    if name in predefined_pset_list(main_window):
        inherited = popups.req_merge_pset()

    parent = None
    if inherited:
        parent = get_parent_by_name(main_window.active_object, name)

    add_pset_to_table(main_window, name, parent)
    text_changed(main_window,main_window.ui.lineEdit_pSet_name.text())


def reload(main_window: MainWindow) -> None:
    if main_window.active_object is not None:
        fill_table(main_window, main_window.active_object)
        if main_window.property_set_window is not None:
            propertyset_window.fill_attribute_table(main_window.active_object, main_window.ui.table_attribute,
                                                    main_window.property_set_window.property_set)


def clear_attribute_table(main_window: MainWindow) -> None:
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    table_widget = ui.table_attribute
    table_widget.setRowCount(0)
