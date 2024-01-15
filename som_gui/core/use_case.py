from som_gui.tool.use_case import UseCase
from som_gui.tool.project import Project
from typing import Type


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
