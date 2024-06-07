from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from PySide6.QtGui import QAction, QShortcut, QKeySequence
from PySide6.QtWidgets import QMenu, QMenuBar, QWidget
import som_gui.core.tool

if TYPE_CHECKING:
    from som_gui.module.util.prop import MenuDict, UtilProperties

class Util(som_gui.core.tool.Util):
    @classmethod
    def get_properties(cls) -> UtilProperties:
        return som_gui.UtilProperties
    @classmethod
    def add_menu(cls, menu_bar: QMenuBar, menu_dict: MenuDict, menu_path: str) -> MenuDict:
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
    def add_action(cls, menu_bar: QMenuBar, menu_dict: MenuDict, menu_path: str, function: Callable):
        menu_steps = menu_path.split("/")
        if len(menu_steps) != 1:
            menu_dict = cls.add_menu(menu_bar, menu_dict, "/".join(menu_steps[:-1]))
            action = QAction(menu_dict["menu"])
            action.setText(action.tr(menu_steps[-1]))
            action.triggered.connect(function)
            menu_dict["actions"].append(action)
        else:
            action = QAction(menu_steps[0])
            menu_dict["actions"].append(action)
            action.triggered.connect(function)

    @classmethod
    def create_actions(cls, menu_dict: MenuDict, parent: QMenu | QMenuBar | None):
        menu = menu_dict["menu"]
        if parent is not None:
            parent.addMenu(menu)
        for sd in menu_dict["submenu"]:
            cls.create_actions(sd, menu)
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
