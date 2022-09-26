from __future__ import annotations
import re
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent,QIcon
from PySide6.QtWidgets import QWidget, QListWidgetItem,QTableWidgetItem,QLineEdit

from desiteRuleCreator.QtDesigns import ui_mapping_window
from desiteRuleCreator.data import classes,constants
from desiteRuleCreator import icons
from desiteRuleCreator.Windows import popups

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from desiteRuleCreator.main_window import MainWindow

class MappingWindow(QWidget):

    def __init__(self, main_window:MainWindow) -> None:
        def connect() -> None:
            self.object_tree.itemClicked.connect(self.single_click)
            self.button_add.clicked.connect(self.add_line)
            self.button_update.clicked.connect(self.update_object)
            self.pset_tree.itemClicked.connect(self.edit_attribute)
            self.button_update_attribute.clicked.connect(self.update_attribute)
            pass

        super().__init__()

        self.widget = ui_mapping_window.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.setWindowTitle("Mapping Window")
        self.main_window = main_window
        self.object_tree = self.widget.object_tree
        self.label_name = self.widget.label_name_modifiable
        self.button_add = self.widget.button_add
        self.input_lines: set[QLineEdit] = {self.widget.line_edit_ifcmapping}
        self.first_line = self.widget.line_edit_ifcmapping
        self.button_update = self.widget.button_update
        self.pset_tree =  self.widget.pset_treewidget
        self.button_update_attribute = self.widget.button_update_attribute

        connect()
        self.active_object_item: None | classes.CustomObjectMappingTreeItem= None
        self._active_attribute_item: None|classes.CustomAttribTreeItem = None
        self.fill_object_table()

    @property
    def active_attribute_item(self) -> classes.CustomAttribTreeItem|None:
        return self._active_attribute_item

    @active_attribute_item.setter
    def active_attribute_item(self,value:classes.CustomAttribTreeItem|None) -> None:
        if value is None:
            self.widget.attribute_widget.setEnabled(False)
        else:
            self.widget.attribute_widget.setEnabled(True)
            self.button_update_attribute.setEnabled(True)
            self._active_attribute_item = value

    def fill_object_table(self) -> None:
        def recursive_fill(main_item:classes.CustomObjectTreeItem,map_item:classes.CustomObjectMappingTreeItem):
            for i in range(main_item.childCount()):
                child = main_item.child(i)
                map_child = classes.CustomObjectMappingTreeItem(child.object)
                map_item.addChild(map_child)
                recursive_fill(child,map_child)

        object:classes.Object

        main_root_item = self.main_window.ui.tree.invisibleRootItem()
        map_root_item = self.object_tree.invisibleRootItem()
        for i in range(map_root_item.childCount()):
            map_root_item.removeChild(main_root_item.child(i))
        recursive_fill(main_root_item,map_root_item)

    def fill_pset_table(self) -> None:
        self.pset_tree.clear()
        obj = self.active_object_item.object
        root_item = self.pset_tree.invisibleRootItem()
        for property_set in obj.property_sets:
            pset_item = classes.CustomPSetTreeItem(root_item,property_set)
            for attribute in property_set.attributes:
                attribute_item = classes.CustomAttribTreeItem(pset_item,attribute)
                attribute_item.setText(1,attribute.revit_name)

    def single_click(self,item:classes.CustomObjectMappingTreeItem) -> None:
        self.active_object_item = item
        obj = item.object
        self.remove_lines()
        self.label_name.setText(obj.name)

        for i,mapping in enumerate(obj.ifc_mapping):
            if i == 0:
                self.first_line.setText(mapping)
            else:
                line = self.add_line()
                line.setText(mapping)

        self.fill_pset_table()

    def add_line(self) -> QLineEdit:
        line_edit = QLineEdit()
        self.input_lines.add(line_edit)
        layout = self.widget.upper_layout
        rc = len(self.input_lines)
        layout.addWidget(line_edit,rc+1,0,1,3)
        return line_edit

    def remove_lines(self) -> None:
        for le in list(self.input_lines):
            if le != self.first_line:
                le.setParent(None)
                self.input_lines.remove(le)

    def update_object(self) -> None:
        obj = self.active_object_item.object
        obj.ifc_mapping = {le.text() for le in self.input_lines}
        self.active_object_item.update()

    def edit_attribute(self,item:classes.CustomAttribTreeItem) -> None:
        if not isinstance(item,classes.CustomAttribTreeItem):
            self.active_attribute_item = None
            self.widget.label_attribute_name.clear()
            self.widget.line_edit_attribute.clear()
            return
        self.widget.line_edit_attribute.setText(item.attribute.revit_name)
        self.active_attribute_item = item
        self.widget.label_attribute_name.setText(f"{item.attribute.property_set.name} : {item.attribute.name}")

    def update_attribute(self) -> None:
        attribute = self.active_attribute_item.attribute
        attribute.revit_name = self.widget.line_edit_attribute.text()
        self.active_attribute_item.setText(1,self.active_attribute_item.attribute.revit_name)
        self.widget.line_edit_attribute.clear()
        self.active_attribute_item = None
        self.widget.label_attribute_name.clear()
