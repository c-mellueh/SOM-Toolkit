import som_gui.core.tool
import SOMcreator
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt
from som_gui.module.project.constants import CLASS_REFERENCE
import som_gui

class Objects(som_gui.core.tool.Object):
    @classmethod
    def update_check_state(cls, item: QTreeWidgetItem):
        obj: SOMcreator.Object = item.data(0, CLASS_REFERENCE)
        obj.optional = True if item.checkState(3) == Qt.CheckState.Checked else False

    @classmethod
    def get_object_tree(cls):
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
        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)

    @classmethod
    def fill_object_tree(cls, objects: set[SOMcreator.Object], parent_item: QTreeWidgetItem) -> None:
        old_objects_dict = {parent_item.child(i).data(0, CLASS_REFERENCE): i for i in range(parent_item.childCount())}
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
            obj: SOMcreator.Object = item.data(0, CLASS_REFERENCE)
            cls.update_item(item, obj)
            cls.fill_object_tree(obj.children, item)
