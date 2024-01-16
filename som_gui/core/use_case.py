from som_gui.tool.use_case import UseCase
from som_gui.tool.project import Project
from typing import Type
from PySide6.QtCore import QModelIndex


def refresh_object_tree(use_case_tool, project_tool):
    load_headers(use_case_tool)
    load_objects(use_case_tool, project_tool)


def create_use_case(use_case_tool: Type[UseCase]):
    use_case_tool.create_use_case("Test")


def load_use_cases(use_case_tool: Type[UseCase]):
    use_case_list = use_case_tool.get_use_case_list()
    use_case_tool.load_use_cases()


def load_headers(use_case_tool: Type[UseCase]):
    header_text_list = ["Objekt", "Identifier"]
    header_text_list += use_case_tool.get_use_case_list()
    use_case_tool.set_header_labels(header_text_list)


def load_objects(use_case_tool: Type[UseCase], project_tool: Type[Project]):
    root_objects = project_tool.get_root_objects(filter=False)
    use_case_tool.fill_object_tree(root_objects)


def tree_mouse_press_event(index: QModelIndex, use_case_tool: Type[UseCase]):
    if index is None:
        return False
    if index.column() < use_case_tool.get_object_title_count():
        return True
    if not use_case_tool.is_object_enabled(index):
        return False
    use_case_tool.toggle_checkstate(index)


def tree_mouse_move_event(index: QModelIndex, use_case_tool: Type[UseCase]):
    if not use_case_tool.is_object_tree_clicked():
        use_case_tool.tree_activate_click_drag(index)
        return
    use_case_tool.tree_move_click_drag(index)


def tree_mouse_release_event(index, use_case_tool: Type[UseCase]):
    if index is None:
        return
    use_case_tool.tree_release_click_drag(index)


def resize_tree(tree, use_case_tool: Type[UseCase]):
    use_case_tool.resize_tree(tree)
