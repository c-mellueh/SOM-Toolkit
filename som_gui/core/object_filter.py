from __future__ import annotations
import logging
import SOMcreator
from PySide6.QtWidgets import QAbstractItemView
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.tool import ObjectFilter, Project
    from PySide6.QtCore import QModelIndex
    from PySide6.QtWidgets import QTreeView


def open_use_case_window(objectfilter_tool: Type[ObjectFilter]):
    window = objectfilter_tool.create_window()
    window.show()
    load_use_cases(objectfilter_tool)
    objectfilter_tool.format_object_tree_header()
    object_tree = objectfilter_tool.get_object_tree()
    pset_tree = objectfilter_tool.get_pset_tree()
    object_tree.expanded.connect(lambda: resize_tree(object_tree, objectfilter_tool))
    pset_tree.expanded.connect(lambda: resize_tree(pset_tree, objectfilter_tool))
    objectfilter_tool.get_widget().buttonBox.accepted.connect(lambda: accept_changes(objectfilter_tool))
    objectfilter_tool.get_widget().buttonBox.rejected.connect(lambda: reject_changes(objectfilter_tool))
    pset_tree.setEnabled(False)

def on_startup(objectfilter_tool: Type[ObjectFilter]):
    logging.debug(f"Startup UseCase")
    objectfilter_tool.reset_use_case_data()
    objectfilter_tool.load_use_cases()
    objectfilter_tool.add_use_case_to_settings_window()


def accept_changes(objectfilter_tool: Type[ObjectFilter]):
    objectfilter_tool.update_pset_data()
    objectfilter_tool.update_attribute_data()
    objectfilter_tool.update_attribute_uses_cases()
    objectfilter_tool.update_pset_use_cases()
    objectfilter_tool.update_object_use_cases()
    window = objectfilter_tool.delete_use_case_window()
    window.close()
    pass


def reject_changes(objectfilter_tool: Type[ObjectFilter]):
    window = objectfilter_tool.delete_use_case_window()
    window.close()


def create_header_context_menu(pos, tree_view: QTreeView, objectfilter_tool: Type[ObjectFilter], project_tool):
    # header = tree_view.header()
    # column_index = header.logicalIndexAt(pos)
    # model = tree_view.model()
    # use_case_index = column_index - objectfilter_tool.get_title_lenght_by_model(model)
    # if use_case_index < 0:
    #     action_dict = {
    #         "Anwendungsfall hinzufügen": lambda: create_use_case(objectfilter_tool, ),
    #         "Leistungsph"}
    # else:
    #     action_dict = {
    #         "Anwendungsfall hinzufügen": lambda: create_use_case(objectfilter_tool, ),
    #         "Umbenennen":                lambda: rename_use_case(use_case_index, objectfilter_tool),
    #         "Löschen":                   lambda: delete_use_case(use_case_index, objectfilter_tool),
    #     }
    #
    # objectfilter_tool.create_context_menu(header.mapToGlobal(pos), action_dict)
    pass


def rename_use_case(use_case_index: int, objectfilter_tool: Type[ObjectFilter]):
    old_name = objectfilter_tool.get_use_case_list()[use_case_index]
    new_name = objectfilter_tool.request_rename_use_case_name(old_name)
    if new_name is None:
        return
    objectfilter_tool.rename_use_case(use_case_index, new_name)


def delete_use_case(use_case_index: int, objectfilter_tool: Type[ObjectFilter]):
    use_case_list = objectfilter_tool.get_use_case_list()
    if len(use_case_list) < 2:  # At least 1 Use case needs to exist
        return
    objectfilter_tool.remove_use_case(use_case_index)


def create_use_case(objectfilter_tool: Type[ObjectFilter]):
    existing_names = objectfilter_tool.get_use_case_list()

    new_name = objectfilter_tool.get_new_use_case_name("Unbenannt", existing_names)
    objectfilter_tool.add_use_case(new_name)


def refresh_object_tree(objectfilter_tool: Type[ObjectFilter], project_tool: Type[Project]):
    load_headers(objectfilter_tool)
    load_objects(objectfilter_tool, project_tool)
    objectfilter_tool.update_active_object_label()
    objectfilter_tool.update_pset_tree()


def load_use_cases(objectfilter_tool: Type[ObjectFilter]):
    logging.debug(f"Load UseCases")
    objectfilter_tool.load_use_cases()
    objectfilter_tool.create_tree_models()


def load_headers(objectfilter_tool: Type[ObjectFilter]):
    obj_titles, pset_titles = objectfilter_tool.get_header_texts()
    filter_matrix = objectfilter_tool.get_filter_matrix()
    header_data = objectfilter_tool.create_header_data(filter_matrix)
    objectfilter_tool.set_header_data(header_data)
    header_texts = objectfilter_tool.get_filter_names()
    obj_titles += header_texts
    object_model = objectfilter_tool.get_object_model()
    objectfilter_tool.set_header_labels(object_model, obj_titles)
    pset_titles += header_texts
    pset_model = objectfilter_tool.get_pset_model()
    objectfilter_tool.set_header_labels(pset_model, pset_titles)


def load_objects(objectfilter_tool: Type[ObjectFilter], project_tool: Type[Project]):
    root_objects = project_tool.get_root_objects(filter_objects=False)
    objectfilter_tool.fill_object_tree(root_objects)


def tree_mouse_press_event(index: QModelIndex, objectfilter_tool: Type[ObjectFilter]):
    if index is None:
        return False
    if index.column() < objectfilter_tool.get_title_count_by_index(index):
        return True
    if not objectfilter_tool.is_object_enabled(index):
        return False
    objectfilter_tool.toggle_checkstate(index)


def tree_mouse_move_event(index: QModelIndex, objectfilter_tool: Type[ObjectFilter]):
    if not objectfilter_tool.is_tree_clicked():
        objectfilter_tool.tree_activate_click_drag(index)
        return
    objectfilter_tool.tree_move_click_drag(index)
    linked_data = objectfilter_tool.get_linked_data(index)
    if isinstance(linked_data, SOMcreator.Object):
        objectfilter_tool.update_object_data(linked_data)


def tree_mouse_release_event(index, objectfilter_tool: Type[ObjectFilter]):
    if index is None:
        return
    objectfilter_tool.tree_release_click_drag(index)
    linked_data = objectfilter_tool.get_linked_data(index)
    if isinstance(linked_data, SOMcreator.Object):
        object_clicked(linked_data, objectfilter_tool)


def resize_tree(tree: QTreeView, objectfilter_tool: Type[ObjectFilter]):
    objectfilter_tool.resize_tree(tree)


def object_clicked(obj: SOMcreator.Object, objectfilter_tool: Type[ObjectFilter]):
    objectfilter_tool.get_pset_tree().setEnabled(True)
    objectfilter_tool.update_pset_data()
    objectfilter_tool.update_attribute_data()
    objectfilter_tool.set_active_object(obj)
    objectfilter_tool.update_pset_tree()
    objectfilter_tool.update_object_data(obj)
