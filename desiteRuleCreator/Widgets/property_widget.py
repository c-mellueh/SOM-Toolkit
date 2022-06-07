from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QListWidgetItem, QAbstractScrollArea

from desiteRuleCreator.QtDesigns import ui_mainwindow
from desiteRuleCreator.Windows.popups import msg_del_ident_pset
from desiteRuleCreator.Windows.propertyset_window import PropertySetWindow
from desiteRuleCreator.data import classes, constants
from desiteRuleCreator.data.classes import PropertySet, CustomTreeItem


def get_parent_by_name(active_object: classes.Object, name: str):
    pset: PropertySet
    for pset in PropertySet.iter:
        is_master = pset.parent is None
        correct_name = pset.name == name
        if active_object is not None:
            is_same_obj = pset.object == active_object
        else:
            is_same_obj = False

        if is_master and correct_name and not is_same_obj:
            return pset


def init(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui

    main_window.pset_table = main_window.ui.tableWidget_inherited
    main_window.pset_table.itemClicked.connect(main_window.list_object_clicked)
    main_window.pset_table.itemDoubleClicked.connect(main_window.list_object_double_clicked)
    main_window.pset_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    ui.button_Pset_add.clicked.connect(main_window.add_pset)
    ui.button_Pset_rename.clicked.connect(main_window.rename_pset)
    ui.button_Pset_delete.clicked.connect(main_window.delete_pset)
    main_window.pset_buttons = [main_window.ui.button_Pset_add, main_window.ui.button_Pset_rename,
                                main_window.ui.button_Pset_delete]
    ui.tab_property_set.setEnabled(False)
    main_window.set_right_window_enable(False)
    main_window.ui.lineEdit_pSet_name.textChanged.connect(main_window.text_changed)


def predefined_pset_list() -> list[PropertySet]:
    property_list = [x.name for x in PropertySet.iter if x.parent is None]
    return property_list


def modify_title(self, tab, text=None):
    self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(tab), text)


def clear_all(main_window):
    for row in range(main_window.pset_table.rowCount()):
        main_window.pset_table.removeRow(row)
    main_window.ui.lineEdit_pSet_name.clear()
    main_window.set_right_window_enable(False)
    modify_title(main_window, main_window.ui.tab_code, "Code")
    modify_title(main_window, main_window.ui.tab_property_set, "PropertySet")


def delete(main_window):
    list_item = main_window.pset_table.selectedItems()
    obj = main_window.active_object

    if not bool([el for el in list_item if
                 el.data(
                     constants.DATA_POS) == obj.ident_attrib.property_set]):
                        #wenn sich der Identifier nicht im Pset befindet

        for el in list_item:
            el: QTableWidgetItem = el
            if el.column() == 0:
                property_set: PropertySet = el.data(constants.DATA_POS)

                if property_set.is_child:
                    property_set.parent.remove_child(property_set)
                else:
                    property_set.delete()
                main_window.pset_table.selectRow(el.row())

        for i in sorted(main_window.pset_table.selectionModel().selectedRows()):
            main_window.pset_table.removeRow(i.row())

    else:
        msg_del_ident_pset()


def rename(main_window):
    new_name = main_window.ui.lineEdit_pSet_name.text()
    list_item = main_window.pset_table.selectedItems()[0]
    selected_pset: PropertySet = list_item.data(constants.DATA_POS)
    list_item.setText(new_name)
    main_window.pset_table.resizeColumnsToContents()
    selected_pset.name = new_name

    obj = selected_pset.object
    if obj.ident_attrib in selected_pset.attributes:  # rename lineinput in ObjectWidget
        tree_item: CustomTreeItem = main_window.ui.tree.selectedItems()[0]
        tree_item.setText(1, str(obj.ident_attrib))
    main_window.pset_table.resizeColumnsToContents()


def text_changed(main_window, text):
    if main_window.pset_table.findItems(text, Qt.MatchFlag.MatchExactly):
        button_text = "Update"
    else:
        button_text = "Add"
    main_window.ui.button_Pset_add.setText(button_text)


def set_enable(main_window, value: bool):
    main_window.ui.tab_property_set.setEnabled(value)

    if not value:
        modify_title(main_window, main_window.ui.tab_code, "Code")
        modify_title(main_window, main_window.ui.tab_property_set, "PropertySet")

        main_window.pset_table.setRowCount(0)
        main_window.ui.lineEdit_pSet_name.setText("")


def fill_table(main_window, obj: classes.Object):
    main_window.set_right_window_enable(True)
    modify_title(main_window, main_window.ui.tab_code, f"{obj.name}: Code")
    modify_title(main_window, main_window.ui.tab_property_set, f"{obj.name}: PropertySets")

    main_window.pset_table.setRowCount(0)
    own_psets = main_window.active_object.property_sets
    table_length = len(own_psets)

    # find inherited Psets

    main_window.pset_table.setRowCount(table_length)  # Prepare Table

    for i, pset in enumerate(own_psets):
        pset: classes.PropertySet = pset
        table_item = QTableWidgetItem(pset.name)
        table_item.setData(constants.DATA_POS, pset)
        main_window.pset_table.setItem(i, 0, table_item)
        if pset.is_child:
            if pset.parent.object is not None:
                table_item = QTableWidgetItem(pset.parent.object.name)
            else:
                table_item = QTableWidgetItem(constants.INHERITED_TEXT)
            main_window.pset_table.setItem(i, 1, table_item)

    current_row = len(own_psets)

    main_window.pset_table.resizeColumnsToContents()


def left_click(main_window, item: QListWidgetItem):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui

    table_widget = ui.tableWidget_inherited

    item = table_widget.item(table_widget.row(item), 0)

    property_set: PropertySet = item.data(constants.DATA_POS)
    main_window.ui.lineEdit_pSet_name.setText(property_set.name)


def double_click(main_window, item: QTableWidgetItem):
    main_window.list_object_clicked(item)
    item = main_window.pset_table.item(item.row(), 0)
    property_set: PropertySet = item.data(constants.DATA_POS)

    # Open New Window
    main_window.pset_window = main_window.open_pset_window(property_set, main_window.active_object, None)


def open_pset_window(main_window, property_set: PropertySet, active_object: classes.Object, window_title=None, ):
    if window_title is None:
        window_title = f"{property_set.object.name}:{property_set.name}"
    window = PropertySetWindow(main_window, property_set, active_object, window_title)
    return window


def add_pset(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    name = main_window.ui.lineEdit_pSet_name.text()
    obj = main_window.active_object

    inherited = False
    if name in predefined_pset_list():
        inherited = True

    item = QTableWidgetItem(name)
    new_row_count = main_window.pset_table.rowCount() + 1
    main_window.pset_table.setRowCount(new_row_count)
    main_window.pset_table.setItem(new_row_count - 1, 0, item)

    parent = get_parent_by_name(main_window.active_object, name)
    if inherited:
        property_set = PropertySet(name)
        if parent is not None:
            parent.add_child(property_set)

        if parent.object is not None:
            item2 = QTableWidgetItem(parent.object.name)
        else:
            item2 = QTableWidgetItem(constants.INHERITED_TEXT)
        main_window.pset_table.setItem(new_row_count - 1, 1, item2)

    else:
        property_set = PropertySet(name)

    obj.add_property_set(property_set)
    item.setData(constants.DATA_POS, property_set)
    main_window.pset_window = main_window.open_pset_window(property_set, main_window.active_object, None)
    main_window.text_changed(main_window.ui.lineEdit_pSet_name.text())
    main_window.pset_table.resizeColumnsToContents()


def reload(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    if main_window.active_object is not None:
        fill_table(main_window, main_window.active_object)