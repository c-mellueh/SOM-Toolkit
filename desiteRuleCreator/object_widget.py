from .classes import Object,CustomTreeItem,Group,PropertySet,Attribute,identifier_tree_text,CustomTree
from .io_messages import req_group_name
from . import property_widget,constants,io_messages
from PySide6.QtCore import QPoint,Qt,QCoreApplication
from PySide6.QtWidgets import QMenu,QTreeWidget,QAbstractItemView

def init(self):

    def init_tree(tree:CustomTree):
        #Design Tree
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

    def connect_items (self):
        self.tree.itemClicked.connect(self.treeObjectClicked)
        self.tree.itemDoubleClicked.connect(self.object_double_clicked)
        self.tree.customContextMenuRequested.connect(self.right_click)
        self.ui.button_objects_add.clicked.connect(self.addObject)
        self.ui.button_objects_delete.clicked.connect(self.deleteObject)
        self.ui.button_objects_update.clicked.connect(self.updateObject)

    self.tree = CustomTree(self.ui.verticalLayout_main)
    init_tree(self.tree)
    connect_items(self)
    self.ui.verticalLayout_objects.addWidget(self.tree)
    self.object_buttons = [self.ui.button_objects_update, self.ui.button_objects_delete, self.ui.button_objects_add]
    self.obj_line_edit_list = [self.ui.lineEdit_object_name,
                               self.ui.lineEdit_ident_value,
                               self.ui.lineEdit_ident_attribute,
                               self.ui.lineEdit_ident_pSet, ]

def clear_object_input(mainWindow):
    for el in mainWindow.obj_line_edit_list:
        el.clear()

def clear_all(mainWindow):

    #Clean Widget
    clear_object_input(mainWindow)
    mainWindow.tree.clear()

    #Delete Attributes & Objects
    for object in Object.iter.values():
        for attribute in object.attributes:
            attribute.delete()
    Object.iter = dict()

def right_click(mainWindow, position:QPoint):

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

def rc_collapse(tree:QTreeWidget):
    for item in tree.selectedItems():
        tree.collapseItem(item)

def rc_expand(tree:QTreeWidget):
    for item in tree.selectedIndexes():
        tree.expandRecursively(item)

def rc_group_items(mainWindow):

    def get_level(item):
        if item is not None:
            counter = 0
            while item.parent():
                counter += 1
                item = item.parent()
        else:
            return -1

        return counter

    group_name = req_group_name(mainWindow)

    if group_name:                                      #i guess there is a better solution TODO: find one
        root = mainWindow.tree.invisibleRootItem()
        selected_items = mainWindow.tree.selectedItems()

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
            parent_merker = [-1, None]

        if parent_merker[0] < 0:
            parent_merker = [0, mainWindow.tree.invisibleRootItem()]

        parent = parent_merker[1]

        child_list = list()

        for item in mainWindow.tree.selectedItems():
            if not item.parent() in mainWindow.tree.selectedItems():
                (item.parent() or root).removeChild(item)
                child_list.append(item)

        group = CustomTreeItem(parent, Group(group_name))
        group.setText(0, group_name)
        parent.addChild(group)
        for item in child_list:
            group.addChild(item)

        if isinstance(parent, CustomTreeItem):
            group.object.parent = parent.object

def double_click(mainWindow,item:CustomTreeItem):

    obj: Object = item.object
    mainWindow.active_object = obj
    property_widget.fill_table(mainWindow,item,obj)

def setIdentLineEnable(mainWindow, value: bool):
    mainWindow.ui.lineEdit_ident_pSet.setEnabled(value)
    mainWindow.ui.lineEdit_ident_attribute.setEnabled(value)
    mainWindow.ui.lineEdit_ident_value.setEnabled(value)

    mainWindow.ui.lineEdit_ident_pSet.setText(" ")
    mainWindow.ui.lineEdit_ident_attribute.setText(" ")
    mainWindow.ui.lineEdit_ident_value.setText(" ")
    mainWindow.ui.label_Ident.setVisible(value)

def single_click(mainWindow):
    def all_equal(iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == x for x in iterator)

    items = mainWindow.tree.selectedItems()
    mainWindow.set_pset_window_enable(False)

    group_selected = [item.object.name for item in items if isinstance(item.object, Group)]
    if group_selected:
        if all_equal(group_selected):
            mainWindow.ui.lineEdit_object_name.setText(group_selected[0])
        mainWindow.setIdentLineEnable(False)


    else:
        mainWindow.setIdentLineEnable(True)
        object_names = [item.object.name for item in items]
        ident_psets = [item.object.identifier.propertySet.name for item in items]
        ident_attributes = [item.object.identifier.name for item in items]
        ident_values = [item.object.identifier.value[0] for item in items]

        line_assignment = {
            mainWindow.ui.lineEdit_object_name: object_names,
            mainWindow.ui.lineEdit_ident_pSet: ident_psets,
            mainWindow.ui.lineEdit_ident_attribute: ident_attributes,
            mainWindow.ui.lineEdit_ident_value: ident_values,
        }

        for key, item in line_assignment.items():

            if all_equal(item):
                key.setText(item[0])
            else:
                key.setText("*")

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
    item.setText(1, identifier_tree_text(obj))
    return item

def deleteObject(mainWindow):

    root = mainWindow.tree.invisibleRootItem()
    for item in mainWindow.tree.selectedItems():
        obj = item.object

        obj.delete()
        (item.parent() or root).removeChild(item)

def updateObject(mainWindow):
    name = mainWindow.ui.lineEdit_object_name.text()
    pSetName = mainWindow.ui.lineEdit_ident_pSet.text()
    identName = mainWindow.ui.lineEdit_ident_attribute.text()
    identValue = [mainWindow.ui.lineEdit_ident_value.text()]

    input_list = [name, pSetName, identName, identValue]
    selected_items = mainWindow.tree.selectedItems()

    for item in selected_items:
        if isinstance(item.object,Group):
            obj:Group = item.object
            obj.name = name
            item.setText(0,name)
            return
        else:
            empty_input = False

            for el in input_list:
                if not bool(el):
                    empty_input = True

            if empty_input:
                io_messages.msg_missing_input(mainWindow.icon)
            else:
                for item in selected_items:
                    object: Object = item.object
                    ident = object.identifier

                    if name != "*":
                        object.name = name
                    if pSetName != ident.propertySet.name and pSetName != "*":
                        ident.propertySet = PropertySet(pSetName)

                    if identName != "*":
                        ident.name = identName

                    if identValue != "*":
                        ident.value = identValue

                    item.setText(0, object.name)
                    item.setText(1, f"{ident.propertySet.name} : {ident.name} = {ident.value[0]}")












