from PySide6.QtCore import QPoint, Qt, QCoreApplication
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QMenu, QTreeWidget, QAbstractItemView, QTreeWidgetItem

from desiteRuleCreator.QtDesigns import ui_mainwindow
from desiteRuleCreator.Widgets import script_widget, property_widget
from desiteRuleCreator.Windows import popups
from desiteRuleCreator.data import classes, constants


def init(main_window):
    def init_tree(tree: classes.CustomTree):
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
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Identifier", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Objects", None))

    def connect_items(main_window):
        main_window.ui.tree.itemClicked.connect(main_window.object_clicked)
        main_window.ui.tree.itemDoubleClicked.connect(main_window.object_double_clicked)
        main_window.ui.tree.customContextMenuRequested.connect(main_window.right_click)
        main_window.ui.button_objects_add.clicked.connect(main_window.add_object)
        main_window.ui.button_objects_update.clicked.connect(main_window.update_object)
        main_window.grpSc.activated.connect(main_window.rc_group)
        main_window.delSc.activated.connect(main_window.delete_object)

    main_window.ui.verticalLayout_objects.removeWidget(main_window.ui.tree)
    main_window.ui.tree.close()
    main_window.ui.tree = classes.CustomTree(main_window.ui.verticalLayout_main)
    main_window.ui.verticalLayout_objects.addWidget(main_window.ui.tree)
    init_tree(main_window.ui.tree)

    main_window.ui.verticalLayout_objects.addWidget(main_window.ui.tree)
    main_window.object_buttons = [main_window.ui.button_objects_update,
                                  main_window.ui.button_objects_add]
    main_window.obj_line_edit_list = [main_window.ui.lineEdit_object_name,
                                      main_window.ui.lineEdit_ident_value,
                                      main_window.ui.lineEdit_ident_attribute,
                                      main_window.ui.lineEdit_ident_pSet, ]
    main_window.delSc = QShortcut(QKeySequence('Ctrl+X'), main_window)
    main_window.grpSc = QShortcut(QKeySequence('Ctrl+G'), main_window)
    connect_items(main_window)


def selected_object(main_window):
    tree: classes.CustomTree = main_window.ui.tree
    sel_items = tree.selectedItems()
    if len(sel_items) == 1:
        return sel_items[0]
    else:
        return None


def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)


def clear_object_input(main_window):
    for el in main_window.obj_line_edit_list:
        el.clear()


def clear_all(main_window):
    # Clean Widget
    clear_object_input(main_window)
    main_window.ui.tree.clear()

    # Delete Attributes & Objects
    for obj in classes.Object.iter:
        for property_set in obj.property_sets:
            property_set.delete()
    classes.Object.iter = list()


def right_click(main_window, position: QPoint):
    menu = QMenu()
    main_window.action_group_objects = menu.addAction("Group")
    main_window.action_delete_attribute = menu.addAction("Delete")
    main_window.action_expand_selection = menu.addAction("Expand")
    main_window.action_collapse_selection = menu.addAction("Collapse")

    main_window.action_delete_attribute.triggered.connect(main_window.delete_object)
    main_window.action_group_objects.triggered.connect(main_window.rc_group)
    main_window.action_expand_selection.triggered.connect(main_window.rc_expand)
    main_window.action_collapse_selection.triggered.connect(main_window.rc_collapse)
    menu.exec(main_window.ui.tree.viewport().mapToGlobal(position))


def rc_collapse(tree: QTreeWidget):
    for item in tree.selectedItems():
        tree.collapseItem(item)


def rc_expand(tree: QTreeWidget):
    for item in tree.selectedIndexes():
        tree.expandRecursively(item)


def rc_group_items(main_window):
    [group_name, ident_pset, ident_attrib, ident_value] = popups.req_group_name(main_window)
    if group_name:
        selected_items = main_window.ui.tree.selectedItems()
        parent_classes = [item for item in selected_items if item.parent() not in selected_items]
        parent = parent_classes[0].parent()

        if parent is None:
            parent: QTreeWidgetItem = main_window.ui.tree.invisibleRootItem()

        pset = classes.PropertySet(ident_pset)
        identifier = classes.Attribute(pset, ident_attrib, [ident_value], constants.LIST)
        group_obj = classes.Object(group_name, identifier)
        group_obj.add_property_set(pset)
        group_item: classes.CustomTreeItem = main_window.add_object_to_tree(group_obj, parent)

        for item in parent_classes:
            child: classes.CustomTreeItem = parent.takeChild(parent.indexOfChild(item))
            group_obj.add_child(child.object)

            group_item.addChild(child)


def double_click(main_window, item: classes.CustomTreeItem):
    obj: classes.Object = item.object
    main_window.active_object = obj
    property_widget.fill_table(main_window, obj)
    script_widget.show(main_window)
    main_window.update_completer()


def set_ident_line_enable(main_window, value: bool):
    main_window.ui.lineEdit_ident_pSet.setEnabled(value)
    main_window.ui.lineEdit_ident_attribute.setEnabled(value)
    main_window.ui.lineEdit_ident_value.setEnabled(value)

    main_window.ui.lineEdit_ident_pSet.setText(" ")
    main_window.ui.lineEdit_ident_attribute.setText(" ")
    main_window.ui.lineEdit_ident_value.setText(" ")
    main_window.ui.label_Ident.setVisible(value)


def single_click(main_window):
    main_window.set_right_window_enable(False)

    items = main_window.ui.tree.selectedItems()

    is_concept = [item.object for item in items if item.object.is_concept]
    if is_concept:
        main_window.clear_object_input()
        if all_equal(is_concept):
            main_window.ui.lineEdit_object_name.setText(is_concept[0].name)

    else:

        main_window.set_ident_line_enable(True)
        object_names = [item.object.name for item in items]
        ident_psets = [item.object.ident_attrib.property_set.name for item in items if isinstance(item.object.ident_attrib,classes.Attribute)]
        ident_attributes = [item.object.ident_attrib.name for item in items]
        ident_values = [item.object.ident_attrib.value for item in items]

        line_assignment = {
            main_window.ui.lineEdit_object_name: object_names,
            main_window.ui.lineEdit_ident_pSet: ident_psets,
            main_window.ui.lineEdit_ident_attribute: ident_attributes,
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
        main_window.ui.lineEdit_ident_value.setText(text)


def add_object(main_window):
    def missing_input(input_list):
        for el in input_list:
            if el == "" or el is None:
                return True
        return False

    def already_exists(ident):
        for obj in classes.Object.iter:
            if obj.ident_attrib == str(ident):
                return True
            else:
                if obj.ident_attrib.is_equal(ident):
                    return True
        return False

    def create_ident(property_set, ident_name, ident_value) -> classes.Attribute:
        ident: classes.Attribute = property_set.get_attribute(ident_name)
        if ident is None:
            ident = classes.Attribute(property_set, ident_name, ident_value, constants.LIST)
        else:
            ident.value = ident_value  #

        return ident

    name = main_window.ui.lineEdit_object_name.text()
    p_set_name = main_window.ui.lineEdit_ident_pSet.text()
    ident_name = main_window.ui.lineEdit_ident_attribute.text()
    ident_value = [main_window.ui.lineEdit_ident_value.text()]

    input_list = [name, p_set_name, ident_name, ident_value]

    parent = None
    if p_set_name in property_widget.predefined_pset_list():  # if PropertySet allready predefined
        result = popups.req_merge_pset()  # ask if you want to merge
        if result:
            parent = property_widget.get_parent_by_name(main_window.active_object, p_set_name)
        elif result is None:
            return

    property_set = classes.PropertySet(p_set_name)
    if parent is not None:
        parent.add_child(property_set)

    if not missing_input(input_list):
        if "*" not in input_list:
            ident = create_ident(property_set, ident_name, ident_value)
            if not already_exists(ident):

                obj = classes.Object(name, ident)
                obj.add_property_set(ident.property_set)
                main_window.add_object_to_tree(obj)
                main_window.clear_object_input()

            else:
                ident.delete()
                popups.msg_already_exists()

        else:
            popups.msg_missing_input()

    else:
        popups.msg_missing_input()


def add_object_to_tree(main_window, obj: classes.Object, parent=None):
    if parent is None:
        item = classes.CustomTreeItem(main_window.ui.tree, obj)

    else:
        item = classes.CustomTreeItem(parent, obj)

    item.setText(0, obj.name)
    if not obj.is_concept:
        item.setText(1, str(obj.ident_attrib))
    return item


def delete_object(main_window):
    string_list = [item.object.name for item in main_window.ui.tree.selectedItems()]


    delete_request = popups.msg_del_items(string_list)

    if delete_request:

        root: QTreeWidgetItem = main_window.ui.tree.invisibleRootItem()
        for item in main_window.ui.tree.selectedItems():
            obj: classes.Object = item.object
            obj.delete()
            children = item.takeChildren()
            root.addChildren(children)
            (item.parent() or root).removeChild(item)
            main_window.project.changed = True


def update_object(main_window):
    name = main_window.ui.lineEdit_object_name.text()
    p_set_name = main_window.ui.lineEdit_ident_pSet.text()
    ident_name = main_window.ui.lineEdit_ident_attribute.text()
    ident_value = main_window.ui.lineEdit_ident_value.text()

    input_list = [name, p_set_name, ident_name, ident_value]

    selected_items = main_window.ui.tree.selectedItems()

    if len(selected_items) > 1 and  "*" not in input_list:
        popups.msg_identical_identifier()
        return
    empty_input = False
    for el in input_list:
        if not bool(el):
            empty_input = True

    if empty_input:
        popups.msg_missing_input()
        return

    else:
        for item in selected_items:
            obj: classes.Object = item.object
            ident = obj.ident_attrib
            if not isinstance(ident, classes.Attribute):
                property_set = classes.PropertySet(p_set_name)
                obj.ident_attrib = classes.Attribute(property_set, ident_name, [ident_value],
                                                        value_type=constants.LIST)
            else:
                if name != "*":
                    obj.name = name
                if p_set_name != "*":
                    ident.property_set = classes.PropertySet(p_set_name)

                if ident_name != "*":
                    ident.name = ident_name

                if ident_value != "*":
                    ident.value = [ident_value]

            item.setText(0, obj.name)
            item.setText(1, str(obj.ident_attrib))


def reload_tree(main_window):
    def loop(item: classes.CustomTreeItem):
        for i in range(item.childCount()):
            child = item.child(i)
            child.update()
            loop(child)

    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    root = ui.tree.invisibleRootItem()
    loop(root)
