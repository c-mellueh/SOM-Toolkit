from __future__ import annotations

import logging
import os
from typing import Type
from typing import TYPE_CHECKING
import som_gui

FILETYPE = "SOM Project  (*.SOMjson);;all (*.*)"
if TYPE_CHECKING:
    from som_gui.tool import Project, Popups, Settings


def save_clicked(project_tool: Type[Project], popup_tool: Type[Popups], settings_tool: Type[Settings]):
    save_path = settings_tool.get_save_path()
    if not os.path.exists(save_path) or not save_path.endswith("json"):
        save_as_clicked(project_tool, popup_tool, settings_tool)
    else:
        save_project(save_path, project_tool, settings_tool)


def save_as_clicked(project_tool: Type[Project], popup_tool: Type[Popups], settings_tool: Type[Settings]):
    save_path = settings_tool.get_save_path()
    if not os.path.exists(save_path):
        save_path = ""
    else:
        save_path = os.path.splitext(save_path)[0]
    save_path = popup_tool.get_save_path(save_path)
    if save_path:
        save_project(save_path, project_tool, settings_tool)


def open_file_clicked(project_tool: Type[Project], settings: Type[Settings]):
    path = project_tool.get_path("Open Project", FILETYPE)
    if not path:
        return

    project_tool.reset_project_infos()
    logging.info("Load Project")
    settings.set_open_path(path)
    settings.set_save_path(path)
    proj = project_tool.load_project(path)
    project_tool.set_active_project(proj)
    som_gui.on_new_project()


def new_file_clicked(project_tool: Type[Project], popup_tool: Type[Popups]):
    if not popup_tool.msg_unsaved():
        return
    name = popup_tool.get_project_name()
    if name is not None:
        project_tool.create_project()
        project_tool.set_project_name(name)


def save_project(path: str, project_tool: Type[Project], settings_tool: Type[Settings]):
    for plugin_function in project_tool.get_plugin_functions():
        plugin_function()
    project = project_tool.get()
    project.save(path)
    settings_tool.set_open_path(path)
    settings_tool.set_save_path(path)
    logging.info(f"Speichern abgeschlossen")


def create_project(project_tool: Type[Project]):
    logging.debug(f"Create Project")
    project_tool.create_project()


def open_project(path, project_tool: Type[Project]):
    proj = project_tool.load_project(path)
    project_tool.set_active_project(proj)
    som_gui.on_new_project()
    return proj


def add_project(project_tool: Type[Project]):
    path = project_tool.get_path("Add Project", FILETYPE)
    if not path:
        return
    p1 = project_tool.get()
    p2 = project_tool.load_project(path)
    project_tool.merge_projects(p1, p2)

    logging.warning(f"Import der Bauwerksstruktur wird noch nicht unterstützt")


def repaint_settings_dialog(project_tool: Type[Project]):
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
