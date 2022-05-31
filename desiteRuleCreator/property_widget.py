from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QListWidgetItem, QAbstractScrollArea,QCompleter

from . import constants, property_list_widget,classes
from .classes import PropertySet, CustomTreeItem, attributes_to_psetdict
from .io_messages import msg_del_ident_pset
from .propertyset_window import PropertySetWindow
from .QtDesigns import ui_mainwindow, ui_PsetInheritance


def get_parent_by_name(name):
    parent = None
    for pset in classes.PropertySet.iter:
        if pset.name == name:
            parent = pset
    return parent


def init(mainWindow):
    ui : ui_mainwindow.Ui_MainWindow = mainWindow.ui

    mainWindow.pset_table = mainWindow.ui.tableWidget_inherited
    mainWindow.pset_table.itemClicked.connect(mainWindow.listObjectClicked)
    mainWindow.pset_table.itemDoubleClicked.connect(mainWindow.listObjectDoubleClicked)
    mainWindow.pset_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    ui.button_Pset_add.clicked.connect(mainWindow.addPset)
    ui.button_Pset_rename.clicked.connect(mainWindow.rename_pset)
    ui.button_Pset_delete.clicked.connect(mainWindow.delete_pset)
    mainWindow.pset_buttons = [mainWindow.ui.button_Pset_add, mainWindow.ui.button_Pset_rename, mainWindow.ui.button_Pset_delete]
    ui.tab_property_set.setEnabled(False)
    mainWindow.set_right_window_enable(False)
    mainWindow.ui.lineEdit_pSet_name.textChanged.connect(mainWindow.text_changed)

def predefined_pset_list():
    property_list = [x.name for x in PropertySet.iter if x.object is None ]
    return property_list

def modify_title(self,tab,text= None):
    self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(tab), text)

def clear_all(mainWindow):
    for row in range(mainWindow.pset_table.rowCount()):
        mainWindow.pset_table.removeRow(row)
    mainWindow.ui.lineEdit_pSet_name.clear()
    mainWindow.set_right_window_enable(False)
    modify_title(mainWindow, mainWindow.ui.tab_code, "Code")
    modify_title(mainWindow, mainWindow.ui.tab_property_set, "PropertySet")

def delete(mainWindow):
    list_item = mainWindow.pset_table.selectedItems()
    object = mainWindow.active_object

    if not bool([el for el in list_item if
                 el.data(
                     constants.DATA_POS) == object.identifier.propertySet]):  # wenn sich der Identifier nicht im Pset befindet

        for el in list_item:
            el: QTableWidgetItem = el
            if el.column() == 0:
                property_set: PropertySet = el.data(constants.DATA_POS)
                property_set.delete()
                mainWindow.pset_table.selectRow(el.row())

        for i in sorted(mainWindow.pset_table.selectionModel().selectedRows()):
            mainWindow.pset_table.removeRow(i.row())

    else:
        msg_del_ident_pset(mainWindow.icon)


def rename(mainWindow):
    new_name = mainWindow.ui.lineEdit_pSet_name.text()
    list_item = mainWindow.pset_table.selectedItems()[0]
    selected_pset: PropertySet = list_item.data(constants.DATA_POS)
    list_item.setText(new_name)
    mainWindow.pset_table.resizeColumnsToContents()
    selected_pset.name = new_name

    object = selected_pset.object
    if object.identifier in selected_pset.attributes:   #rename lineinput in ObjectWidget
        tree_item: CustomTreeItem = mainWindow.ui.tree.selectedItems()[0]
        tree_item.setText(1, str(object.identifier))
    mainWindow.pset_table.resizeColumnsToContents()


def text_changed(mainWindow, text):
    if mainWindow.pset_table.findItems(text, Qt.MatchFlag.MatchExactly):
        button_text = "Update"
    else:
        button_text = "Add"
    mainWindow.ui.button_Pset_add.setText(button_text)


def set_enable(mainWindow, value: bool):
    mainWindow.ui.tab_property_set.setEnabled(value)

    if not value:

        modify_title(mainWindow,mainWindow.ui.tab_code,"Code")
        modify_title(mainWindow,mainWindow.ui.tab_property_set,"PropertySet")

        mainWindow.pset_table.setRowCount(0)
        mainWindow.ui.lineEdit_pSet_name.setText("")


def fill_table(mainWindow, obj:classes.Object):

    mainWindow.set_right_window_enable(True)
    modify_title(mainWindow,mainWindow.ui.tab_code,f"{obj.name}: Code")
    modify_title(mainWindow,mainWindow.ui.tab_property_set,f"{obj.name}: PropertySets")

    mainWindow.pset_table.setRowCount(0)
    own_psets = mainWindow.active_object.property_sets
    table_length = len(own_psets)

    # find inherited Psets
    inherited_property_sets = obj.inherited_property_sets

    for inh_obj,property_sets in inherited_property_sets.items():
        table_length+= len (inherited_property_sets[inh_obj])

    mainWindow.pset_table.setRowCount(table_length)  # Prepare Table

    for i, pset in enumerate(own_psets):
        pset:classes.PropertySet = pset
        table_item = QTableWidgetItem(pset.name)
        table_item.setData(constants.DATA_POS, pset)
        mainWindow.pset_table.setItem(i, 0, table_item)
        if pset.is_child:
            table_item = QTableWidgetItem(constants.INHERITED_TEXT)
            mainWindow.pset_table.setItem(i,1,table_item)

    current_row = len(own_psets)

    for obj, pset_list in inherited_property_sets.items():
        group_name = obj.name

        for pset in pset_list:
            pset_name = pset.name
            pset_item = QTableWidgetItem(pset_name)
            pset_item.setData(constants.DATA_POS, pset)
            inherit_item = QTableWidgetItem(group_name)
            inherit_item.setData(constants.DATA_POS, obj)
            mainWindow.pset_table.setItem(current_row, 0, pset_item)
            mainWindow.pset_table.setItem(current_row, 1, inherit_item)
            current_row += 1
    mainWindow.pset_table.resizeColumnsToContents()


def left_click(mainWindow, item: QListWidgetItem):
    ui:ui_mainwindow.Ui_MainWindow = mainWindow.ui

    table_widget = ui.tableWidget_inherited

    item = table_widget.item(table_widget.row(item),0)

    propertySet: PropertySet = item.data(constants.DATA_POS)
    mainWindow.ui.lineEdit_pSet_name.setText(propertySet.name)

def double_click(mainWindow, item: QTableWidgetItem):
    mainWindow.listObjectClicked(item)
    item = mainWindow.pset_table.item(item.row(), 0)
    propertySet: PropertySet = item.data(constants.DATA_POS)

    # Open New Window
    mainWindow.pset_window = mainWindow.openPsetWindow(propertySet,mainWindow.active_object,None)



def openPsetWindow(mainWindow,propertySet: PropertySet,active_object:classes.Object, window_title = None,):
    if window_title is None:
        window_title = f"{propertySet.object.name}:{propertySet.name}"
    window = PropertySetWindow(mainWindow,propertySet,active_object,window_title)
    return window


def addPset(mainWindow):
    ui: ui_mainwindow.Ui_MainWindow = mainWindow.ui
    name = mainWindow.ui.lineEdit_pSet_name.text()
    object = mainWindow.active_object

    inherited = False
    if name in predefined_pset_list():
        inherited = True

    item = QTableWidgetItem(name)
    new_row_count = mainWindow.pset_table.rowCount() + 1
    mainWindow.pset_table.setRowCount(new_row_count)
    mainWindow.pset_table.setItem(new_row_count - 1, 0, item)

    parent = get_parent_by_name(name)
    if inherited:
        property_set = PropertySet(name)
        if parent is not None:
            parent.add_child(property_set)
        item2 = QTableWidgetItem(constants.INHERITED_TEXT)
        mainWindow.pset_table.setItem(new_row_count - 1, 1, item2)

    else:
        property_set = PropertySet(name)

    object.add_property_set(property_set)
    item.setData(constants.DATA_POS, property_set)
    mainWindow.pset_window = mainWindow.openPsetWindow(property_set,mainWindow.active_object,None)
    mainWindow.text_changed(mainWindow.ui.lineEdit_pSet_name.text())
    mainWindow.pset_table.resizeColumnsToContents()
