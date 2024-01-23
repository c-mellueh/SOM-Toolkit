from __future__ import annotations
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from som_gui.tool import MainWindow, Popups, Project


def set_main_window(window, main_window_tool: Type[MainWindow]):
    main_window_tool.set(window)


def add_menu_entries(main_window_tool: Type[MainWindow]):
    from som_gui.module.main_window import trigger
    main_window_tool.add_action("Test/Neu", trigger.new_file_clicked)


def open_new_file(project_tool: Type[Project], popup_tool: Type[Popups]):
    if not popup_tool.msg_unsaved():
        return
    name = popup_tool.get_project_name()
    if name is not None:
        project_tool.create_project()
        project_tool.set_project_name(name)




def create_menus(main_window_tool: Type[MainWindow]):
    menu_dict = main_window_tool.get_menu_dict()
    menu_dict["menu"] = main_window_tool.get_menu_bar()
    main_window_tool.create_actions(menu_dict)
