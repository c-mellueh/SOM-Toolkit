from QtDesigns.ui_mainwindow import Ui_MainWindow
import sys
from PySide6.QtWidgets import QApplication, QMainWindow,QTreeWidgetItem,QMessageBox,QFileDialog,QListWidgetItem, QMenu,QInputDialog,QTreeWidget
from PySide6 import QtCore,QtWidgets
from classes import Object,PropertySet,Attribute,Group
import PySide6
import constants
from lxml import etree

from propertyset_window import  PropertySetWindow

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
    msgBox.exec()



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

        self.tree = CustomTree(self.ui.verticalLayout_main)
        self.tree.setObjectName(u"treeWidget_objects")
        self.tree.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.tree.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.tree.setAlternatingRowColors(False)
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree.setSortingEnabled(True)
        #self.tree.setDropIndicatorShown(False)

        self.ui.verticalLayout_objects.addWidget(self.tree)
        ___qtreewidgetitem = self.tree.headerItem()
        ___qtreewidgetitem.setText(1, QtCore.QCoreApplication.translate("MainWindow", u"Identifier", None));
        ___qtreewidgetitem.setText(0, QtCore.QCoreApplication.translate("MainWindow", u"Objects", None));

        self.tree.itemClicked.connect(self.treeObjectClicked)
        self.tree.itemDoubleClicked.connect(self.show_pset_info)
        self.tree.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)


        self.list = self.ui.listWidget_pSet
        self.list.itemClicked.connect(self.listObjectClicked)
        self.list.itemDoubleClicked.connect(self.listObjectDoubleClicked)

        self.ui.button_objects_add.clicked.connect(self.addObject)
        self.ui.button_objects_delete.clicked.connect(self.deleteObject)
        self.ui.button_objects_update.clicked.connect(self.updateObject)

        self.ui.button_Pset_add.clicked.connect(self.addPset)

        self.ui.action_file_Open.triggered.connect(self.openFile)
        self.openFile(path= "E:/Cloud/OneDrive/Arbeit/DB_Werkstudent/Projekte/Karlsruhe_Durmersheim/Modelchecking/Regeln/Datenstruktur/22_04_18.xml")
        self.tree.viewport().setAcceptDrops(True)

        self.pset_buttons = [self.ui.button_Pset_add,self.ui.button_Pset_edit,self.ui.button_Pset_delete,self.ui.button_Pset_update]
        self.object_buttons =[self.ui.button_objects_update,self.ui.button_objects_delete,self.ui.button_objects_add]



    def openMenu(self,position:QtCore.QPoint):

        menu = QMenu()
        self.ui.action_group_objects = menu.addAction("Group")
        self.ui.action_delete_objects =menu.addAction("Delete")
        self.ui.action_delete_objects.triggered.connect(self.deleteObject)
        self.ui.action_group_objects.triggered.connect(self.groupObject)

        menu.exec(self.tree.viewport().mapToGlobal(position))

    def groupObject(self):



        group_name = QInputDialog.getText(self,"Group Name","Input Name of new Group",echo=QtWidgets.QLineEdit.EchoMode.Normal,text= "")[0]
        root = self.tree.invisibleRootItem()

        first_parent = self.tree.selectedItems()[0].parent()
        first_level = get_level(first_parent)


        if first_level != -1:
            parent_merker = [first_level,first_parent] #Level,Parent

            for item in self.tree.selectedItems():
                parent = item.parent()
                level = get_level(parent)
                if level < parent_merker[0]:
                    parent_merker = [level,parent]

        else:
            parent_merker = [0,self.tree.invisibleRootItem()]

        group = CustomTreeItem(parent_merker[1],Group(group_name))
        group.setText(0, group_name)

        print("HIER")

        for item in self.tree.selectedItems():
            if item != group:
                if not item.parent() in self.tree.selectedItems():

                    (item.parent() or root).removeChild(item)
                    group.addChild(item)

        print(parent_merker)

        parent_merker[1].addChild(group)
        print(parent_merker[1])
        if isinstance(parent_merker[1],CustomTreeItem):
            print("HIER")
            group.object.parent = parent_merker[1].object

    def show_pset_info(self, item:QTreeWidgetItem, column):
        object:Object = item.object
        print(object.parent)
        if isinstance(object,Object):

            psets = object.attributes_to_psetdict()

            self.ui.listWidget_pSet.clear()

            for el in psets.keys():
                item = QListWidgetItem(el.name,self.ui.listWidget_pSet)
                item.setData(1,el)


            pass

    def treeObjectClicked(self,item:QTreeWidgetItem,column):

        items = self.tree.selectedItems()

        identicals = [True,True,True,True] #Name,PSet,Attrib,Value
        lineEditList = [
            self.ui.lineEdit_object_name,
            self.ui.lineEdit_ident_pSet,
            self.ui.lineEdit_ident_attribute,
            self.ui.lineEdit_ident_value
            ]

        merk_list = ["","","",""]

        is_first = True

        for item in items:

            object:Object = item.object
            if isinstance(object,Object):
                if is_first:
                    merk_list = [object.name, object.identifier.propertySet.name, object.identifier.name,
                                 object.identifier.value]
                    is_first = False
                else:
                    compare_list = [object.name, object.identifier.propertySet.name, object.identifier.name,
                                    object.identifier.value]

                    for i, el in enumerate(compare_list):
                        if el != merk_list[i]:
                            identicals[i] = False

        for i in range(len(identicals)):
            if identicals[i]:
                lineEditList[i].setText(merk_list[i])
            else:
                lineEditList[i].setText("*")

        if len(items) ==1:
            self.show_pset_info(items[0],column)

        else:
            self.ui.listWidget_pSet.clear()


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
        identValue = self.ui.lineEdit_ident_value.text()

        input_list=[name,pSetName,identName,identValue]

        pSet = PropertySet(pSetName)
        ident = Attribute(pSet,identName,identValue,constants.VALUE)

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
        item.setText(1, f"{obj.identifier.propertySet.name} : {obj.identifier.name} = {obj.identifier.value}")

    def openFile(self,path = None):

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

        if path is None:
            path = QFileDialog.getOpenFileName(self,"Open XML", "", "xml Files (*.xml *.DRCxml)")[0]
        self.clearObjectInput()


        ### OlD FILE

        tree = etree.parse(path)
        projekt_xml = tree.getroot()

        for xml_objects in projekt_xml:
            if (xml_objects.tag == "Objekt"):
                attributes = xml_objects.attrib

                identifier_string: str = attributes.get("Identifier")
                pSet = PropertySet(identifier_string.split(":")[0])
                attribute = Attribute(pSet,identifier_string.split(":")[1], attributes.get("Name"),constants.VALUE )

                obj = Object(attributes.get("Name"), attribute)
                self.addObjectToTree(obj)

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

    def listObjectClicked(self,item:QListWidgetItem):
        propertySet:PropertySet = item.data(1)
        self.ui.lineEdit_pSet_name.setText(propertySet.name)

    def listObjectDoubleClicked(self,item:QListWidgetItem):
        self.listObjectClicked(item)
        propertySet:PropertySet = item.data(1)

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
        identValue = self.ui.lineEdit_ident_value.text()

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
                item.setText(1, f"{ident.propertySet.name} : {ident.name} = {ident.value}")

    def addPset(self):
        name = self.ui.lineEdit_pSet_name.text()

        items = self.tree.selectedItems()
        if len(items)==1:
            object = items[0].object
            property_set = PropertySet(name)
            property_set.object = object
            self.ui.listWidget_pSet.addItem(QListWidgetItem(name))
            self.pset_window = self.openPsetWindow(property_set)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())




def main():
    pass
