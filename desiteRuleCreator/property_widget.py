from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QListWidgetItem, QAbstractScrollArea

from . import constants
from .classes import PropertySet, CustomTreeItem, attributes_to_psetdict
from .io_messages import msg_del_ident_pset
from .propertyset_window import PropertySetWindow
from .QtDesigns import ui_mainwindow

def init(self):
    self.pset_table = self.ui.tableWidget_inherited
    self.pset_table.itemClicked.connect(self.listObjectClicked)
    self.pset_table.itemDoubleClicked.connect(self.listObjectDoubleClicked)
    self.pset_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    self.ui.button_Pset_add.clicked.connect(self.addPset)
    self.ui.button_Pset_rename.clicked.connect(self.rename_pset)
    self.ui.button_Pset_delete.clicked.connect(self.delete_pset)
    self.pset_buttons = [self.ui.button_Pset_add, self.ui.button_Pset_rename, self.ui.button_Pset_delete]


    ui : ui_mainwindow.Ui_MainWindow = self.ui
    ui.tab_property_set.setEnabled(False)
    self.set_right_window_enable(False)
    self.ui.lineEdit_pSet_name.textChanged.connect(self.text_changed)

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
    object = mainWindow.uitree.selectedItems()[0].object

    if not bool([el for el in list_item if
                 el.data(
                     constants.DATA_POS) == object.identifier.propertySet]):  # wenn sich der Identifier nicht im Pset befindet

        for el in list_item:
            el: QTableWidgetItem = el
            property_set: PropertySet = el.data(constants.DATA_POS)
            for attribute in property_set.attributes:
                object.remove_attribute(attribute)
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
    if object.identifier in selected_pset.attributes:
        tree_item: CustomTreeItem = mainWindow.uitree.selectedItems()[0]
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


def fill_table(mainWindow, item: CustomTreeItem, obj):
    mainWindow.set_right_window_enable(True)
    modify_title(mainWindow,mainWindow.ui.tab_code,f"{obj.name}: Code")
    modify_title(mainWindow,mainWindow.ui.tab_property_set,f"{obj.name}: PropertySets")

    mainWindow.pset_table.setRowCount(0)
    own_psets = attributes_to_psetdict(obj.attributes)
    table_length = len(own_psets)

    # find inherited Psets
    if item.parent() is not None:
        inherited_attributes = obj.inherited_attributes
        inherited_psets = dict()

        for obj, attributes in inherited_attributes.items():
            inherited_psets[obj] = attributes_to_psetdict(attributes)
            table_length += len(inherited_psets[obj])

    mainWindow.pset_table.setRowCount(table_length)  # Prepare Table

    for i, el in enumerate(own_psets.keys()):
        table_item = QTableWidgetItem(el.name)
        table_item.setData(constants.DATA_POS, el)
        mainWindow.pset_table.setItem(i, 0, table_item)

    current_row = len(own_psets)

    if item.parent() is not None:
        for group, pset_dict in inherited_psets.items():
            group_name = group.name

            for pset in pset_dict.keys():
                pset_name = pset.name
                pset_item = QTableWidgetItem(pset_name)
                pset_item.setData(constants.DATA_POS, pset)
                inherit_item = QTableWidgetItem(group_name)
                inherit_item.setData(constants.DATA_POS, group)

                mainWindow.pset_table.setItem(current_row, 0, pset_item)
                mainWindow.pset_table.setItem(current_row, 1, inherit_item)
                current_row += 1
    mainWindow.pset_table.resizeColumnsToContents()


def left_click(mainWindow, item: QListWidgetItem):
    propertySet: PropertySet = item.data(constants.DATA_POS)
    mainWindow.ui.lineEdit_pSet_name.setText(propertySet.name)


def double_click(mainWindow, item: QTableWidgetItem):
    mainWindow.listObjectClicked(item)
    item = mainWindow.pset_table.item(item.row(), 0)
    propertySet: PropertySet = item.data(constants.DATA_POS)

    # Open New Window
    mainWindow.pset_window = mainWindow.openPsetWindow(propertySet)


def openPsetWindow(propertySet: PropertySet):
    window = PropertySetWindow(propertySet)
    return window


def addPset(mainWindow):
    name = mainWindow.ui.lineEdit_pSet_name.text()
    items = mainWindow.uitree.selectedItems()

    if len(items) == 1:
        object = items[0].object
        property_set = PropertySet(name)
        property_set.object = object
        item = QTableWidgetItem(name)
        item.setData(constants.DATA_POS, property_set)
        new_row_count = mainWindow.pset_table.rowCount() + 1

        mainWindow.pset_table.setRowCount(new_row_count)

        mainWindow.pset_table.setItem(new_row_count - 1, 0, item)

        mainWindow.pset_window = mainWindow.openPsetWindow(property_set)
        mainWindow.text_changed(mainWindow.ui.lineEdit_pSet_name.text())

    mainWindow.pset_table.resizeColumnsToContents()
