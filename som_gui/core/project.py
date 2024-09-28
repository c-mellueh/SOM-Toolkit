from __future__ import annotations

import logging
import os
from typing import Type
from typing import TYPE_CHECKING
import som_gui
from som_gui.module.project.constants import FILETYPE, OPEN_PATH, SAVE_PATH

if TYPE_CHECKING:
    from som_gui.tool import Project, Popups, Appdata
    from som_gui import tool
    from som_gui.module.project import ui
def save_clicked(project_tool: Type[Project], popup_tool: Type[Popups], appdata: Type[Appdata],
                 main_window: Type[tool.MainWindow]):
    save_path = appdata.get_path(SAVE_PATH)
    if not os.path.exists(save_path) or not save_path.endswith("json"):
        save_as_clicked(project_tool, popup_tool, appdata, main_window)
    else:
        save_project(save_path, project_tool, appdata)


def save_as_clicked(project_tool: Type[Project], popup_tool: Type[Popups], appdata: Type[Appdata],
                    main_window: Type[tool.MainWindow]):
    path = appdata.get_path(SAVE_PATH)
    path = popup_tool.get_save_path(FILETYPE, main_window.get(), path, "Save Project")
    if path:
        save_project(path, project_tool, appdata)


def open_file_clicked(project_tool: Type[Project], appdata: Type[Appdata], main_window: Type[tool.MainWindow],
                      popups: Type[tool.Popups]):
    path = appdata.get_path(OPEN_PATH)
    path = popups.get_open_path(FILETYPE, main_window.get(), path, "Open Project")
    if not path:
        return

    project_tool.reset_project_infos()
    logging.info("Load Project")
    appdata.set_path(OPEN_PATH, path)
    appdata.set_path(SAVE_PATH, path)
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


def save_project(path: str, project_tool: Type[Project], appdata: Type[Appdata]):
    for plugin_function in project_tool.get_plugin_functions():
        plugin_function()
    project = project_tool.get()
    project.save(path)
    appdata.set_path(OPEN_PATH, path)
    appdata.set_path(SAVE_PATH, path)
    logging.info(f"Speichern abgeschlossen")


def create_project(project_tool: Type[Project]):
    logging.debug(f"Create Project")
    project_tool.create_project()


def open_project(path, project_tool: Type[Project]):
    proj = project_tool.load_project(path)
    project_tool.set_active_project(proj)
    som_gui.on_new_project()
    return proj


def add_project(project_tool: Type[Project], appdata: Type[tool.Appdata], popups: Type[tool.Popups],
                main_window: Type[tool.MainWindow]):
    path = appdata.get_path(OPEN_PATH)
    path = popups.get_open_path(FILETYPE, main_window.get(), path, "Open Project")
    if not path:
        return
    p1 = project_tool.get()
    p2 = project_tool.load_project(path)
    project_tool.merge_projects(p1, p2)

    logging.warning(f"Import der Bauwerksstruktur wird noch nicht unterstützt")

def settings_general_created(widget: ui.SettingsGeneral, project: Type[tool.Project]):
    project.set_settings_general_widget(widget)
    proj = project.get()
    widget.ui.le_name.setText(proj.name)
    widget.ui.le_version.setText(proj.version)
    widget.ui.le_description.setText(proj.description)
    widget.ui.le_author_mail.setText(proj.author)


def settings_path_created(widget: ui.SettingsPath, project: Type[tool.Project], appdata: Type[tool.Appdata]):
    project.set_settings_path_widget(widget)
    proj = project.get()
    path = proj.path if "path" in dir(proj) else ""
    widget.ui.le_project_path.setText(path)
    widget.ui.le_save_path.setText(appdata.get_path(SAVE_PATH))
    widget.ui.le_open_path.setText(appdata.get_path(OPEN_PATH))


def settings_accepted(project: Type[tool.Project], appdata: Type[tool.Appdata]):
    widget = project.get_settings_general_widget()
    proj = project.get()
    proj.author = widget.ui.le_author_mail.text()
    proj.name = widget.ui.le_name.text()
    proj.version = widget.ui.le_version.text()
    proj.description = widget.ui.le_description.toPlainText()

    path_widget = project.get_settings_path_widget()
    proj.path = path_widget.ui.le_project_path.text()
    appdata.set_path(SAVE_PATH, path_widget.ui.le_save_path.text())
    appdata.set_path(OPEN_PATH, path_widget.ui.le_open_path.text())
