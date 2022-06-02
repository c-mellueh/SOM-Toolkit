from PySide6.QtCore import QPoint, Qt, QCoreApplication
from PySide6.QtWidgets import QMenu, QTreeWidget, QAbstractItemView,QTreeWidgetItem
from PySide6.QtGui import QShortcut,QKeySequence

from . import property_widget, constants, io_messages,classes,script_widget
from .classes import Object, CustomTreeItem,  PropertySet, Attribute, CustomTree
from .io_messages import req_group_name
from .QtDesigns import ui_mainwindow

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

    def connect_items(mainView):
        mainView.ui.tree.itemClicked.connect(mainView.object_clicked)
        mainView.ui.tree.itemDoubleClicked.connect(mainView.object_double_clicked)
        mainView.ui.tree.customContextMenuRequested.connect(mainView.right_click)
        mainView.ui.button_objects_add.clicked.connect(mainView.addObject)
        mainView.ui.button_objects_delete.clicked.connect(mainView.deleteObject)
        mainView.ui.button_objects_update.clicked.connect(mainView.updateObject)
        mainView.grpSc.activated.connect(mainView.rc_group)
        mainView.delSc.activated.connect(mainView.deleteObject)

    mainView.ui.verticalLayout_objects.removeWidget(mainView.ui.tree)
    mainView.ui.tree.close()
    mainView.ui.tree = CustomTree(mainView.ui.verticalLayout_main)
    mainView.ui.verticalLayout_objects.addWidget(mainView.ui.tree)
    init_tree(mainView.ui.tree)

    mainView.ui.verticalLayout_objects.addWidget(mainView.ui.tree)
    mainView.object_buttons = [mainView.ui.button_objects_update, mainView.ui.button_objects_delete, mainView.ui.button_objects_add]
    mainView.obj_line_edit_list = [mainView.ui.lineEdit_object_name,
                                   mainView.ui.lineEdit_ident_value,
                                   mainView.ui.lineEdit_ident_attribute,
                                   mainView.ui.lineEdit_ident_pSet, ]
    mainView.delSc = QShortcut(QKeySequence('Ctrl+X'), mainView)
    mainView.grpSc = QShortcut(QKeySequence('Ctrl+G'), mainView)
    connect_items(mainView)

def selected_object(mainWindow):
    tree: classes.CustomTree = mainWindow.ui.tree
    sel_items = tree.selectedItems()
    if len(sel_items) == 1:
        return sel_items [0]
    else:
        return None

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
    mainWindow.ui.tree.clear()

    # Delete Attributes & Objects
    for object in Object.iter:
        for property_set in object.property_sets:
            property_set.delete()
    Object.iter = list()


def right_click(mainWindow, position: QPoint):
    menu = QMenu()
    mainWindow.action_group_objects = menu.addAction("Group")
    mainWindow.action_delete_attribute = menu.addAction("Delete")
    mainWindow.action_expand_selection = menu.addAction("Expand")
    mainWindow.action_collapse_selection = menu.addAction("Collapse")

    mainWindow.action_delete_attribute.triggered.connect(mainWindow.deleteObject)
    mainWindow.action_group_objects.triggered.connect(mainWindow.rc_group)
    mainWindow.action_expand_selection.triggered.connect(mainWindow.rc_expand)
    mainWindow.action_collapse_selection.triggered.connect(mainWindow.rc_collapse)
    menu.exec(mainWindow.ui.tree.viewport().mapToGlobal(position))


def rc_collapse(tree: QTreeWidget):
    for item in tree.selectedItems():
        tree.collapseItem(item)


def rc_expand(tree: QTreeWidget):
    for item in tree.selectedIndexes():
        tree.expandRecursively(item)


def rc_group_items(mainWindow):


    [group_name,ident_pset,ident_attrib,ident_value ]= req_group_name(mainWindow)
    if group_name:
        selected_items = mainWindow.ui.tree.selectedItems()
        parent_classes = [item for item in selected_items if item.parent() not in selected_items]
        parent = parent_classes[0].parent()

        if parent is None:
            parent:QTreeWidgetItem = mainWindow.ui.tree.invisibleRootItem()

        pset = PropertySet(ident_pset)
        identifier = Attribute(pset,ident_attrib,[ident_value],constants.LIST)
        group_obj = Object(group_name,identifier)

        group_item:CustomTreeItem = mainWindow.addObjectToTree(group_obj,parent)

        for item in parent_classes:
            child:classes.CustomTreeItem = parent.takeChild(parent.indexOfChild(item))
            group_obj.add_child(child.object)

            group_item.addChild(child)


def double_click(mainWindow, item: CustomTreeItem):
    obj: Object = item.object
    mainWindow.active_object = obj
    property_widget.fill_table(mainWindow, obj)
    script_widget.show(mainWindow)
    mainWindow.update_completer()

def setIdentLineEnable(mainWindow, value: bool):
    mainWindow.ui.lineEdit_ident_pSet.setEnabled(value)
    mainWindow.ui.lineEdit_ident_attribute.setEnabled(value)
    mainWindow.ui.lineEdit_ident_value.setEnabled(value)

    mainWindow.ui.lineEdit_ident_pSet.setText(" ")
    mainWindow.ui.lineEdit_ident_attribute.setText(" ")
    mainWindow.ui.lineEdit_ident_value.setText(" ")
    mainWindow.ui.label_Ident.setVisible(value)


def single_click(mainWindow):
    mainWindow.set_right_window_enable(False)


    items = mainWindow.ui.tree.selectedItems()

    is_concept =[item.object for item in items if item.object.is_concept]
    if is_concept:
        mainWindow.clearObjectInput()
        if all_equal(is_concept):
            mainWindow.ui.lineEdit_object_name.setText(is_concept[0].name)

    else:

        mainWindow.setIdentLineEnable(True)
        object_names = [item.object.name for item in items]
        ident_psets = [item.object.ident_attrib.propertySet.name for item in items]
        ident_attributes = [item.object.ident_attrib.name for item in items]
        ident_values = [item.object.ident_attrib.value for item in items]

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
        for obj in Object.iter:
            if obj.ident_attrib ==str(ident):
                return True
            else:
                if obj.ident_attrib.is_equal(ident):
                    return True
        return False

    def create_ident(pSet,identName,identValue)-> Attribute:
        ident: Attribute = pSet.get_attribute(identName)
        if ident is None:
            ident = Attribute(pSet, identName, identValue, constants.LIST)
        else:
            ident.value = identValue#

        return ident

    name = mainWindow.ui.lineEdit_object_name.text()
    pSetName = mainWindow.ui.lineEdit_ident_pSet.text()
    identName = mainWindow.ui.lineEdit_ident_attribute.text()
    identValue = [mainWindow.ui.lineEdit_ident_value.text()]

    input_list = [name, pSetName, identName, identValue]

    parent = None
    if pSetName in property_widget.predefined_pset_list():      #if PropertySet allready predefined
        result = io_messages.req_merge_pset(mainWindow.icon)    #ask if you want to merge
        if result == True:
            parent = property_widget.get_parent_by_name(mainWindow.active_object,pSetName)
        elif result is None:
            return

    pSet = PropertySet(pSetName)
    if parent is not None:
        parent.add_child(pSet)

    if not missing_input(input_list):
        if not "*" in input_list:
            ident = create_ident(pSet, identName, identValue)
            if not already_exists(ident):

                obj = Object(name, ident)
                obj.add_property_set(ident.propertySet)
                mainWindow.addObjectToTree(obj)
                mainWindow.clearObjectInput()

            else:
                ident.delete()
                io_messages.msg_already_exists(mainWindow.icon)

        else:
            io_messages.msg_missing_input(mainWindow.icon)

    else:
        io_messages.msg_missing_input(mainWindow.icon)


def addObjectToTree(mainWindow, obj: Object, parent=None):
    if parent is None:
        item = CustomTreeItem(mainWindow.ui.tree, obj)

    else:
        item = CustomTreeItem(parent, obj)

    item.setText(0, obj.name)
    if not obj.is_concept:
        item.setText(1, str(obj.ident_attrib))
    return item


def deleteObject(mainWindow):
    root:QTreeWidgetItem = mainWindow.ui.tree.invisibleRootItem()
    for item in mainWindow.ui.tree.selectedItems():
        obj:Object = item.object
        obj.delete()
        children = item.takeChildren()
        root.addChildren(children)
        (item.parent() or root).removeChild(item)
        mainWindow.project.changed = True

def updateObject(mainWindow):
    name = mainWindow.ui.lineEdit_object_name.text()
    pSetName = mainWindow.ui.lineEdit_ident_pSet.text()
    identName = mainWindow.ui.lineEdit_ident_attribute.text()
    identValue = mainWindow.ui.lineEdit_ident_value.text()

    input_list = [name, pSetName, identName, identValue]

    selected_items = mainWindow.ui.tree.selectedItems()

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
            ident = object.ident_attrib
            if not isinstance(ident,Attribute):
                property_set = PropertySet(pSetName)
                object.ident_attrib = Attribute(property_set, identName, [identValue], value_type=constants.LIST)
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
            item.setText(1, str(object.ident_attrib))

def reload_tree(mainWindow):

    def loop(item:CustomTreeItem):
        for i in range(item.childCount()):
            child = item.child(i)
            child.update()
            loop(child)

    ui: ui_mainwindow.Ui_MainWindow = mainWindow.ui
    root = ui.tree.invisibleRootItem()
    loop(root)