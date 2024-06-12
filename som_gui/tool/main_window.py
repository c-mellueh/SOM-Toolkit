from __future__ import annotations
import som_gui.core.tool
import som_gui
from typing import TYPE_CHECKING, Callable
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar, QApplication, QLabel
from som_gui import tool
from som_gui.module.main_window import ui
if TYPE_CHECKING:
    from som_gui.module.main_window.prop import MainWindowProperties, MenuDict
    from som_gui.tool.object import ObjectDataDict
    from som_gui.main_window import Ui_MainWindow


class MainWindow(som_gui.core.tool.MainWindow):
    @classmethod
    def create(cls, application: QApplication):
        if cls.get_properties().window is None:
            window = ui.MainWindow(application)
            cls.get_properties().window = window
            cls.get_properties().ui = window.ui
            cls.get_properties().application = application
        return cls.get_properties().window
    @classmethod
    def set_window_title(cls, title: str):
        cls.get().setWindowTitle(title)

    @classmethod
    def create_status_label(cls):
        label = QLabel()
        prop = cls.get_properties()
        prop.status_bar_label = label
        cls.get_ui().statusbar.addWidget(label)

    @classmethod
    def set_status_bar_text(cls, text: str):
        cls.get_properties().status_bar_label.setText(text)

    @classmethod
    def get_menu_bar(cls) -> QMenuBar:
        return cls.get_ui().menubar

    @classmethod
    def get_menu_dict(cls) -> MenuDict:
        prop = cls.get_properties()
        return prop.menu_dict

    @classmethod
    def add_action(cls, menu_path: str, function: Callable):
        menu_bar = cls.get_menu_bar()
        menu_dict = cls.get_menu_dict()
        tool.Util.add_action(menu_bar, menu_dict, menu_path, function)

    @classmethod
    def get_properties(cls) -> MainWindowProperties:
        return som_gui.MainWindowProperties

    @classmethod
    def get_ui(cls) -> Ui_MainWindow:
        return cls.get_properties().ui

    @classmethod
    def get(cls) -> som_gui.MainWindow:
        return cls.get_properties().window

    @classmethod
    def get_app(cls) -> QApplication:
        return cls.get_properties().application


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

    @classmethod
    def get_attribute_table(cls):
        return cls.get_ui().table_attribute

    @classmethod
    def get_object_tree_widget(cls):
        return cls.get_ui().tree_object

    @classmethod
    def get_property_set_table_widget(cls):
        return cls.get_ui().table_pset

    @classmethod
    def get_ident_pset_name_line_edit(cls):
        return cls.get_ui().lineEdit_ident_pSet

    @classmethod
    def get_pset_name_line_edit(cls):
        return cls.get_ui().lineEdit_pSet_name

    @classmethod
    def get_pset_layout(cls):
        return cls.get_ui().box_layout_pset
