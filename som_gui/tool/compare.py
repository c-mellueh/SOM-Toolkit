from __future__ import annotations
from typing import TYPE_CHECKING
from som_gui import tool
import SOMcreator
from som_gui.module.compare import ui
import som_gui.core.tool
import som_gui
from PySide6.QtWidgets import QTreeWidgetItem
from som_gui.module.project.constants import CLASS_REFERENCE

if TYPE_CHECKING:
    from som_gui.module.compare.prop import CompareProperties


class Compare(som_gui.core.tool.Compare):

    @classmethod
    def get_properties(cls) -> CompareProperties:
        return som_gui.CompareProperties

    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_project(cls, index=1) -> SOMcreator.Project:
        return cls.get_properties().projects[index]

    @classmethod
    def get_uuid_dict(cls, index=1) -> dict:
        uuid_dict = cls.get_properties().uuid_dicts[index]
        project = cls.get_project(index)
        if uuid_dict is None:
            d = {hi.uuid: hi for hi in project.get_all_hirarchy_items()}
            cls.get_properties().uuid_dicts[index] = d
        return cls.get_properties().uuid_dicts[index]

    @classmethod
    def get_ident_dict(cls, index=1) -> dict:
        uuid_dict = cls.get_properties().ident_dicts[index]
        project = cls.get_project(index)
        if uuid_dict is None:
            d = {obj.ident_value: obj for obj in project.get_all_objects()}
            cls.get_properties().ident_dicts[index] = d
        return cls.get_properties().ident_dicts[index]

    @classmethod
    def find_matching_object(cls, obj: SOMcreator.Object, index=1) -> SOMcreator.Object | None:
        uuid_dict = cls.get_uuid_dict(index)
        ident_dict = cls.get_ident_dict(index)

        uuid_match = uuid_dict.get(obj.uuid)
        if uuid_match:
            return uuid_match
        ident_match = ident_dict.get(obj.ident_value)

        if ident_match:
            return ident_match

        return None

    @classmethod
    def create_object_dicts(cls):
        project_0 = cls.get_project(0)
        project_1 = cls.get_project(1)
        missing_objects_0 = list()
        missing_objects_1 = list(project_1.get_all_objects())
        object_dict0 = dict()
        object_dict1 = dict()
        for obj in project_0.get_all_objects():
            match = cls.find_matching_object(obj, 1)
            if match is not None:
                object_dict0[obj] = match
                object_dict1[match] = obj
                missing_objects_1.remove(match)
            else:
                object_dict0[obj] = None
                missing_objects_0.append(obj)
        for obj in missing_objects_1:
            object_dict1[obj] = None
        cls.get_properties().missing_objects = [missing_objects_0, missing_objects_1]
        cls.get_properties().object_dicts = [object_dict0, object_dict1]

    @classmethod
    def create_window(cls):
        cls.get_properties().window = ui.CompareDialog()
        return cls.get_window()

    @classmethod
    def get_window(cls) -> ui.CompareDialog:
        return cls.get_properties().window

    @classmethod
    def get_object_dict(cls, index=1) -> dict:
        return cls.get_properties().object_dicts[index]

    @classmethod
    def get_missing_objects(cls, index=1) -> list:
        return cls.get_properties().missing_objects[index]

    @classmethod
    def add_object_to_item(cls, obj: SOMcreator.Object, item: QTreeWidgetItem, index: int):

        start_index = index * 2
        item.setText(start_index, obj.name)
        item.setText(start_index + 1, obj.ident_value)
        item.setData(start_index, CLASS_REFERENCE, obj)
        item.setData(start_index + 1, CLASS_REFERENCE, obj)
        cls.get_properties().object_tree_item_dict[obj] = item

    @classmethod
    def fill_object_tree_layer(cls, objects: list[SOMcreator.Object], parent_item: QTreeWidgetItem):
        obj_dict0, obj_dict1 = cls.get_object_dict(0), cls.get_object_dict(1)

        for obj in objects:
            match_obj = obj_dict0.get(obj)
            item = QTreeWidgetItem()
            cls.add_object_to_item(obj, item, 0)
            if match_obj:
                cls.add_object_to_item(match_obj, item, 1)
            parent_item.addChild(item)
            cls.fill_object_tree_layer(list(obj.children), item)

    @classmethod
    def find_existing_parent(cls, obj: SOMcreator.Object):
        tree = cls.get_window().widget.tree_widget_object
        object_tree_item_dict = cls.get_properties().object_tree_item_dict
        parent = obj.parent
        while parent is not None:
            if parent in object_tree_item_dict:
                return object_tree_item_dict[parent]
            parent = parent.parent
        return tree.invisibleRootItem()

    @classmethod
    def add_missing_objects_to_tree(cls, root_objects: list[SOMcreator.Object]):
        tree = cls.get_window().widget.tree_widget_object
        missing_objects = cls.get_missing_objects(1)
        for obj in root_objects:
            if obj in missing_objects:
                parent = cls.find_existing_parent(obj)
                item = QTreeWidgetItem()
                cls.add_object_to_item(obj, item, 1)
                parent.addChild(item)
            cls.add_missing_objects_to_tree(list(obj.children))

    @classmethod
    def fill_object_tree(cls):
        item_dict = dict()
        tree = cls.get_window().widget.tree_widget_object
        proj0, proj1 = cls.get_project(0), cls.get_project(1)
        obj_dict0, obj_dict1 = cls.get_object_dict(0), cls.get_object_dict(1)
        missing0, missing1 = cls.get_missing_objects(0), cls.get_missing_objects(1)
        cls.fill_object_tree_layer(tool.Project.get_root_objects(False, proj0), tree.invisibleRootItem())
        cls.add_missing_objects_to_tree(tool.Project.get_root_objects(False, proj1))
