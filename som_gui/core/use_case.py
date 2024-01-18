import logging

import SOMcreator

from som_gui.tool.use_case import UseCase
from som_gui.tool.project import Project
from typing import Type
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItem


def on_startup(use_case_tool: Type[UseCase]):
    logging.debug(f"Startup UseCase")
    use_case_tool.reset_use_case_data()
    use_case_tool.load_use_cases()
    use_case_tool.add_use_case_to_settings_window()

def accept_changes(use_case_tool: Type[UseCase]):
    old_current_use_case = use_case_tool.get_use_case()
    use_case_tool.update_project_use_cases()
    # if active usecase is deleted take first usecase as active usecase
    if old_current_use_case not in use_case_tool.get_use_case_list():
        use_case_tool.set_use_case(use_case_tool.get_use_case_list()[0])
    use_case_tool.update_pset_data()
    use_case_tool.update_attribute_data()
    use_case_tool.update_attribute_uses_cases()
    use_case_tool.update_pset_uses_cases()
    use_case_tool.update_object_uses_cases()
    window = use_case_tool.delete_use_case_window()
    window.close()
    pass


def reject_changes(use_case_tool: Type[UseCase]):
    window = use_case_tool.delete_use_case_window()
    window.close()


def create_header_context_menu(pos, tree_view: QTreeView, use_case_tool: Type[UseCase], project_tool):
    header = tree_view.header()
    column_index = header.logicalIndexAt(pos)
    model = tree_view.model()
    use_case_index = column_index - use_case_tool.get_title_lenght_by_model(model)
    proj = project_tool.get()
    if use_case_index < 0:
        action_dict = {
            "Anwendungsfall hinzufügen": lambda: create_use_case(use_case_tool, ), }
    else:
        action_dict = {
            "Anwendungsfall hinzufügen": lambda: create_use_case(use_case_tool, ),
            "Umbenennen":                lambda: rename_use_case(use_case_index, use_case_tool),
            "Löschen":                   lambda: delete_use_case(use_case_index, use_case_tool),
        }

    use_case_tool.create_context_menu(header.mapToGlobal(pos), action_dict)
    pass


def rename_use_case(use_case_index: int, use_case_tool: Type[UseCase]):
    old_name = use_case_tool.get_use_case_list()[use_case_index]
    new_name = use_case_tool.request_rename_use_case_name(old_name)
    if new_name is None:
        return
    use_case_tool.rename_use_case(use_case_index, new_name)


def delete_use_case(use_case_index: int, use_case_tool: Type[UseCase]):
    use_case_list = use_case_tool.get_use_case_list()
    if len(use_case_list) < 2:  # At least 1 Use case needs to exist
        return
    use_case_tool.remove_use_case(use_case_index)


def create_use_case(use_case_tool: Type[UseCase]):
    new_name = use_case_tool.get_new_use_case_name("Unbenannt")
    use_case_tool.add_use_case(new_name)


def refresh_object_tree(use_case_tool: Type[UseCase], project_tool: Type[Project]):
    load_headers(use_case_tool)
    load_objects(use_case_tool, project_tool)
    use_case_tool.update_active_object_label()
    use_case_tool.update_pset_tree()


def load_use_cases(use_case_tool: Type[UseCase]):
    logging.debug(f"Load UseCases")
    use_case_tool.load_use_cases()
    use_case_tool.create_tree_models()


def load_headers(use_case_tool: Type[UseCase]):
    obj_titles, pset_titles = use_case_tool.get_header_texts()
    use_case_list = use_case_tool.get_use_case_list()
    obj_titles += use_case_list
    object_model = use_case_tool.get_object_model()
    use_case_tool.set_header_labels(object_model, obj_titles)
    pset_titles += use_case_list
    pset_model = use_case_tool.get_pset_model()
    use_case_tool.set_header_labels(pset_model, pset_titles)


def load_objects(use_case_tool: Type[UseCase], project_tool: Type[Project]):
    root_objects = project_tool.get_root_objects(filter=False)
    use_case_tool.fill_object_tree(root_objects)


def tree_mouse_press_event(index: QModelIndex, use_case_tool: Type[UseCase]):
    if index is None:
        return False
    if index.column() < use_case_tool.get_title_count_by_index(index):
        return True
    if not use_case_tool.is_object_enabled(index):
        return False
    use_case_tool.toggle_checkstate(index)


def tree_mouse_move_event(index: QModelIndex, use_case_tool: Type[UseCase]):
    if not use_case_tool.is_tree_clicked():
        use_case_tool.tree_activate_click_drag(index)
        return
    use_case_tool.tree_move_click_drag(index)
    linked_data = use_case_tool.get_linked_data(index)
    if isinstance(linked_data, SOMcreator.Object):
        use_case_tool.update_object_data(linked_data)

def tree_mouse_release_event(index, use_case_tool: Type[UseCase]):
    if index is None:
        return
    use_case_tool.tree_release_click_drag(index)
    linked_data = use_case_tool.get_linked_data(index)
    if isinstance(linked_data, SOMcreator.Object):
        object_clicked(linked_data, use_case_tool)


def resize_tree(tree: QTreeView, use_case_tool: Type[UseCase]):
    use_case_tool.resize_tree(tree)

def object_clicked(obj: SOMcreator.Object, use_case_tool: Type[UseCase]):
    use_case_tool.update_pset_data()
    use_case_tool.update_attribute_data()
    use_case_tool.set_active_object(obj)
    use_case_tool.update_pset_tree()
    use_case_tool.update_object_data(obj)
