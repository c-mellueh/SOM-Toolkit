from dataclasses import dataclass
from SOMcreator import Project
from PySide6.QtWidgets import QDialog
from typing import TypedDict, Callable


class InfoDict(TypedDict):
    get_function: Callable
    set_function: Callable
    display_name: str
    value: str
    options: Callable


@dataclass
class ProjectProperties:
    project_infos: list[InfoDict]
    active_project: Project | None = None
    settings_window: QDialog = None
