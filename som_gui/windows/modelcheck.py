from __future__ import annotations

import logging
import os
from time import time, sleep
from typing import TYPE_CHECKING

import ifcopenshell
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QFileDialog, QWidget, QTreeWidgetItem,QListWidgetItem
from SOMcreator import classes,desite

from ..filehandling import export
from ..widgets import object_widget
from ..icons import get_icon
from ..qt_designs import ui_modelcheck

if TYPE_CHECKING:
    from ..main_window import MainWindow

BIMCOLLAB = "BimCollabZoom"
DESITE_TABLE = "Desite_Table"
DESITE_JS = "Desite_JS"

class DataItem(QTreeWidgetItem):
    def __init__(self,data:classes.Object):
        super(DataItem, self).__init__()
        self.setText(0,data.name)
        self.setText(1,data.ident_value)
        self.setCheckState(0,Qt.CheckState.Checked)

class ListItem(QListWidgetItem):
    def __init__(self,index,text):
        super(ListItem, self).__init__()
        self.setText(f"[{index}] {text}")
        self.setCheckState(Qt.CheckState.Checked)

class ModelcheckWindow(QWidget):


    def __init__(self, main_window: MainWindow,software_type:str):

        def connect():
            self.widget.tree_widget_objects.itemChanged.connect(self.item_checked)
            self.widget.buttonBox.accepted.connect(self.run)
        super(ModelcheckWindow, self).__init__()
        main_window.modelcheck_window = self
        self.main_window = main_window
        self.widget = ui_modelcheck.Ui_Form()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.show()
        self.software_type = software_type
        self.project = main_window.project
        object_widget.fill_tree(self.project.objects,self.widget.tree_widget_objects,DataItem)
        self.fill_table()
        connect()
        self.object_dict = dict()
        self.rule_dict = dict()


    def fill_tree(self) -> None:
        def add_object_to_tree(o):
            tree_item = DataItem(o)
            root_item.addChild(tree_item)
            #self.widget.tree_widget_objects.setItemWidget(tree_item,0,CheckBoxItem(True,True))
            return tree_item
        object_list = list(self.project.objects)
        root_item = self.widget.tree_widget_objects.invisibleRootItem()
        self.object_dict: dict[classes.Object, DataItem] = \
            {obj: add_object_to_tree(obj) for obj in
             object_list}  # add all Objects to Tree without Order
        for obj in object_list:
            tree_item = self.object_dict[obj]
            parent_is_none = obj.parent is None
            parent_in_dict = obj.parent in self.object_dict
            if not parent_is_none and parent_in_dict:
                parent_item = self.object_dict[obj.parent]
                root = tree_item.treeWidget().invisibleRootItem()
                item = root.takeChild(root.indexOfChild(tree_item))
                parent_item.addChild(item)

    def item_checked(self,item:DataItem):
        current_state = item.checkState(0)
        if current_state == Qt.CheckState.Unchecked:
            new_checkstate = Qt.CheckState.Checked
        else:
            new_checkstate = Qt.CheckState.Unchecked

        for child_index in range(item.childCount()):
            child = item.child(child_index)
            child.setCheckState(0, current_state)

    def fill_table(self):
        main_pset,main_attribute = self.get_main_attribute(self.project)
        data =  [[1, f"Propertyset '{main_pset}' fehlt"],
                [2, f"{main_pset}:{main_attribute} fehlt"],
                [3, "Bauteilklassifikation nicht in SOM vorhanden"],
                [4, "GUID ist in mehreren Dateien identisch"],
                [5, "PropertySet Fehlt"],
                [6, "Attribut Fehlt"],
                [7, "Attribut hat falschen Wert"],
                [8, "Gruppe hat falsches Subelement"],
                [9, "Zwischenebene besitzt verschiedene Klassen als Subelement"],
                [10, "Gruppe besitzt keine Subelemente"],
                [11, "Element hat keine Gruppenzuweisen"],
                [12, "Zu Viele Subelemente]"]]

        for [index,text] in data:
            self.widget.list_widget_checkrules.addItem(ListItem(index,text))

    def get_main_attribute(self,proj: classes.Project) -> (str, str):
        ident_attributes = dict()
        ident_psets = dict()
        for obj in proj.objects:
            if obj.ident_attrib is None:
                continue
            ident_pset = obj.ident_attrib.property_set.name
            ident_attribute = obj.ident_attrib.name
            if not ident_pset in ident_psets:
                ident_psets[ident_pset] = 0
            if not ident_attribute in ident_attributes:
                ident_attributes[ident_attribute] = 0
            ident_psets[ident_pset] += 1
            ident_attributes[ident_attribute] += 1

        ident_attribute = (sorted(ident_attributes.items(), key=lambda x: x[1]))
        ident_pset = (sorted(ident_psets.items(), key=lambda x: x[1]))
        if ident_attribute and ident_pset:
            return ident_pset[0][0], ident_attribute[0][0]
        else:
            return "", ""

    def run(self):
        if self.software_type == DESITE_JS:
            path = export.get_path(self.main_window, "qa.xml")
            desite.export_modelcheck()
