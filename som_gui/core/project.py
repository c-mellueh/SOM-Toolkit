from __future__ import annotations

import logging
import os
from typing import Type
from typing import TYPE_CHECKING
import som_gui
from som_gui.module.project.constants import FILETYPE, OPEN_PATH, SAVE_PATH

if TYPE_CHECKING:
    from som_gui.tool import Project, Popups, Settings
    from som_gui import tool


def save_clicked(project_tool: Type[Project], popup_tool: Type[Popups], settings_tool: Type[Settings],
                 main_window: Type[tool.MainWindow]):
    save_path = settings_tool.get_path(SAVE_PATH)
    if not os.path.exists(save_path) or not save_path.endswith("json"):
        save_as_clicked(project_tool, popup_tool, settings_tool, main_window)
    else:
        save_project(save_path, project_tool, settings_tool)


def save_as_clicked(project_tool: Type[Project], popup_tool: Type[Popups], settings_tool: Type[Settings],
                    main_window: Type[tool.MainWindow]):
    path = settings_tool.get_path(SAVE_PATH)
    path = popup_tool.get_save_path(FILETYPE, main_window.get(), path, "Save Project")
    if path:
        save_project(path, project_tool, settings_tool)


def open_file_clicked(project_tool: Type[Project], settings: Type[Settings], main_window: Type[tool.MainWindow],
                      popups: Type[tool.Popups]):
    path = settings.get_path(OPEN_PATH)
    path = popups.get_open_path(FILETYPE, main_window.get(), path, "Open Project")
    if not path:
        return

    logging.info("Load Project")
    settings.set_path(OPEN_PATH, path)
    settings.set_path(SAVE_PATH, path)
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
    settings_tool.set_path(OPEN_PATH, path)
    settings_tool.set_path(SAVE_PATH, path)
    logging.info(f"Speichern abgeschlossen")


def create_project(project_tool: Type[Project]):
    logging.debug(f"Create Project")
    project_tool.create_project()


def open_project(path, project_tool: Type[Project]):
    proj = project_tool.load_project(path)
    project_tool.set_active_project(proj)
    som_gui.on_new_project()
    return proj


def add_project(project_tool: Type[Project], settings: Type[tool.Settings], popups: Type[tool.Popups],
                main_window: Type[tool.MainWindow]):
    path = settings.get_path(OPEN_PATH)
    path = popups.get_open_path(FILETYPE, main_window.get(), path, "Open Project")
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
