from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui.module.mapping import trigger, ui

if TYPE_CHECKING:
    from som_gui.module.mapping.prop import MappingProperties
    from PySide6.QtGui import QAction
from som_gui.module.project.constants import CLASS_REFERENCE


class Mapping(som_gui.core.tool.Mapping):
    @classmethod
    def get_properties(cls) -> MappingProperties:
        return som_gui.MappingProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

    @classmethod
    def create_window(cls):
        prop = cls.get_properties()
        prop.window = ui.MappingWindow()
        prop.object_tree = prop.window.ui.object_tree
        prop.pset_tree = prop.window.ui.pset_tree
        return cls.get_window()

    @classmethod
    def get_window(cls):
        return cls.get_properties().window

    @classmethod
    def connect_window_triggers(cls, window: ui.MappingWindow) -> None:
        window.ui.action_ifc.triggered.connect(trigger.export_revit_ifc_mapping)
        window.ui.action_shared_parameters.triggered.connect(
            trigger.export_revit_shared_parameters
        )
        window.ui.object_tree.itemSelectionChanged.connect(trigger.update_pset_tree)
        cls.get_object_tree().itemChanged.connect(trigger.tree_item_changed)
        cls.get_pset_tree().itemChanged.connect(trigger.tree_item_changed)

    @classmethod
    def get_object_tree(cls) -> ui.ObjectTreeWidget:
        return cls.get_properties().object_tree

    @classmethod
    def get_pset_tree(cls) -> ui.PropertySetTreeWidget:
        return cls.get_properties().pset_tree

    @classmethod
    def get_selected_object(cls) -> SOMcreator.SOMClass | None:
        tree = cls.get_object_tree()
        selected_items = tree.selectedItems()
        if not selected_items:
            return None
        return selected_items[0].data(0, CLASS_REFERENCE)

    @classmethod
    def fill_object_tree(cls, root_objects: list[SOMcreator.SOMClass]) -> None:
        tree = cls.get_object_tree()
        cls.update_tree(set(root_objects), tree.invisibleRootItem(), tree)

    @classmethod
    def update_tree(
        cls,
        entities: set[SOMcreator.SOMProperty | SOMcreator.SOMClass],
        parent_item: QTreeWidgetItem,
        tree: ui.ObjectTreeWidget,
    ):

        existing_entities_dict = {
            parent_item.child(index).data(0, CLASS_REFERENCE): index
            for index in range(parent_item.childCount())
        }

        old_entities = set(existing_entities_dict.keys())
        new_entities = entities.difference(old_entities)
        delete_entities = old_entities.difference(entities)

        for entity in reversed(
            sorted(delete_entities, key=lambda o: existing_entities_dict[o])
        ):
            row_index = existing_entities_dict[entity]
            parent_item.removeChild(parent_item.child(row_index))

        for new_entity in sorted(new_entities, key=lambda x: x.name):
            child = cls.create_child(new_entity)
            parent_item.addChild(child)

        for child_row in range(parent_item.childCount()):
            class_item = parent_item.child(child_row)
            entity = cls.get_entity_from_item(class_item)
            if not (
                parent_item.isExpanded() or parent_item == tree.invisibleRootItem()
            ):
                continue
            if isinstance(entity, SOMcreator.SOMClass):
                cls.update_tree(
                    set(entity.get_children(filter=False)), class_item, tree
                )
            if isinstance(entity, SOMcreator.SOMPropertySet):
                cls.update_tree(
                    set(entity.get_attributes(filter=True)), class_item, tree
                )

    @classmethod
    def create_child(
        cls,
        entity: (
            SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty
        ),
    ) -> QTreeWidgetItem:
        entity_item = QTreeWidgetItem()
        entity_item.setData(0, CLASS_REFERENCE, entity)
        entity_item.setText(0, entity.name)
        cs = (
            Qt.CheckState.Checked
            if cls.get_checkstate(entity)
            else Qt.CheckState.Unchecked
        )
        entity_item.setCheckState(0, cs)
        if isinstance(entity, SOMcreator.SOMClass):
            mapping_text = "; ".join(entity.ifc_mapping)

        elif isinstance(entity, SOMcreator.SOMPropertySet):
            mapping_text = ""
        else:
            disable_state = not cls.get_checkstate(entity.property_set)
            entity_item.setDisabled(disable_state)
            mapping_text = entity.revit_name
        entity_item.setText(1, mapping_text)
        return entity_item

    @classmethod
    def get_checkstate(
        cls,
        entity: (
            SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty
        ),
    ):
        if entity not in cls.get_properties().check_state_dict:
            cls.set_checkstate(entity, True)
        return cls.get_properties().check_state_dict[entity]

    @classmethod
    def set_checkstate(
        cls,
        entity: (
            SOMcreator.SOMClass | SOMcreator.SOMPropertySet | SOMcreator.SOMProperty
        ),
        checkstate: bool,
    ) -> None:
        cls.get_properties().check_state_dict[entity] = checkstate

    @classmethod
    def get_entity_from_item(cls, item: QTreeWidgetItem):
        return item.data(0, CLASS_REFERENCE)

    @classmethod
    def disable_all_child_entities(cls, item: QTreeWidgetItem, disabled: bool):
        for child_index in range(item.childCount()):
            child_item = item.child(child_index)
            child_item.setDisabled(disabled)
            if child_item.checkState(0) == Qt.CheckState.Unchecked:
                continue
            cls.disable_all_child_entities(child_item, disabled)

    @classmethod
    def create_export_dict(cls, root_objects: list[SOMcreator.SOMClass]) -> dict:
        def _loop_objects(o: SOMcreator.SOMClass):
            cs = cls.get_checkstate(o)
            if not cs:
                return
            cls.add_object_to_ifc_export_data(o)
            for child in o.get_children(filter=True):
                _loop_objects(child)

        cls.reset_export_dict()
        for obj in root_objects:
            _loop_objects(obj)
        return cls.get_ifc_export_dict()

    @classmethod
    def add_object_to_ifc_export_data(cls, obj: SOMcreator.SOMClass) -> None:
        export_dict = cls.get_properties().ifc_export_dict
        for property_set in obj.get_property_sets(filter=False):
            if not cls.get_checkstate(property_set):
                continue
            for attribute in property_set.get_attributes(filter=False):
                if not cls.get_checkstate(attribute):
                    continue
                if property_set.name not in export_dict:
                    export_dict[property_set.name] = (list(), set())
                property_set_list = export_dict[property_set.name]
                if attribute.name not in set(a.name for a in property_set_list[0]):
                    property_set_list[0].append(attribute)
                property_set_list[1].update(obj.ifc_mapping)
        cls.get_properties().ifc_export_dict = export_dict

    @classmethod
    def get_ifc_export_dict(cls):
        return cls.get_properties().ifc_export_dict

    @classmethod
    def reset_export_dict(cls):
        cls.get_properties().ifc_export_dict = dict()
