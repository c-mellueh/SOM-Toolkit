from __future__ import annotations

import re
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget, QTreeWidgetItem,QTreeWidget
from SOMcreator import classes
from ..data.constants import PROJECT_PHASE_COUNT

from .. import icons
from ..qt_designs import ui_project_phase_window
from ..windows import popups

if TYPE_CHECKING:
    from ..main_window import MainWindow
def resize_tree(tree:QTreeWidget):
    for index in range(tree.columnCount()):
        tree.resizeColumnToContents(index)

class ObjectItem(QTreeWidgetItem):
    def __init__(self,data:classes.Object|classes.PropertySet|classes.Attribute):
        self.item_data = data
        super(ObjectItem, self).__init__()
        self.setText(0, self.item_data.name)
        self.setText(1, self.item_data.ident_value)
        for index,value in enumerate(self.item_data.project_phases, start=2):
            check_state = Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
            self.setCheckState(index,check_state)

class DataItem(QTreeWidgetItem):
    def __init__(self,data:classes.Object|classes.PropertySet|classes.Attribute):
        self.item_data = data
        super(DataItem, self).__init__()
        self.setText(0,self.item_data.name)
        for index,value in enumerate(self.item_data.project_phases,start=1):
            check_state = Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
            self.setCheckState(index,check_state)

def checkstate_to_bool(check_state:Qt.CheckState) -> bool:
    return True if check_state == Qt.CheckState.Checked else False

class ProjectPhaseWindow(QWidget):
    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            obj_tree = self.widget.object_tree
            pset_tree = self.widget.property_set_tree
            obj_tree.itemExpanded.connect(lambda: resize_tree(obj_tree))
            obj_tree.itemClicked.connect(lambda item: self.fill_property_set_tree(item.item_data))
            pset_tree.itemExpanded.connect(lambda :resize_tree(pset_tree))
            pset_tree.itemChanged.connect(self.modify_data_model)
            obj_tree.itemChanged.connect(self.modify_data_model)
            self.widget.buttonBox.accepted.connect(self.accepted)

        super().__init__()
        self.widget = ui_project_phase_window.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.main_window = main_window
        connect()
        self.data_model:dict[classes.Object|classes.PropertySet|classes.Attribute,list[bool]] = dict()

    def modify_data_model(self,data_item:DataItem|ObjectItem):
        item:classes.Object|classes.PropertySet|classes.Attribute = data_item.item_data

        start_index = 1
        if isinstance(data_item,ObjectItem):
            start_index = 2 #factor in identifier column

        state_list = list()
        for index in range(start_index,start_index+PROJECT_PHASE_COUNT):
            cs = checkstate_to_bool(data_item.checkState(index))
            state_list.append(cs)

        self.data_model[item] = state_list
        print(state_list)

    def show(self) -> None:
        self.widget.object_tree.clear()
        self.widget.property_set_tree.clear()
        self.fill_object_tree()
        self.fill_data_model()
        super(ProjectPhaseWindow, self).show()

    def accepted(self):
        for item,project_phase_list in self.data_model.items():
            item.project_phases = project_phase_list
        self.hide()

    def fill_data_model(self):
        self.data_model = dict()
        for obj in self.main_window.project.objects:
            self.data_model[obj] = obj.project_phases
            for pset in obj.property_sets:
                self.data_model[pset] = pset.project_phases
                for attribute in pset.attributes:
                    self.data_model[attribute] = attribute.project_phases

    def resize_to_content(self) -> None:
        """resizes Tree to content so it allways looks fresh and tidy"""
        resize_tree(self.widget.object_tree)
        resize_tree(self.widget.property_set_tree)


    def fill_object_tree(self) -> None:
        project = self.main_window.project
        tree = self.widget.object_tree
        root = tree.invisibleRootItem()
        obj_item_dict: dict[classes.Object, ObjectItem] = dict()

        for obj in project.objects:
            obj_item = ObjectItem(obj)
            obj_item_dict[obj] = obj_item
            root.addChild(obj_item)

        for obj in project.objects:
            tree_item = obj_item_dict[obj]
            if obj.parent is not None:
                parent_item = obj_item_dict[obj.parent]
                root = tree_item.treeWidget().invisibleRootItem()
                item = root.takeChild(root.indexOfChild(tree_item))
                parent_item.addChild(item)

        resize_tree(tree)

    def fill_property_set_tree(self,selected_object:classes.Object):
        tree = self.widget.property_set_tree
        tree.clear()
        root = tree.invisibleRootItem()
        for property_set in selected_object.property_sets:
            pset_item = DataItem(property_set)
            root.addChild(pset_item)
            for attribute in property_set.attributes:
                attribute_item = DataItem(attribute)
                pset_item.addChild(attribute_item)
        resize_tree(tree)