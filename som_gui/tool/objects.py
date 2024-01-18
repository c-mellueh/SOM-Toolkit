from __future__ import annotations
import som_gui.core.tool
import SOMcreator
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget
from PySide6.QtCore import Qt
from som_gui.module.project.constants import CLASS_REFERENCE
import som_gui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.objects.prop import ObjectProperties
    from som_gui.main_window import MainWindow


class Objects(som_gui.core.tool.Object):
    @classmethod
    def get_selected_items(cls) -> list[QTreeWidgetItem]:
        widget = cls.get_object_tree()
        return widget.selectedItems()

    @classmethod
    def get_object_from_item(cls, item: QTreeWidgetItem):
        return item.data(0, CLASS_REFERENCE)

    @classmethod
    def _fill_object_entry(cls, obj: SOMcreator.Object):
        window: MainWindow = som_gui.MainUi.window
        window.ui.line_edit_object_name.setText(obj.name)
        window.ui.line_edit_abbreviation.setText(obj.abbreviation)
        if obj.ident_attrib:
            window.ui.lineEdit_ident_value.setText(obj.ident_value)
            window.ui.lineEdit_ident_attribute.setText(obj.ident_attrib.name)
            window.ui.lineEdit_ident_pSet.setText(obj.ident_attrib.property_set.name)

    @classmethod
    def set_active_object(cls, obj: SOMcreator.Object):
        prop: ObjectProperties = som_gui.ObjectProperties
        prop.active_object = obj
        cls._fill_object_entry(obj)


    @classmethod
    def update_check_state(cls, item: QTreeWidgetItem):
        obj: SOMcreator.Object = cls.get_object_from_item(item)
        obj.optional = True if item.checkState(3) == Qt.CheckState.Checked else False

    @classmethod
    def get_object_tree(cls) -> QTreeWidget:
        return som_gui.MainUi.ui.tree_object

    @classmethod
    def create_item(cls, obj: SOMcreator.Object):
        item = QTreeWidgetItem()
        item.setData(0, CLASS_REFERENCE, obj)
        return item

    @classmethod
    def update_item(cls, item: QTreeWidgetItem, obj: SOMcreator.Object):
        item.setText(0, obj.name)
        item.setText(1, obj.ident_value)
        item.setText(2, obj.abbreviation)
        cs = Qt.CheckState.Checked if obj.optional else Qt.CheckState.Unchecked
        item.setCheckState(3, cs)
        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

    @classmethod
    def fill_object_tree(cls, objects: set[SOMcreator.Object], parent_item: QTreeWidgetItem) -> None:
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
