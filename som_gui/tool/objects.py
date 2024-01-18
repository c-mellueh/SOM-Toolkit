from __future__ import annotations

import logging

import som_gui.core.tool
import SOMcreator
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget, QAbstractItemView
from PySide6.QtCore import Qt, QPoint
from som_gui.module.project.constants import CLASS_REFERENCE
import som_gui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.objects.prop import ObjectProperties
    from som_gui.main_window import MainWindow


class Objects(som_gui.core.tool.Object):
    @classmethod
    def set_mouse_press(cls, is_pressed: bool):
        logging.debug(f"Set Mouse Press")
        prop: ObjectProperties = som_gui.ObjectProperties
        prop.mouse_is_pressed = is_pressed

    @classmethod
    def is_mouse_pressed(cls) -> bool:
        logging.debug(f"Mouse State Requested")

        prop: ObjectProperties = som_gui.ObjectProperties
        return prop.mouse_is_pressed

    @classmethod
    def drop_indication_pos_is_on_item(cls):
        logging.debug(f"Drop Indicator Requested")

        widget = cls.get_object_tree()
        if widget.dropIndicatorPosition() == QAbstractItemView.DropIndicatorPosition.OnItem:
            return True
        else:
            return False

    @classmethod
    def get_item_from_pos(cls, pos: QPoint):
        logging.debug(f"Item from Pos Requested")

        widget = cls.get_object_tree()
        return widget.itemFromIndex(widget.indexAt(pos))

    @classmethod
    def get_selected_items(cls) -> list[QTreeWidgetItem]:
        logging.debug(f"selected Items Requested")
        widget = cls.get_object_tree()
        return widget.selectedItems()

    @classmethod
    def get_object_from_item(cls, item: QTreeWidgetItem) -> SOMcreator.Object:
        logging.debug(f"Object from Item Requested")
        return item.object

    @classmethod
    def _fill_object_entry(cls, obj: SOMcreator.Object):
        logging.debug(f"Fill Object Entry")

        window: MainWindow = som_gui.MainUi.window
        window.ui.line_edit_object_name.setText(obj.name)
        window.ui.line_edit_abbreviation.setText(obj.abbreviation)
        if obj.ident_attrib:
            window.ui.lineEdit_ident_value.setText(obj.ident_value)
            window.ui.lineEdit_ident_attribute.setText(obj.ident_attrib.name)
            window.ui.lineEdit_ident_pSet.setText(obj.ident_attrib.property_set.name)

    @classmethod
    def set_active_object(cls, obj: SOMcreator.Object):
        logging.debug(f"Set Active Object")

        prop: ObjectProperties = som_gui.ObjectProperties
        prop.active_object = obj
        cls._fill_object_entry(obj)


    @classmethod
    def update_check_state(cls, item: QTreeWidgetItem):
        logging.debug(f"Update CheckState")

        obj: SOMcreator.Object = cls.get_object_from_item(item)
        obj.optional = True if item.checkState(3) == Qt.CheckState.Checked else False

    @classmethod
    def get_object_tree(cls) -> QTreeWidget:
        logging.debug(f"ObjectTree Requested")

        return som_gui.MainUi.ui.tree_object

    @classmethod
    def create_item(cls, obj: SOMcreator.Object):
        logging.debug(f"CreateItem")

        item = QTreeWidgetItem()
        item.object = obj  # item.setData(0,obj) leads to recursion bug so allocating directly
        item.setText(0, obj.name)
        return item

    @classmethod
    def update_item(cls, item: QTreeWidgetItem, obj: SOMcreator.Object):
        logging.debug(f"Update Item {obj}")

        item.setText(0, obj.name)
        item.setText(1, obj.ident_value)
        item.setText(2, obj.abbreviation)
        cs = Qt.CheckState.Checked if obj.optional else Qt.CheckState.Unchecked
        item.setCheckState(3, cs)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable)

    @classmethod
    def fill_object_tree(cls, objects: set[SOMcreator.Object], parent_item: QTreeWidgetItem) -> None:
        logging.debug(f"Fill Object Tree {parent_item}")
        old_objects_dict = {cls.get_object_from_item(parent_item.child(i)): i for i in range(parent_item.childCount())}
        old_objects = set(old_objects_dict.keys())
        new_objects = objects.difference(old_objects)
        delete_objects = old_objects.difference(objects)

        for obj in reversed(sorted(delete_objects, key=lambda o: old_objects_dict[o])):
            row_index = old_objects_dict[obj]
            parent_item.removeChild(parent_item.child(row_index))

        for new_object in sorted(new_objects, key=lambda o: o.name):
            item = cls.create_item(new_object)
            parent_item.addChild(item)

        for index in range(parent_item.childCount()):
            item = parent_item.child(index)
            obj: SOMcreator.Object = cls.get_object_from_item(item)
            cls.update_item(item, obj)
            cls.fill_object_tree(obj.children, item)
