from __future__ import annotations
import som_gui.core.tool
from som_gui import tool
from som_gui.module.modelcheck import ui, trigger
from som_gui.module.project.constants import CLASS_REFERENCE
import SOMcreator
from typing import TYPE_CHECKING
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter, QLayout, QWidget, QTreeView
from PySide6.QtGui import QStandardItem, QStandardItemModel

if TYPE_CHECKING:
    from som_gui.module.modelcheck.prop import ModelcheckProperties


class Modelcheck(som_gui.core.tool.Modelcheck):
    @classmethod
    def set_selected_object(cls, obj: SOMcreator.Object):
        prop = cls.get_properties()
        prop.selected_object = obj

    @classmethod
    def get_selected_object(cls) -> SOMcreator.Object | None:
        return cls.get_properties().selected_object

    @classmethod
    def get_object_tree(cls):
        prop = cls.get_properties()
        return prop.checkbox_widget.widget.object_tree

    @classmethod
    def get_object_checkstate_dict(cls):
        prop = cls.get_properties()
        if not prop.check_state_dict:
            prop.check_state_dict = {o: True for o in tool.Object.get_all_objects()}
        return prop.check_state_dict

    @classmethod
    def get_object_check_state(cls, obj: SOMcreator.Object) -> Qt.CheckState:
        cd = cls.get_object_checkstate_dict()
        if cd.get(obj) is None:
            cd[obj] = True
        check_state = Qt.CheckState.Checked if cd[obj] else Qt.CheckState.Unchecked
        return check_state

    @classmethod
    def set_object_check_state(cls, obj: SOMcreator.Object, cs: Qt.CheckState) -> None:
        print(f"set Object_check-state: {cs}")
        cs = True if cs == Qt.CheckState.Checked else False
        cd = cls.get_object_checkstate_dict()
        cd[obj] = cs

    @classmethod
    def get_properties(cls) -> ModelcheckProperties:
        return som_gui.ModelcheckProperties

    @classmethod
    def create_checkbox_widget(cls):
        prop = cls.get_properties()
        prop.checkbox_widget = ui.ObjectCheckWidget()
        return prop.checkbox_widget

    @classmethod
    def create_window(cls):
        prop = cls.get_properties()
        prop.active_window = ui.ModelcheckWindow()
        return prop.active_window

    @classmethod
    def connect_window(cls, window: ui.ModelcheckWindow):
        trigger.connect_window(window)

    @classmethod
    def add_splitter(cls, layout: QLayout, orientation: Qt.Orientation, widget_1: QWidget, widget_2: QWidget):
        splitter = QSplitter(orientation)
        layout.addWidget(splitter)
        splitter.addWidget(widget_1)
        splitter.addWidget(widget_2)

    @classmethod
    def create_object_tree_row(cls, obj: SOMcreator.Object):
        item_list = [QStandardItem(obj.name), QStandardItem(obj.ident_value)]
        item_list[0].setFlags(item_list[0].flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable)
        item_list[0].setCheckable(True)
        item_list[0].setCheckState(Qt.CheckState.Checked)
        [i.setData(obj, CLASS_REFERENCE) for i in item_list]
        return item_list

    @classmethod
    def update_object_tree_row(cls, parent_item: QStandardItem, row_index):
        items = [parent_item.child(row_index, col) for col in range(parent_item.columnCount())]
        obj = items[0].data(CLASS_REFERENCE)
        texts = [obj.name, obj.ident_value]

        for column, text in enumerate(texts):
            if items[column].text() != text:
                items[column].setText(text)

        cs = cls.get_object_check_state(items[0].data(CLASS_REFERENCE))
        if items[0].checkState() != cs:
            items[0].setCheckState(cs)

        enabled = True if parent_item.isEnabled() and parent_item.checkState() == Qt.CheckState.Checked else False
        if parent_item == parent_item.model().invisibleRootItem():
            enabled = True

        for item in items:
            item.setEnabled(enabled)
        return items[0], obj

    @classmethod
    def fill_object_tree(cls, entities: set[SOMcreator.Object], parent_item: QStandardItem, model: QStandardItemModel,
                         tree: QTreeView):
        existing_entities_dict = {parent_item.child(index, 0).data(CLASS_REFERENCE): index for index in
                                  range(parent_item.rowCount())}

        old_entities = set(existing_entities_dict.keys())
        new_entities = entities.difference(old_entities)
        delete_entities = old_entities.difference(entities)
        for entity in reversed(sorted(delete_entities, key=lambda o: existing_entities_dict[o])):
            row_index = existing_entities_dict[entity]
            parent_item.removeRow(row_index)

        for new_entity in sorted(new_entities, key=lambda x: x.name):
            row = cls.create_object_tree_row(new_entity)
            parent_item.appendRow(row)

        for child_row in range(parent_item.rowCount()):
            class_item, obj = cls.update_object_tree_row(parent_item, child_row)
            if tree.isExpanded(parent_item.index()) or parent_item == model.invisibleRootItem():
                cls.fill_object_tree(obj.get_all_children(), class_item, model, tree)

    @classmethod
    def create_pset_tree_row(cls, entity: SOMcreator.PropertySet | SOMcreator.Attribute, parent_item: QStandardItem):
        item = QStandardItem(entity.name)
        item.setData(entity, CLASS_REFERENCE)
        item.setCheckable(True)
        item.setCheckState(Qt.CheckState.Checked)
        parent_item.appendRow(item)
        if not isinstance(entity, SOMcreator.PropertySet):
            return
        for attribute in entity.attributes:
            cls.create_pset_tree_row(attribute, item)

    @classmethod
    def fill_pset_tree(cls, property_sets: set[SOMcreator.PropertySet], tree: QTreeView):
        root_item: QStandardItem = tree.model().invisibleRootItem()
        existing_psets_dict = {root_item.child(row, 0).data(CLASS_REFERENCE): row for row in
                               range(root_item.rowCount())}
        old_psets = set(existing_psets_dict.keys())
        new_psets = property_sets.difference(old_psets)
        delete_entities = old_psets.difference(property_sets)

        for entity in reversed(sorted(delete_entities, key=lambda o: existing_psets_dict[o])):
            row_index = existing_psets_dict[entity]
            root_item.removeRow(row_index)

        for new_entity in sorted(new_psets, key=lambda x: x.name):
            row = cls.create_pset_tree_row(new_entity, root_item)
            root_item.appendRow(row)
