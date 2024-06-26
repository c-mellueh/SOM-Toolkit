from dataclasses import dataclass, field
from SOMcreator import Project
from PySide6.QtWidgets import QDialog
from typing import TypedDict, Callable


class InfoDict(TypedDict):
    get_function: Callable
    set_function: Callable
    display_name: str
    value: str
    options: Callable


class ProjectProperties:
    project_infos: list[InfoDict] = list()
    active_project: Project | None = None
    settings_window: QDialog = None
    shourtcuts: list = list()
    plugin_save_functions: list[Callable] = list()
