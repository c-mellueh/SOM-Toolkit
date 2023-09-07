from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

import SOMcreator
from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent,QStandardItemModel,QStandardItem,QFont
from PySide6.QtWidgets import QWidget, QTreeWidgetItem,QTreeWidget,QTreeView
from SOMcreator import classes
from ..data.constants import PROJECT_PHASE_COUNT

from .. import icons
from ..qt_designs import ui_project_phase_window

if TYPE_CHECKING:
    from ..main_window import MainWindow



def resize_tree_view(tree:QTreeView):
    columns = tree.model().columnCount()
    for index in range(columns):
        tree.resizeColumnToContents(index)

def resize_tree(tree:QTreeWidget):
    for index in range(tree.columnCount()):
        tree.resizeColumnToContents(index)

class PropertySetModel(QStandardItemModel):
    def __init__(self,project:SOMcreator.Project):
        super(PropertySetModel, self).__init__()
        self.project = project

    def clear(self) -> None:
        super(PropertySetModel, self).clear()
        texte = list(self.project.project_phases)
        self.setHorizontalHeaderLabels(["PropertySet, Attribut"] + texte)


class ObjectItem(QTreeWidgetItem):
    def __init__(self,data:classes.Object|classes.PropertySet|classes.Attribute):
        self.object = data
        super(ObjectItem, self).__init__()
        self.setText(0, self.object.name)
        self.setText(1, self.object.ident_value)
        for index,project_phase_name in enumerate(self.object.project.project_phases, start=2):
            value = self.object.project_phase_state(project_phase_name)
            check_state = Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
            self.setCheckState(index,check_state)

class CheckBoxItem(QStandardItem):
  def __init__(self, is_checked:bool, is_enabled:bool):
    super(CheckBoxItem, self).__init__()
    check_state = Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked
    self.setCheckState(check_state)
    self.setCheckable(True)
    self.setEnabled(is_enabled)

class AttributeItem(QStandardItem):
  def __init__(self,attribute:classes.Attribute):
    super(AttributeItem, self).__init__()
    self.attribute = attribute
    self.setText(attribute.name)
    self.setEditable(False)

class PropertySetItem(QStandardItem):
  def __init__(self,property_set:classes.PropertySet):
    super(PropertySetItem, self).__init__()
    font = QFont()
    font.setBold(True)
    self.setFont(font)
    self.property_set = property_set
    self.setEditable(False)
    self.setText(property_set.name)

def checkstate_to_bool(check_state:Qt.CheckState) -> bool:
    return True if check_state == Qt.CheckState.Checked else False

class ProjectPhaseWindow(QWidget):
    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            obj_tree = self.widget.object_tree
            pset_tree = self.widget.property_set_tree
            obj_tree.itemExpanded.connect(lambda: resize_tree(obj_tree))
            obj_tree.itemSelectionChanged.connect(self.object_selection_changed)
            pset_tree.expanded.connect(lambda :resize_tree_view(pset_tree))
            self.tree_model.itemChanged.connect(self.modify_data_model)
            obj_tree.itemChanged.connect(self.modify_data_model)
            self.widget.buttonBox.accepted.connect(self.accepted)
        super().__init__()
        self.widget = ui_project_phase_window.Ui_Form()
        self.widget.setupUi(self)
        self.tree_model = PropertySetModel(main_window.project)
        self.widget.property_set_tree.setModel(self.tree_model)
        self.setWindowIcon(icons.get_icon())
        self.main_window = main_window
        connect()
        self.data_model:dict[classes.Object|classes.PropertySet|classes.Attribute,dict[str,bool]] = dict()
        self.set_object_tree_header()

    @property
    def _project_phases(self) -> list[str]:
        return self.main_window.project.project_phases

    def set_object_tree_header(self):
        project_phases = list(self.main_window.project.project_phases)
        tree_widget = self.widget.object_tree
        tree_widget.setColumnCount(len(project_phases)+2)
        header_text = ["Objekt","Identifier"]
        header_text += list(project_phases)
        for index,text in enumerate(header_text):
            tree_widget.headerItem().setText(index,text)

    def modify_data_model(self,tree_item:CheckBoxItem|ObjectItem):
        def modify_object_data(obj_item:ObjectItem):
            obj = obj_item.object
            check_state_dict = dict()
            for column_index in range(2, 2 + len(self._project_phases)):
                header_text = self.widget.object_tree.headerItem().text(column_index)
                check_state_dict[header_text] = checkstate_to_bool(obj_item.checkState(column_index))
            self.data_model[obj] = check_state_dict
            self.fill_property_set_tree(obj)

        def modify_checkbox_data(check_box_item:CheckBoxItem):
            model_index = check_box_item.index()
            column = model_index.column()
            new_checkstate = True if check_box_item.checkState() == Qt.CheckState.Checked else False
            data_index = model_index.siblingAtColumn(0)
            data_item = self.tree_model.itemFromIndex(data_index)
            header_text = self.tree_model.horizontalHeaderItem(column).text()
            if isinstance(data_item,PropertySetItem):
                data = data_item.property_set
            elif isinstance(data_item,AttributeItem):
                data = data_item.attribute
            else:
                raise TypeError(f"Datatype {type(data_item)} doesn't match!")
            self.data_model[data][header_text] = new_checkstate

            if isinstance(data_item, PropertySetItem):
                for index in range(data_item.rowCount()):
                    data_item.child(index, column).setEnabled(new_checkstate)

        if isinstance(tree_item,ObjectItem):
            modify_object_data(tree_item)
        elif isinstance(tree_item,CheckBoxItem):
            modify_checkbox_data(tree_item)

    def show(self) -> None:
        self.widget.object_tree.clear()
        self.tree_model.clear()
        self.fill_object_tree()
        self.fill_data_model()
        self.widget.label_object.hide()
        super(ProjectPhaseWindow, self).show()

    def accepted(self):

        for item,project_phase_dict in self.data_model.items():
            for project_phase_name,value in project_phase_dict.items():
                if item.project_phase_state(project_phase_name) != value:
                    logging.info(f"{item}: Projektphase {project_phase_name} geändert")
                    item.set_project_phase_state(project_phase_name,value)
        self.hide()
        self.main_window.reload()

    def fill_data_model(self):
        def add_to_model(entity:SOMcreator.Object|SOMcreator.PropertySet|SOMcreator.Attribute) -> None:
            self.data_model[entity] = {name:entity.project_phase_state(name) for name in self._project_phases}


        self.data_model = dict()
        for obj in self.main_window.project.get_all_objects():
            add_to_model(obj)
            for pset in obj.get_all_property_sets():
                add_to_model(pset)
                for attribute in pset.get_all_attributes():
                    add_to_model(attribute)

    def resize_to_content(self) -> None:
        """resizes Tree to content so it allways looks fresh and tidy"""
        resize_tree(self.widget.object_tree)
        resize_tree_view(self.widget.property_set_tree)

    def fill_object_tree(self) -> None:
        project = self.main_window.project
        tree = self.widget.object_tree
        root = tree.invisibleRootItem()
        obj_item_dict: dict[classes.Object, ObjectItem] = dict()

        for obj in project.get_all_objects():
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

    def object_selection_changed(self):
        object_items = self.widget.object_tree.selectedItems()
        if not len(object_items):
            return
        item:ObjectItem = object_items[0]
        self.fill_property_set_tree(item.object)
        self.widget.label_object.show()
        self.widget.label_object.setText(f"{item.object.name} ({item.object.ident_value})")

    def fill_property_set_tree(self,selected_object:classes.Object):
        project_phases = self.main_window.project.project_phases

        tree = self.widget.property_set_tree
        self.tree_model.clear()
        root = self.tree_model.invisibleRootItem()
        tree.setModel(self.tree_model)
        for property_set in selected_object.get_all_property_sets():
            pset_item = PropertySetItem(property_set)
            pset_row = [pset_item]
            for index,project_phase_name in enumerate(project_phases):
                pset_is_enabled = self.data_model[selected_object][project_phase_name]
                pset_is_checked = self.data_model[property_set][project_phase_name]
                pset_row.append(CheckBoxItem(pset_is_checked,pset_is_enabled))
            root.appendRow(pset_row)
            for attribute in property_set.get_all_attributes():
                attribute_row  = [AttributeItem(attribute)]
                for index,project_phase_name in enumerate(project_phases):
                    pset_is_enabled = self.data_model[selected_object][project_phase_name]
                    attribute_is_enabled = self.data_model[property_set][project_phase_name]
                    attribute_is_checked = self.data_model[attribute][project_phase_name]
                    attribute_row.append(CheckBoxItem(attribute_is_checked,all((attribute_is_enabled,pset_is_enabled))))
                pset_item.appendRow(attribute_row)

        resize_tree_view(tree)
        tree.expandAll()