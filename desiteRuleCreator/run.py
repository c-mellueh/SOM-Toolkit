from QtDesigns.ui_mainwindow import Ui_MainWindow
import sys
from PySide6.QtWidgets import QApplication,QPushButton, QMainWindow,QTreeWidgetItem,QMessageBox,QFileDialog,QListWidgetItem, QMenu,QInputDialog,QTreeWidget,QTableWidgetItem,QTableWidget
from PySide6 import QtCore,QtWidgets,QtGui
from classes import Object,PropertySet,Attribute,Group, attributes_to_psetdict
import PySide6
import constants
from lxml import etree


from propertyset_window import  PropertySetWindow

def identifier_tree_text(object:Object):
    text = f"{object.identifier.propertySet.name} : {object.identifier.name} = {object.identifier.value[0]}"
    return text

def get_level(item):


    if item is not None:
        counter = 0
        while item.parent():
            counter += 1
            item = item.parent()
    else:
        return -1

    return counter

def already_exists(ident):

    for key in Object.iter.keys():
        if (key.is_equal(ident)):
            return True
    return False

def already_exists_warning():
    msgBox = QMessageBox()
    msgBox.setText("Object exists already!")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)

    icon = QtGui.QIcon(constants.ICON_PATH)
    msgBox.setWindowIcon(icon)
    msgBox.exec()

def missing_input(input_list):
    for el in input_list:
        if el == "" or el is None:
            return True
    return False

def missing_input_warning():
    msgBox = QMessageBox()
    msgBox.setText("Object informations are missing!")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)
    icon = QtGui.QIcon(constants.ICON_PATH)
    msgBox.setWindowIcon(icon)
    msgBox.exec()

def loose_unsaved_warning():
    msgBox = QMessageBox()
    msgBox.setText("Warning, unsafed progress will be lost!")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)
    msgBox.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Ok)
    icon = QtGui.QIcon(constants.ICON_PATH)
    msgBox.setWindowIcon(icon)
    if msgBox.exec() == msgBox.Ok:
        return True
    else:
        return False

def delete_or_merge():
    msgBox = QMessageBox()
    msgBox.setText("Warning, there is allready exisiting data!\n do you want to delete or merge?")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)

    msgBox.setStandardButtons(QMessageBox.Cancel)
    merge_button= msgBox.addButton("Merge",QMessageBox.NoRole)
    delete_button:QPushButton = msgBox.addButton("Delete",QMessageBox.YesRole)
    icon = QtGui.QIcon(constants.ICON_PATH)
    msgBox.setWindowIcon(icon)
    msgBox.exec()
    if msgBox.clickedButton() == merge_button:
        return False
    elif msgBox.clickedButton() == delete_button:
        return True
    else:
        return None

class CustomTree(QTreeWidget):
    def __init__(self,layout):
        super(CustomTree, self).__init__(layout)

    def dropEvent(self, event:PySide6.QtGui.QDropEvent) -> None:

        selected_items = self.selectedItems()

        if self.dropIndicatorPosition() == QtWidgets.QAbstractItemView.DropIndicatorPosition.OnItem:
            droped_on_item = self.itemFromIndex(self.indexAt(event.pos()))
            object = droped_on_item.object

            if isinstance(object,Group):
                super(CustomTree,self).dropEvent(event)

        else:
            super(CustomTree, self).dropEvent(event)

        for el in selected_items:
            object = el.object
            parent = el.parent()
            if parent is not None:
                object.parent = parent.object
            else:
                object.parent = None


class CustomTreeItem(QTreeWidgetItem):
    def __init__(self,tree,object):
        super(CustomTreeItem, self).__init__(tree)
        self._object = object


    def addChild(self, child:PySide6.QtWidgets.QTreeWidgetItem) -> None:
        super(CustomTreeItem, self).addChild(child)
        self._object.add_child(child.object)

    @property
    def object(self):
        return self._object
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.icon = QtGui.QIcon(constants.ICON_PATH)

        self.setWindowIcon(self.icon)

        self.tree = CustomTree(self.ui.verticalLayout_main)
        self.tree.setObjectName(u"treeWidget_objects")
        self.tree.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.tree.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.tree.setAlternatingRowColors(False)
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree.setSortingEnabled(True)
        self.tree.setExpandsOnDoubleClick(False)

        self.ui.verticalLayout_objects.addWidget(self.tree)
        ___qtreewidgetitem = self.tree.headerItem()
        ___qtreewidgetitem.setText(1, QtCore.QCoreApplication.translate("MainWindow", u"Identifier", None));
        ___qtreewidgetitem.setText(0, QtCore.QCoreApplication.translate("MainWindow", u"Objects", None));

        self.tree.itemClicked.connect(self.treeObjectClicked)
        self.tree.itemDoubleClicked.connect(self.treeobject_double_clicked)
        self.tree.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)
        self.tree.viewport().setAcceptDrops(True)


        self.pset_table = self.ui.tableWidget_inherited
        self.pset_table.itemClicked.connect(self.listObjectClicked)
        self.pset_table.itemDoubleClicked.connect(self.listObjectDoubleClicked)
        self.pset_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.ui.button_objects_add.clicked.connect(self.addObject)
        self.ui.button_objects_delete.clicked.connect(self.deleteObject)
        self.ui.button_objects_update.clicked.connect(self.updateObject)
        self.ui.button_Pset_add.clicked.connect(self.addPset)
        self.ui.button_Pset_rename.clicked.connect(self.rename_pset)
        self.ui.button_Pset_delete.clicked.connect(self.delete_pset)

        self.ui.action_file_Open.triggered.connect(self.openFile_dialog)
        self.ui.action_file_new.triggered.connect(self.new_file)
        self.ui.action_file_Save.triggered.connect(self.save_clicked)
        self.ui.action_file_Save_As.triggered.connect(self.save_as_clicked)

        self.pset_buttons = [self.ui.button_Pset_add,self.ui.button_Pset_rename,self.ui.button_Pset_delete]
        self.object_buttons =[self.ui.button_objects_update,self.ui.button_objects_delete,self.ui.button_objects_add]
        self.line_edit_list = [self.ui.lineEdit_object_name,self.ui.lineEdit_ident_value,self.ui.lineEdit_ident_attribute,self.ui.lineEdit_ident_pSet,self.ui.lineEdit_pSet_name]
        self.set_pset_window_enable(False)
        self.ui.lineEdit_pSet_name.textChanged.connect(self.text_changed)

        self.openFile(path= "E:/Cloud/OneDrive/Arbeit/DB_Werkstudent/Projekte/Karlsruhe_Durmersheim/Modelchecking/Regeln/Datenstruktur/22_04_18.xml")

        self.tree.resizeColumnToContents(0)
        self.save_path = None

    def save_clicked(self):
        if self.save_path is None:
            self.save_as_clicked()
        else:
            self.save(self.save_path)

    def save(self,path):
        print(f"Path: {path}")
        pass

    def save_as_clicked(self):
        if self.save_path is not None:
            self.save_path = QFileDialog.getSaveFileName(self,"Save XML", self.save_path, "xml Files (*.xml *.DRCxml)")[0]
        else:
            self.save_path = QFileDialog.getSaveFileName(self,"Save XML","", "xml Files (*.xml *.DRCxml)")[0]

        self.save(self.save_path)


    def new_file(self):
        new_file = loose_unsaved_warning()
        if new_file:
            self.clear_all()

    def clear_all(self):
        self.tree.clear()

        for row in range(self.pset_table.rowCount()):
            self.pset_table.removeRow(row)
        for el in self.line_edit_list:
            el.clear()

        for object in Object.iter.values():
            for attribute in object.attributes:
                attribute.delete()
        Object.iter = dict()
        self.set_pset_window_enable(False)

    def delete_pset(self):
        list_item = self.pset_table.selectedItems()
        object = self.tree.selectedItems()[0].object

        if not bool([el for el in list_item if el.data(constants.DATA_POS) == object.identifier.propertySet]):    #wenn sich der Identifier nicht im Pset befindet

            for el in list_item:
                el:QTableWidgetItem = el
                property_set:PropertySet = el.data(constants.DATA_POS)
                for attribute in property_set.attributes:
                    object.remove_attribute(attribute)
                self.pset_table.selectRow(el.row())
                for i in sorted(self.pset_table.selectionModel().selectedRows()):
                    self.pset_table.removeRow(i.row())

        else:
            msgBox = QMessageBox()
            msgBox.setText("can't delete Pset of Identifier!")
            msgBox.setWindowTitle(" ")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()


    def rename_pset(self):
        new_name = self.ui.lineEdit_pSet_name.text()
        list_item = self.pset_table.selectedItems()[0]
        selected_pset: PropertySet= list_item.data(constants.DATA_POS)
        list_item.setText(new_name)
        self.pset_table.resizeColumnsToContents()
        selected_pset.name = new_name

        object = selected_pset.object
        if object.identifier in selected_pset.attributes:
            tree_item: CustomTreeItem = self.tree.selectedItems()[0]
            tree_item.setText(1,identifier_tree_text(object))
        self.pset_table.resizeColumnsToContents()


    def text_changed(self, text):


        if self.pset_table.findItems(text,QtCore.Qt.MatchFlag.MatchExactly):
            button_text = "Update"
        else:
            button_text = "Add"
        self.ui.button_Pset_add.setText(button_text)


    def set_pset_window_enable(self, value: bool):
        for button in self.pset_buttons:
            button.setEnabled(value)

        self.ui.lineEdit_pSet_name.setEnabled(value)
        self.ui.label_pSet_name.setEnabled(value)
        self.pset_table.setEnabled(value)
        self.ui.tableWidget_inherited.setEnabled(value)
        if not value:
            self.ui.horizontalLayout_pSet.setTitle("PropertySet")
            self.pset_table.setRowCount(0)
            self.ui.lineEdit_pSet_name.setText("")
    def openMenu(self,position:QtCore.QPoint):

        menu = QMenu()
        self.action_group_objects = menu.addAction("Group")
        self.action_delete_objects =menu.addAction("Delete")
        self.action_expand_selection = menu.addAction("Expand")
        self.action_collapse_selection = menu.addAction("Collapse")

        self.action_delete_objects.triggered.connect(self.deleteObject)
        self.action_group_objects.triggered.connect(self.right_click_group)
        self.action_expand_selection.triggered.connect(self.expand_selection)
        self.action_collapse_selection.triggered.connect(self.collapse_selection)
        menu.exec(self.tree.viewport().mapToGlobal(position))

    def collapse_selection(self):
        for item in self.tree.selectedItems():

            self.tree.collapseItem(item)

    def expand_selection(self):
        for item in self.tree.selectedIndexes():
            self.tree.expandRecursively(item)

    def right_click_group(self):
        group_name = QInputDialog.getText(self,"Group Name","Input Name of new Group",echo=QtWidgets.QLineEdit.EchoMode.Normal,text= "")[0]

        if group_name:
            root = self.tree.invisibleRootItem()
            selected_items = self.tree.selectedItems()


            first_parent = selected_items[0].parent()
            first_level = get_level(first_parent)
            if first_level != -1:
                parent_merker = [first_level, first_parent]  # Level,Parent

                for item in selected_items:
                    parent = item.parent()
                    level = get_level(parent)

                    if level < parent_merker[0]:
                        parent_merker = [level, parent]
            else:
                parent_merker = [-1,None]

            if parent_merker[0] <0:
                parent_merker = [0, self.tree.invisibleRootItem()]

            parent = parent_merker[1]

            child_list = list()

            for item in self.tree.selectedItems():
                if not item.parent() in self.tree.selectedItems():
                    (item.parent() or root).removeChild(item)
                    child_list.append(item)

            group = CustomTreeItem(parent, Group(group_name))
            group.setText(0, group_name)
            parent.addChild(group)
            self.groupObject(group,child_list)

            if isinstance(parent,CustomTreeItem):
                group.object.parent =parent.object

    def groupObject(self,group:CustomTreeItem,items:list[CustomTreeItem]):

        for item in items:
            group.addChild(item)



    def treeobject_double_clicked(self, item:QTreeWidgetItem, column):
        object:Object = item.object
        self.set_pset_window_enable(True)
        self.ui.horizontalLayout_pSet.setTitle(f"PropertySet {object.name}")
        self.pset_table.setRowCount(0)
        own_psets = attributes_to_psetdict(object.attributes)
        table_length = len(own_psets)

        if item.parent() is not None:
            inherited_attributes = object.inherited_attributes
            inherited_psets = dict()

            for object,attributes in inherited_attributes.items():
                inherited_psets[object] = attributes_to_psetdict(attributes)
                table_length +=len(inherited_psets[object])

        self.pset_table.setRowCount(table_length)

        for i,el in enumerate(own_psets.keys()):
            table_item = QTableWidgetItem(el.name)
            table_item.setData(constants.DATA_POS,el)
            self.pset_table.setItem(i,0,table_item)

        current_row = len(own_psets)

        if item.parent() is not None:
            for group,pset_dict in inherited_psets.items():
                group_name = group.name

                for pset in pset_dict.keys():
                    pset_name = pset.name
                    pset_item = QTableWidgetItem(pset_name)
                    pset_item.setData(constants.DATA_POS, pset)
                    inherit_item = QTableWidgetItem(group_name)
                    inherit_item.setData(constants.DATA_POS,group)

                    self.pset_table.setItem(current_row,0,pset_item)
                    self.pset_table.setItem(current_row,1,inherit_item)
                    current_row+=1

        self.active_object = object
        self.pset_table.resizeColumnsToContents()



    def setIdentLineEnable(self,value:bool):
        self.ui.lineEdit_ident_pSet.setEnabled(value)
        self.ui.lineEdit_ident_attribute.setEnabled(value)
        self.ui.lineEdit_ident_value.setEnabled(value)

        self.ui.lineEdit_ident_pSet.setText(" ")
        self.ui.lineEdit_ident_attribute.setText(" ")
        self.ui.lineEdit_ident_value.setText(" ")
        self.ui.label_Ident.setVisible(value)


    def treeObjectClicked(self,item:QTreeWidgetItem,column):
        def all_equal(iterator):
            iterator = iter(iterator)
            try:
                first = next(iterator)
            except StopIteration:
                return True
            return all(first == x for x in iterator)

        items = self.tree.selectedItems()
        self.set_pset_window_enable(False)

        group_selected = [item.object.name for item in items if isinstance(item.object,Group)]
        if group_selected:
            if all_equal(group_selected):
                self.ui.lineEdit_object_name.setText(group_selected[0])
            self.setIdentLineEnable(False)


        else:
            self.setIdentLineEnable(True)
            object_names = [item.object.name for item in items]
            ident_psets = [item.object.identifier.propertySet.name for item in items]
            ident_attributes = [item.object.identifier.name for item in items]
            ident_values = [item.object.identifier.value[0] for item in items]

            line_assignment =  {
                self.ui.lineEdit_object_name:object_names,
                self.ui.lineEdit_ident_pSet: ident_psets,
                self.ui.lineEdit_ident_attribute: ident_attributes,
                self.ui.lineEdit_ident_value: ident_values,
            }

            for key,item in line_assignment.items():

                if all_equal(item):
                    key.setText(item[0])
                else:
                    key.setText("*")


    def group_clicked(self):
        for el in self.pset_buttons:
            el.setDisabled(True)


    def clearObjectInput(self):
        self.ui.lineEdit_ident_attribute.clear()
        self.ui.lineEdit_ident_value.clear()
        self.ui.lineEdit_ident_pSet.clear()
        self.ui.lineEdit_object_name.clear()

    def addObject(self):


        name = self.ui.lineEdit_object_name.text()
        pSetName = self.ui.lineEdit_ident_pSet.text()
        identName = self.ui.lineEdit_ident_attribute.text()
        identValue = [self.ui.lineEdit_ident_value.text()]

        input_list=[name,pSetName,identName,identValue]

        pSet = PropertySet(pSetName)
        ident = Attribute(pSet,identName,identValue,constants.LIST)

        if not missing_input(input_list):
            if not  "*" in input_list:

                if not already_exists(ident):

                        obj = Object(name, ident)
                        self.addObjectToTree(obj)
                        self.clearObjectInput()


                else:already_exists_warning()

            else:missing_input_warning()

        else:missing_input_warning()

    def addObjectToTree(self,obj:Object,parent = None):

        if parent is None:item = CustomTreeItem(self.tree,obj)

        else:  item = CustomTreeItem(parent,obj)

        item.setText(0, obj.name)
        item.setText(1,identifier_tree_text(obj))
        return item

    def openFile_dialog(self,path = False):
        if Object.iter:
            result = delete_or_merge()
            if result is None:
                return
            elif result:
                self.clear_all()
                self.openFile(path)
            else:
                self.merge_new_file()
                self.openFile(path)

        else:
            self.openFile(path)

    def merge_new_file(self):
        print("MERGE NEEDS TO BE PROGRAMMED")   #TODO: Write Merge

    def openFile(self,path = False):

        def transform_values(xml_object,value_type):
            value_list = list()
            if value_type == constants.LIST or value_type == constants.FORMAT:
                for xml_value in xml_object:
                    value_list.append(xml_value.attrib.get("Wert"))

            if value_type == constants.RANGE:
                for xml_value in xml_object:
                    domain = xml_value.attrib.get("Wert").split(":")
                    if len(domain)>1 :
                        value_list.append([float(domain[0]),float(domain[1])])
                    else:
                        value_list.append(domain)

            return value_list

        def transform_value_types(value_type):
            if value_type == "Wert":
                value_type = constants.LIST
            elif value_type == "Bereich":
                value_type = constants.RANGE
            elif value_type == "Format":
                value_type = constants.FORMAT
            else:
                raise ImportWarning(f"Imported ValueType {value_type} not known")
            return value_type

        if path is False:
            path = QFileDialog.getOpenFileName(self,"Open XML", "", "xml Files (*.xml *.DRCxml)")[0]

        if path:
            self.clearObjectInput()

            ### OlD FILE

            tree:etree._ElementTree = etree.parse(path)

            projekt_xml:etree._Element = tree.getroot()

            groups_with_duplicates = [group.attrib.get("Fachdisziplin") for group in projekt_xml if group.tag == "Objekt"]
            groups_without_duplicates = dict.fromkeys(groups_with_duplicates)

            parent = self.tree.invisibleRootItem()
            for group_name in groups_without_duplicates:
                group = CustomTreeItem(parent, Group(group_name))
                group.setText(0, group_name)
                parent.addChild(group)
                groups_without_duplicates[group_name] = group



            for xml_objects in projekt_xml:
                if (xml_objects.tag == "Objekt"):
                    attributes = xml_objects.attrib

                    identifier_string: str = attributes.get("Identifier")
                    pSet = PropertySet(identifier_string.split(":")[0])
                    attribute = Attribute(pSet,identifier_string.split(":")[1], [attributes.get("Name")],constants.LIST )


                    group_name = attributes.get("Fachdisziplin")

                    obj = Object(attributes.get("Name"), attribute)
                    self.addObjectToTree(obj,groups_without_duplicates[group_name])
                    obj.parent= groups_without_duplicates[group_name]._object

                    for xml_property_set in xml_objects:
                        psetName = xml_property_set.attrib.get("Name")
                        if psetName in obj.psetNameDict:
                            pSet = obj.psetNameDict[psetName]
                        else:
                            pSet = PropertySet(psetName)
                        for xml_attribute in xml_property_set:
                            attrib = xml_attribute.attrib
                            name = attrib.get("Name")
                            value_type = transform_value_types(attrib.get("Art"))
                            data_type = attrib.get("Datentyp")

                            value = transform_values(xml_attribute, value_type)


                            atrb = Attribute(pSet,name,value,value_type,data_type)
                            obj.add_attribute(atrb)

        self.tree.resizeColumnToContents(0)

    def listObjectClicked(self,item:QListWidgetItem):
        propertySet:PropertySet = item.data(constants.DATA_POS)
        self.ui.lineEdit_pSet_name.setText(propertySet.name)

    def listObjectDoubleClicked(self,item:QListWidgetItem):
        self.listObjectClicked(item)
        propertySet:PropertySet = item.data(constants.DATA_POS)

        #Open New Window
        self.pset_window = self.openPsetWindow(propertySet)

    def openPsetWindow(self,propertySet:PropertySet):
        window = PropertySetWindow(propertySet)
        return window

    def deleteObject(self):


        root = self.tree.invisibleRootItem()
        for item  in self.tree.selectedItems():
            obj = item.object

            obj.delete()
            (item.parent() or root).removeChild(item)

    def updateObject(self):
        name = self.ui.lineEdit_object_name.text()
        pSetName = self.ui.lineEdit_ident_pSet.text()
        identName = self.ui.lineEdit_ident_attribute.text()
        identValue = [self.ui.lineEdit_ident_value.text()]

        input_list = [name, pSetName, identName, identValue]


        empty_input = False

        for el in input_list:
            if not bool(el):
                empty_input = True

        if empty_input:
            missing_input_warning()
        else:
            for item in self.tree.selectedItems():
                object: Object = item.object

                ident = object.identifier


                if name != object.name and name != "*":
                    object.name = name
                if pSetName != ident.propertySet.name and pSetName != "*":
                    ident.propertySet = PropertySet(pSetName)

                if identName != ident.name and identName != "*":
                    ident.name = identName

                if identValue != ident.value and identValue != "*":
                    ident.value = identValue

                item.setText(0,object.name)
                item.setText(1, f"{ident.propertySet.name} : {ident.name} = {ident.value[0]}")

    def addPset(self):
        name = self.ui.lineEdit_pSet_name.text()
        items = self.tree.selectedItems()

        if len(items)==1:
            object = items[0].object
            property_set = PropertySet(name)
            property_set.object = object
            item = QTableWidgetItem(name)
            item.setData(constants.DATA_POS, property_set)
            new_row_count = self.pset_table.rowCount()+1

            self.pset_table.setRowCount(new_row_count)

            self.pset_table.setItem(new_row_count-1,0,item)

            self.pset_window = self.openPsetWindow(property_set)
            self.text_changed(self.ui.lineEdit_pSet_name.text())

        self.pset_table.resizeColumnsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.resize(1200, 550)

    sys.exit(app.exec())




def main():
    pass
