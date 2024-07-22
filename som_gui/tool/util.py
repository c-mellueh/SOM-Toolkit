from __future__ import annotations
from typing import Callable, TYPE_CHECKING
import os, tempfile
from PySide6.QtCore import QFile
from PySide6.QtGui import QAction, QShortcut, QKeySequence
from PySide6.QtWidgets import QMenu, QMenuBar, QWidget, QComboBox
import som_gui.core.tool
import re
if TYPE_CHECKING:
    from som_gui.module.util.prop import MenuDict, UtilProperties

class Util(som_gui.core.tool.Util):
    @classmethod
    def get_properties(cls) -> UtilProperties:
        return som_gui.UtilProperties
    @classmethod
    def menu_bar_add_menu(cls, menu_bar: QMenuBar, menu_dict: MenuDict, menu_path: str) -> MenuDict:
        menu_steps = menu_path.split("/")
        focus_dict = menu_dict
        parent = menu_bar
        for index, menu_name in enumerate(menu_steps):
            if not menu_name in {menu["name"] for menu in focus_dict["submenu"]}:
                menu = QMenu(parent)
                menu.setTitle(menu.tr(menu_name))
                d = {
                    "name":    menu_name,
                    "submenu": list(),
                    "actions": list(),
                    "menu":    menu
                }
                focus_dict["submenu"].append(d)
            sub_menus = {menu["name"]: menu for menu in focus_dict["submenu"]}
            focus_dict = sub_menus[menu_name]
            parent = focus_dict["menu"]
        return focus_dict

    @classmethod
    def menu_bar_add_action(cls, menu_bar: QMenuBar, menu_dict: MenuDict, menu_path: str, function: Callable):
        menu_steps = menu_path.split("/")
        if len(menu_steps) != 1:
            menu_dict = cls.menu_bar_add_menu(menu_bar, menu_dict, "/".join(menu_steps[:-1]))
            action = QAction(menu_dict["menu"])
            action.setText(action.tr(menu_steps[-1]))
            action.triggered.connect(function)
            menu_dict["actions"].append(action)
        else:
            action = QAction(menu_steps[0])
            menu_dict["actions"].append(action)
            action.triggered.connect(function)

    @classmethod
    def menu_bar_create_actions(cls, menu_dict: MenuDict, parent: QMenu | QMenuBar | None):
        menu = menu_dict["menu"]
        if parent is not None:
            parent.addMenu(menu)
        for sd in menu_dict["submenu"]:
            cls.menu_bar_create_actions(sd, menu)
        for action in menu_dict["actions"]:
            menu.addAction(action)

    @classmethod
    def add_shortcut(cls, sequence: str, window: QWidget, function: Callable):
        prop = cls.get_properties()
        shortcut = QShortcut(QKeySequence(sequence), window)
        if not hasattr(prop, "shortcuts"):
            prop.shourtcuts = list()
        prop.shourtcuts.append(shortcut)
        shortcut.activated.connect(function)

    @classmethod
    def create_context_menu(cls, menu_list: list[list[str, Callable]]) -> QMenu:
        """
        Create a context menu from a menu list.
        The Menu List contains of tuples containing the displayname of action and the callable function itself
        If the displayname contains '/' submenus will be created
        """

        menu_dict = dict()
        menu = QMenu()
        menu_dict[""] = menu
        for text, function in menu_list:
            cls.context_menu_create_action(menu_dict, text, function, False)
        return menu

    @classmethod
    def context_menu_create_action(cls, menu_dict: dict[str, QAction | QMenu], name: str, action_func: None | Callable,
                                   is_sub_menu: bool):
        parent_structure = "/".join(name.split("/")[:-1])
        if parent_structure not in menu_dict:
            parent: QMenu = cls.context_menu_create_action(menu_dict, parent_structure, None, True)
        else:
            parent: QMenu = menu_dict[parent_structure]

        if is_sub_menu:
            menu = parent.addMenu(name.split("/")[-1])
            menu_dict[name] = menu
            return menu

        action = parent.addAction(name.split("/")[-1])
        if action_func is not None:
            action.triggered.connect(action_func)
        menu_dict[name] = action
        return action

    @classmethod
    def create_tempfile(cls, suffix: str | None = None) -> str:
        suffix = ".tmp" if suffix is None else suffix
        return os.path.abspath(tempfile.NamedTemporaryFile(suffix=suffix).name)

    @classmethod
    def transform_guid(cls, guid: str, add_zero_width: bool):
        """Fügt Zero Width Character ein weil PowerBI (WARUM AUCH IMMER FÜR EIN BI PROGRAMM?????) Case Insensitive ist"""
        if add_zero_width:
            return re.sub(r"([A-Z])", lambda m: m.group(0) + u"\u200B", guid)
        else:
            return guid

    @classmethod
    def get_combobox_values(cls, combo_box: QComboBox):
        count = combo_box.count()
        return [combo_box.itemText(i) for i in range(count)]
