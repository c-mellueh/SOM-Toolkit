from __future__ import annotations
import som_gui.core.tool
import som_gui
from typing import TYPE_CHECKING, Callable
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar, QApplication, QLabel

if TYPE_CHECKING:
    from som_gui.module.main_window.prop import MainWindowProperties, MenuDict
    from som_gui.tool.object import ObjectDataDict
    from som_gui.main_window import Ui_MainWindow


class MainWindow(som_gui.core.tool.MainWindow):
    @classmethod
    def set_window_title(cls, title: str):
        cls.get().setWindowTitle(title)

    @classmethod
    def create_status_label(cls):
        label = QLabel()
        prop = cls.get_main_menu_properties()
        prop.status_bar_label = label
        cls.get_ui().statusbar.addWidget(label)

    @classmethod
    def set_status_bar_text(cls, text: str):
        cls.get_main_menu_properties().status_bar_label.setText(text)

    @classmethod
    def get_menu_bar(cls) -> QMenuBar:
        return cls.get_ui().menubar

    @classmethod
    def get_menu_dict(cls) -> MenuDict:
        prop = cls.get_main_menu_properties()
        return prop.menu_dict

    @classmethod
    def create_actions(cls, menu_dict: MenuDict, parent: QMenu | QMenuBar):
        menu = menu_dict["menu"]
        if parent is not None:
            parent.addMenu(menu)
        for sd in menu_dict["submenu"]:
            cls.create_actions(sd, menu)
        for action in menu_dict["actions"]:
            menu.addAction(action)

    @classmethod
    def add_menu(cls, menu_path: str) -> MenuDict:
        menu_steps = menu_path.split("/")
        menu_dict = cls.get_menu_dict()
        focus_dict = menu_dict
        parent = cls.get_ui().menubar
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
    def add_action(cls, menu_path: str, function: Callable):
        menu_steps = menu_path.split("/")
        print(menu_path)
        if len(menu_steps) != 1:
            menu_dict = cls.add_menu("/".join(menu_steps[:-1]))
            action = QAction(menu_dict["menu"])
            action.setText(action.tr(menu_steps[-1]))
            action.triggered.connect(function)
            menu_dict["actions"].append(action)
        else:
            action = QAction(menu_steps[0])
            cls.get_menu_dict()["actions"].append(action)
            action.triggered.connect(function)

    @classmethod
    def get_main_menu_properties(cls) -> MainWindowProperties:
        return som_gui.MainWindowProperties

    @classmethod
    def get_ui(cls) -> Ui_MainWindow:
        return cls.get_main_menu_properties().ui

    @classmethod
    def get(cls) -> som_gui.MainWindow:
        return cls.get_main_menu_properties().window

    @classmethod
    def get_app(cls) -> QApplication:
        return som_gui.MainUi.window.app

    @classmethod
    def set(cls, window):
        prop = cls.get_main_menu_properties()
        prop.window = window
        prop.ui = window.ui

    @classmethod
    def get_object_infos(cls) -> ObjectDataDict:
        ui = cls.get_ui()
        d: ObjectDataDict = dict()
        d["name"] = ui.line_edit_object_name.text()
        d["is_group"] = False
        d["ident_pset_name"] = ui.lineEdit_ident_pSet.text()
        d["ident_attribute_name"] = ui.lineEdit_ident_attribute.text()
        d["ident_value"] = ui.lineEdit_ident_value.text()
        d["ifc_mappings"] = ["IfcBuildingElementProxy"]
        d["abbreviation"] = ui.line_edit_abbreviation.text()
        return d

    @classmethod
    def get_pset_name(cls):
        return cls.get_ui().lineEdit_pSet_name.text()
