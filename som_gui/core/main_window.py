from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui.tool import MainWindow


def set_main_window(window, main_window_tool: Type[MainWindow]):
    main_window_tool.set(window)


def add_menu_entries(main_window_tool: Type[MainWindow]):
    main_window_tool.add_action("Test/Call", main_window_tool.test_call)


def create_menus(main_window_tool: Type[MainWindow]):
    menu_dict = main_window_tool.get_menu_dict()
    menu_dict["menu"] = main_window_tool.get_menu_bar()
    main_window_tool.create_actions(menu_dict)
