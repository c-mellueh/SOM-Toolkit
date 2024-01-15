from som_gui.tool.project import Project
from typing import Type


def open_project(path, project_tool: Type[Project]):
    return project_tool.load_project(path)
