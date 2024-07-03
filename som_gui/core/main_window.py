from __future__ import annotations
from typing import TYPE_CHECKING, Type

import som_gui
from som_gui.core import project as core_project
from PySide6.QtWidgets import QApplication

if TYPE_CHECKING:
    from som_gui.tool import MainWindow, Settings, Project, Popups
    from som_gui import tool


def create_main_window(application: QApplication, main_window: Type[tool.MainWindow]):
    mw = main_window.create(application)
    mw.show()


def close_event(project_tool: Type[Project], settings_tool: Type[Settings],
                popups_tool: Type[Popups]):
    reply = popups_tool.request_save_before_exit()
    if reply is None:  # abort Dialog
        return False
    if reply is False:  # No
        return True
    core_project.save_clicked(project_tool, popups_tool, settings_tool)
    return True


def add_label_to_statusbar(main_window_tool: Type[MainWindow]):
    main_window_tool.create_status_label()


def create_menus(main_window_tool: Type[MainWindow], util: Type[tool.Util]):
    menu_dict = main_window_tool.get_menu_dict()
    menu_bar = main_window_tool.get_menu_bar()
    menu_dict["menu"] = menu_bar
    util.menu_bar_create_actions(menu_dict, None)


def refresh_main_window(main_window_tool: Type[MainWindow], project_tool: Type[Project]):
    status = f"{project_tool.get_project_name()} {project_tool.get_project_version()}"
    main_window_tool.set_status_bar_text(status)
    main_window_tool.set_window_title(f"SOM-Toolkit v{som_gui.__version__}")


def fill_old_menus(main_window_tool: Type[MainWindow]):
    """
    fill menus of functions / windows that aren't refactored
    """

    main_window = main_window_tool.get()

    main_window_tool.add_action("Datei/Mappings", lambda: main_window_tool.open_mapping_window())
    main_window_tool.add_action("Modelle/Informationen einlesen",
                                lambda: main_window_tool.open_attribute_import_window())
