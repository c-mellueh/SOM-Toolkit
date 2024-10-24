from __future__ import annotations
import som_gui.core.tool
import som_gui
from typing import TYPE_CHECKING, Callable
from PySide6.QtWidgets import QHBoxLayout, QMenuBar, QApplication, QLineEdit, QStatusBar, QMenu
from PySide6.QtGui import QAction
from som_gui import tool
from som_gui.module.main_window import ui as ui_main_window
import ctypes

if TYPE_CHECKING:
    from som_gui.module.main_window.prop import MainWindowProperties, MenuDict
    from som_gui.module.main_window.qt.ui_MainWindow import Ui_MainWindow


class MainWindow(som_gui.core.tool.MainWindow):
    @classmethod
    def get_properties(cls) -> MainWindowProperties:
        return som_gui.MainWindowProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]


    @classmethod
    def create(cls, application: QApplication):
        if cls.get_properties().window is None:
            window = ui_main_window.MainWindow(application)
            cls.get_properties().window = window
            cls.get_properties().ui = window.ui
            cls.get_properties().application = application
        return cls.get_properties().window

    @classmethod
    def hide_console(cls):
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd != 0:
            ctypes.windll.user32.ShowWindow(hWnd, 0)

    @classmethod
    def show_console(cls):
        console_window = ctypes.windll.kernel32.GetConsoleWindow()
        if console_window != 0:
            # Check if the console is visible
            ctypes.windll.user32.ShowWindow(console_window, 5)  # Show the console

    @classmethod
    def is_console_visible(cls):
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd == 0:
            return False
        if ctypes.windll.user32.IsWindowVisible(hWnd):
            return True
        return False
    @classmethod
    def toggle_console(cls):
        active_window = cls.get_app().activeWindow()
        if cls.is_console_visible():
            cls.hide_console()
        elif ctypes.windll.kernel32.GetConsoleWindow() != 0:
            cls.show_console()
        active_window.activateWindow()

    @classmethod
    def set_window_title(cls, title: str):
        cls.get().setWindowTitle(title)

    @classmethod
    def get_statusbar(cls) -> QStatusBar:
        return cls.get_ui().statusbar

    @classmethod
    def set_status_bar_text(cls, text: str):
        cls.get_ui().statusbar.showMessage(text)

    @classmethod
    def get_menu_bar(cls) -> QMenuBar:
        return cls.get_ui().menubar

    @classmethod
    def add_submenu(cls, parent_name: str, name) -> QMenu:
        if parent_name:
            menu: QMenuBar | QMenu = getattr(cls.get_ui(), parent_name)
        else:
            menu = cls.get_menu_bar()
        return menu.addMenu(name)

    @classmethod
    def add_action2(cls, parent_name: str, name: str, function: Callable) -> QAction:
        if parent_name:
            menu: QMenuBar | QMenu = getattr(cls.get_ui(), parent_name)
        else:
            menu = cls.get_menu_bar()
        action = menu.addAction(name)
        action.triggered.connect(function)
        return action

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
    def get_ident_value_line_edit(cls):
        return cls.get_ui().lineEdit_ident_value

    @classmethod
    def get_attribute_name_line_edit(cls) -> QLineEdit:
        return cls.get_ui().lineEdit_ident_attribute

    @classmethod
    def get_object_name_line_edit(cls):
        return cls.get_ui().line_edit_object_name

    @classmethod
    def get_pset_name_line_edit(cls):
        return cls.get_ui().lineEdit_pSet_name

    @classmethod
    def get_pset_layout(cls):
        return cls.get_ui().box_layout_pset

    @classmethod
    def get_object_name_horizontal_layout(cls) -> QHBoxLayout:
        return cls.get_ui().horizontalLayout_object_button
