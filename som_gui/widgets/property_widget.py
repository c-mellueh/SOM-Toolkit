from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QTableWidgetItem, QListWidgetItem, QAbstractScrollArea, QMenu
from SOMcreator import classes, json_constants

from . import object_widget
from ..qt_designs import ui_mainwindow
from ..windows import popups, propertyset_window
from ..windows.popups import msg_del_ident_pset, msg_del_items
from ..windows.propertyset_window import PropertySetWindow

if TYPE_CHECKING:
    from ..main_window import MainWindow

from ..windows.propertyset_window import ATTRIBUTE_DATA_ROLE


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
        main_window.pset_table.itemDoubleClicked.connect(lambda item: double_click(main_window, item))
        main_window.ui.table_attribute.itemDoubleClicked.connect(lambda item: attribute_double_click(main_window, item))
        main_window.ui.lineEdit_pSet_name.textChanged.connect(lambda text: text_changed(main_window, text))
        main_window.pset_table.customContextMenuRequested.connect(lambda position: open_menu(main_window, position))
        main_window.ui.button_Pset_add.clicked.connect(lambda: create_new_pset(main_window))

    main_window.pset_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
    main_window.ui.box_layout_pset.setEnabled(False)
    set_enable(main_window, False)
    connect()


def open_menu(main_window: MainWindow, position: QPointF) -> None:
    menu = QMenu()
    main_window.action_pset_delete_attribute = menu.addAction("Delete")
    main_window.action_pset_rename_attribute = menu.addAction("Rename")
    main_window.action_pset_delete_attribute.triggered.connect(lambda: delete_selection(main_window))
    main_window.action_pset_rename_attribute.triggered.connect(lambda: rename(main_window))
    menu.exec(main_window.pset_table.viewport().mapToGlobal(position))


def predefined_pset_dict(proj: classes.Project) -> dict[str, classes.PropertySet]:
    return {pset.name: pset for pset in proj.get_predefined_psets()}


def clear_all(main_window: MainWindow) -> None:
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    for row in range(main_window.pset_table.rowCount()):
        main_window.pset_table.removeRow(row)

    for row in range(ui.table_attribute.rowCount()):
        ui.table_attribute.removeRow(row)

    main_window.ui.lineEdit_pSet_name.clear()
    set_enable(main_window, False)


def delete_selection(main_window: MainWindow) -> None:
    list_item: list[QTableWidgetItem] = main_window.pset_table.selectedItems()
    property_sets: list[classes.PropertySet] = [i.data(ATTRIBUTE_DATA_ROLE) for i in list_item if i.column() == 0]
    row_list = [item.row() for item in list_item if item.column() == 0]

    obj = main_window.active_object
    delete_request, recursive_deletion = msg_del_items([pset.name for pset in property_sets], item_type=3)

    if not delete_request:
        return

    if obj.ident_attrib.property_set in property_sets:
        msg_del_ident_pset()
        return

    for property_set in property_sets:
        if property_set.is_child:
            property_set.parent.remove_child(property_set)
        else:
            property_set.delete(recursive_deletion)

    for i in sorted(row_list, reverse=True):
        main_window.pset_table.removeRow(i)


def rename(main_window: MainWindow) -> None:
    list_item: QTableWidgetItem = main_window.pset_table.selectedItems()[0]
    selected_pset: classes.PropertySet = list_item.data(ATTRIBUTE_DATA_ROLE)
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
    item: QTableWidgetItem = main_window.pset_table.item(
        main_window.pset_table.row(item), 0)

    property_set: classes.PropertySet = item.data(ATTRIBUTE_DATA_ROLE)
    select_property_set(main_window, property_set)


def select_property_set(main_window: MainWindow, property_set: classes.PropertySet) -> None:
    propertyset_window.fill_attribute_table(main_window.active_object, main_window.ui.table_attribute, property_set)
    main_window.ui.lineEdit_pSet_name.setText(property_set.name)
    main_window.active_property_set = property_set


def attribute_double_click(main_window: MainWindow, item: QTableWidgetItem) -> None:
    attribute: classes.Attribute = item.data(ATTRIBUTE_DATA_ROLE)
    property_set = attribute.property_set
    open_pset_window(main_window, property_set, main_window.active_object, None)
    main_window.property_set_window.table_clicked(item)


def double_click(main_window: MainWindow, item: QTableWidgetItem) -> None:
    left_click(main_window, item)
    property_set: classes.PropertySet = item.data(ATTRIBUTE_DATA_ROLE)
    # Open New Window
    open_pset_window(main_window, property_set, main_window.active_object, None)


def open_pset_window(main_window: MainWindow, property_set: classes.PropertySet,
                     active_object: classes.Object, window_title=None, ) -> None:
    if window_title is None:
        window_title = f"{property_set.object.name}:{property_set.name}"

    window = PropertySetWindow(main_window, property_set, active_object, window_title)
    main_window.property_set_window = window


def fill_table(main_window: MainWindow, obj: classes.Object) -> None:
    set_enable(main_window, True)
    main_window.pset_table.setRowCount(0)
    property_sets = obj.property_sets
    # find inherited Psets
    for pset in property_sets:
        add_pset_to_table(main_window, pset)


def add_pset_to_table(main_window: MainWindow, pset: str | classes.PropertySet, parent=None) -> None:
    items = [QTableWidgetItem() for _ in range(3)]
    table = main_window.pset_table

    row_index = main_window.pset_table.rowCount()
    main_window.pset_table.setRowCount(row_index + 1)
    if isinstance(pset, str):
        property_set = parent.create_child(pset) if parent is not None else classes.PropertySet(pset)
        main_window.active_object.add_property_set(property_set)
    else:
        property_set = pset

    [item.setData(ATTRIBUTE_DATA_ROLE, property_set) for item in items]
    [table.setItem(row_index, col_index, item) for col_index, item in enumerate(items)]

    if property_set.is_child:
        text = property_set.parent.name if property_set.parent.object is not None else json_constants.INHERITED_TEXT
        items[1].setText(text)
    items[0].setText(property_set.name)
    check_state = Qt.CheckState.Checked if property_set.optional else Qt.CheckState.Unchecked
    items[2].setCheckState(check_state)

    table.resizeColumnsToContents()


def create_new_pset(main_window: MainWindow) -> None:
    name = main_window.ui.lineEdit_pSet_name.text()
    inherited = False
    if name in predefined_pset_dict(main_window.project).keys():
        inherited = popups.req_merge_pset()

    parent = None
    if inherited:
        parent = predefined_pset_dict(main_window.project).get(name)

    add_pset_to_table(main_window, name, parent)
    text_changed(main_window, main_window.ui.lineEdit_pSet_name.text())


def reload(main_window: MainWindow) -> None:
    active_object = main_window.active_object
    if active_object is None:
        return
    fill_table(main_window, active_object)
    pset_window = main_window.property_set_window
    if pset_window is not None:
        propertyset_window.fill_attribute_table(active_object, main_window.ui.table_attribute,
                                                pset_window.property_set)

    active_pset = main_window.active_property_set
    if active_pset is not None and active_pset in active_object.property_sets:
        select_property_set(main_window, active_pset)


def clear_attribute_table(main_window: MainWindow) -> None:
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    table_widget = ui.table_attribute
    table_widget.setRowCount(0)
