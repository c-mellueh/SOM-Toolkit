from __future__ import annotations
import som_gui
from typing import Type
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.tool.project import Project


def open_project(path, project_tool: Type[Project]):
    project_tool.reset_project_infos()
    return project_tool.load_project(path)


def repaint_settings_dialog(project_tool: Type[Project]):
    print(project_tool.get().get_use_case_list())
    project_infos = project_tool.get_project_infos()
    for index, info_dict in enumerate(project_infos):
        project_tool.refresh_info_dict(info_dict, index)


def fill_settings_dialog(project_tool: Type[Project]):
    project_infos = project_tool.get_project_infos()
    for info_dict in project_infos:
        project_tool.add_setting_to_dialog(info_dict)


def update_settings(project_tool: Type[Project]):
    project_infos = project_tool.get_project_infos()
    for info_dict in project_infos:
        project_tool.update_setting(info_dict)


def reset_settings_dialog(project_tool: Type[Project]):
    project_infos = project_tool.get_project_infos()
    for info_dict in project_infos:
        info_dict["value"] = info_dict["get_function"]()
