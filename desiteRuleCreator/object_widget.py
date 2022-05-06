from PySide6.QtCore import QPoint, Qt, QCoreApplication
from PySide6.QtWidgets import QMenu, QTreeWidget, QAbstractItemView,QTreeWidgetItem
from PySide6.QtGui import QShortcut,QKeySequence

from . import property_widget, constants, io_messages
from .classes import Object, CustomTreeItem,  PropertySet, Attribute, CustomTree
from .io_messages import req_group_name


def init(mainView):
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
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Identifier", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Objects", None));

    def connect_items(self):
        self.tree.itemClicked.connect(self.treeObjectClicked)
        self.tree.itemDoubleClicked.connect(self.object_double_clicked)
        self.tree.customContextMenuRequested.connect(self.right_click)
        self.ui.button_objects_add.clicked.connect(self.addObject)
        self.ui.button_objects_delete.clicked.connect(self.deleteObject)
        self.ui.button_objects_update.clicked.connect(self.updateObject)

    mainView.tree = CustomTree(mainView.ui.verticalLayout_main)
    init_tree(mainView.tree)
    connect_items(mainView)
    mainView.ui.verticalLayout_objects.addWidget(mainView.tree)
    mainView.object_buttons = [mainView.ui.button_objects_update, mainView.ui.button_objects_delete, mainView.ui.button_objects_add]
    mainView.obj_line_edit_list = [mainView.ui.lineEdit_object_name,
                                   mainView.ui.lineEdit_ident_value,
                                   mainView.ui.lineEdit_ident_attribute,
                                   mainView.ui.lineEdit_ident_pSet, ]

    mainView.delSc = QShortcut(QKeySequence('Ctrl+X'), mainView)
    mainView.delSc.activated.connect(mainView.deleteObject)

    mainView.delSc = QShortcut(QKeySequence('Ctrl+G'), mainView)
    mainView.delSc.activated.connect(mainView.rc_group)

def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)

def clear_object_input(mainWindow):
    for el in mainWindow.obj_line_edit_list:
        el.clear()


def clear_all(mainWindow):
    # Clean Widget
    clear_object_input(mainWindow)
    mainWindow.tree.clear()

    # Delete Attributes & Objects
    for object in Object.iter.values():
        for attribute in object.attributes:
            attribute.delete()
    Object.iter = dict()


def right_click(mainWindow, position: QPoint):
    menu = QMenu()
    mainWindow.action_group_objects = menu.addAction("Group")
    mainWindow.action_delete_objects = menu.addAction("Delete")
    mainWindow.action_expand_selection = menu.addAction("Expand")
    mainWindow.action_collapse_selection = menu.addAction("Collapse")

    mainWindow.action_delete_objects.triggered.connect(mainWindow.deleteObject)
    mainWindow.action_group_objects.triggered.connect(mainWindow.rc_group)
    mainWindow.action_expand_selection.triggered.connect(mainWindow.rc_expand)
    mainWindow.action_collapse_selection.triggered.connect(mainWindow.rc_collapse)
    menu.exec(mainWindow.tree.viewport().mapToGlobal(position))


def rc_collapse(tree: QTreeWidget):
    for item in tree.selectedItems():
        tree.collapseItem(item)


def rc_expand(tree: QTreeWidget):
    for item in tree.selectedIndexes():
        tree.expandRecursively(item)


def rc_group_items(mainWindow):


    [group_name,ident_pset,ident_attrib,ident_value ]= req_group_name(mainWindow)
    if group_name:
        selected_items = mainWindow.tree.selectedItems()
        parent_classes = [item for item in selected_items if item.parent() not in selected_items]
        parent = parent_classes[0].parent()

        if parent is None:
            parent = mainWindow.tree.invisibleRootItem()

        pset = PropertySet(ident_pset)
        identifier = Attribute(pset,ident_attrib,[ident_value],constants.LIST)
        group_obj = Object(group_name,identifier)
        group_obj.add_attribute(identifier)

        group_item:CustomTreeItem = mainWindow.addObjectToTree(group_obj,parent)

        for item in parent_classes:
            parent.removeChild(item)
            group_item.addChild(item)


def double_click(mainWindow, item: CustomTreeItem):
    obj: Object = item.object
    mainWindow.active_object = obj
    property_widget.fill_table(mainWindow, item, obj)


def setIdentLineEnable(mainWindow, value: bool):
    mainWindow.ui.lineEdit_ident_pSet.setEnabled(value)
    mainWindow.ui.lineEdit_ident_attribute.setEnabled(value)
    mainWindow.ui.lineEdit_ident_value.setEnabled(value)

    mainWindow.ui.lineEdit_ident_pSet.setText(" ")
    mainWindow.ui.lineEdit_ident_attribute.setText(" ")
    mainWindow.ui.lineEdit_ident_value.setText(" ")
    mainWindow.ui.label_Ident.setVisible(value)


def single_click(mainWindow):

    items = mainWindow.tree.selectedItems()
    mainWindow.set_pset_window_enable(False)

    is_concept =[item.object for item in items if item.object.is_concept]
    if is_concept:
        mainWindow.clearObjectInput()
        if all_equal(is_concept):
            mainWindow.ui.lineEdit_object_name.setText(is_concept[0].name)

    else:

        mainWindow.setIdentLineEnable(True)
        object_names = [item.object.name for item in items]
        ident_psets = [item.object.identifier.propertySet.name for item in items]
        ident_attributes = [item.object.identifier.name for item in items]
        ident_values = [item.object.identifier.value for item in items]

        line_assignment = {
            mainWindow.ui.lineEdit_object_name: object_names,
            mainWindow.ui.lineEdit_ident_pSet: ident_psets,
            mainWindow.ui.lineEdit_ident_attribute: ident_attributes,
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
        mainWindow.ui.lineEdit_ident_value.setText(text)

def addObject(mainWindow):
    def missing_input(input_list):
        for el in input_list:
            if el == "" or el is None:
                return True
        return False

    def already_exists(ident):
        for key in Object.iter.keys():
            if (key.is_equal(ident)):
                return True
        return False

    name = mainWindow.ui.lineEdit_object_name.text()
    pSetName = mainWindow.ui.lineEdit_ident_pSet.text()
    identName = mainWindow.ui.lineEdit_ident_attribute.text()
    identValue = [mainWindow.ui.lineEdit_ident_value.text()]

    input_list = [name, pSetName, identName, identValue]

    pSet = PropertySet(pSetName)
    ident = Attribute(pSet, identName, identValue, constants.LIST)

    if not missing_input(input_list):
        if not "*" in input_list:

            if not already_exists(ident):

                obj = Object(name, ident)
                mainWindow.addObjectToTree(obj)
                mainWindow.clearObjectInput()


            else:
                io_messages.msg_already_exists(mainWindow.icon)

        else:
            io_messages.msg_missing_input(mainWindow.icon)

    else:
        io_messages.msg_missing_input(mainWindow.icon)


def addObjectToTree(mainWindow, obj: Object, parent=None):
    if parent is None:
        item = CustomTreeItem(mainWindow.tree, obj)

    else:
        item = CustomTreeItem(parent, obj)

    item.setText(0, obj.name)
    if not obj.is_concept:
        item.setText(1, str(obj.identifier))
    return item


def deleteObject(mainWindow):
    root:QTreeWidgetItem = mainWindow.tree.invisibleRootItem()
    for item in mainWindow.tree.selectedItems():
        obj = item.object
        obj.delete()

        children = item.takeChildren()
        root.addChildren(children)
        (item.parent() or root).removeChild(item)
    mainWindow.changed = True

def updateObject(mainWindow):
    name = mainWindow.ui.lineEdit_object_name.text()
    pSetName = mainWindow.ui.lineEdit_ident_pSet.text()
    identName = mainWindow.ui.lineEdit_ident_attribute.text()
    identValue = mainWindow.ui.lineEdit_ident_value.text()

    input_list = [name, pSetName, identName, identValue]

    selected_items = mainWindow.tree.selectedItems()

    if len(selected_items) >1 and not "*" in input_list:
        io_messages.msg_identical_identifier(mainWindow.icon)
        return
    empty_input = False
    for el in input_list:
        if not bool(el):
            empty_input = True

    if empty_input:
        io_messages.msg_missing_input(mainWindow.icon)
        return

    else:
        for item in selected_items:
            object: Object = item.object
            ident = object.identifier
            if not isinstance(ident,Attribute):
                property_set = PropertySet(pSetName)
                object.identifier = Attribute(property_set,identName,[identValue],value_type=constants.LIST)
                object.add_attribute(object.identifier)
                object.is_concept = False

            else:
                if name != "*":
                    object.name = name
                if pSetName != "*":
                    ident.propertySet = PropertySet(pSetName)

                if identName != "*":
                    ident.name = identName

                if identValue != "*":
                    ident.value = [identValue]

            item.setText(0, object.name)
            item.setText(1, str(object.identifier))
