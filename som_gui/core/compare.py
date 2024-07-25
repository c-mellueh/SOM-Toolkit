from __future__ import annotations
from typing import TYPE_CHECKING, Type
from SOMcreator import Project

if TYPE_CHECKING:
    from som_gui import tool


def test(compare: Type[tool.Compare], project: Type[tool.Project]):
    other_file_path = "C:/Users/ChristophMellueh/Desktop/test_som.SOMjson"
    project_0 = project.get()
    project_1 = Project.open(other_file_path)
    compare.set_projects(project_0, project_1)
    compare.create_object_dicts()
    window = compare.create_window()
    compare.fill_object_tree()
    window.exec()
