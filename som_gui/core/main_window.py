from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtWidgets import QApplication

import som_gui

if TYPE_CHECKING:
    from som_gui.tool import MainWindow, Project, Popups
    from som_gui import tool
from PySide6.QtCore import QCoreApplication,Qt
from PySide6.QtGui import QCloseEvent


def create_main_menu_actions(main_window: Type[tool.MainWindow]):
    """
    Create the actions used in the MainMenuBar. using add_action and set_action. Afterwards the Actions can be called by get_action. This is mostly used in retranslate_ui
    :param main_window:
    :return:
    """
    from som_gui.module.main_window import trigger
    open_window_action = main_window.add_action("menuEdit", "ToggleConsole", trigger.toggle_console)
    main_window.set_action(trigger.TOOGLE_CONSOLE_ACTION, open_window_action)


def retranslate_ui(main_window: Type[tool.MainWindow]):
    """
    retranslates the UI and the Actions of the Main Window
    :param main_window:
    :return:
    """
    from som_gui.module.main_window import trigger

    action = main_window.get_action(trigger.TOOGLE_CONSOLE_ACTION)
    if main_window.is_console_visible():
        action.setText(QCoreApplication.translate("MainWindow", "Hide Console"))
    else:
        action.setText(QCoreApplication.translate("MainWindow", "Show Console"))
    main_window.get().ui.retranslateUi(main_window.get())


def create_main_window(application: QApplication, main_window: Type[tool.MainWindow],property_set:Type[tool.PropertySet]):
    """
    Creates the main window from the given application and hides the console.
    :param application:
    :param main_window:
    :return:
    """
    mw = main_window.create(application)
    mw.show()
    table = main_window.get_property_set_table_widget()
    property_set.set_sorting_indicator(table,0)
    main_window.hide_console()


def close_event(event: QCloseEvent, main_window: Type[tool.MainWindow], popups_tool: Type[tool.Popups]):
    """
    Overwrites Close Event of MainWindow. Asks Save before exiting the main window
    :param event:
    :param main_window:
    :param popups_tool:
    :return:
    """
    reply = popups_tool.request_save_before_exit()
    if reply is None:
        # Dont Close Window
        event.ignore()
        return
    if reply:
        #Save before Closing
        from som_gui.module.project import trigger
        trigger.save()
    #Close Windows
    main_window.get_app().closeAllWindows()
    event.accept()


def refresh_main_window(main_window_tool: Type[MainWindow], project_tool: Type[Project]):
    """
    refresh Statusbar-Text and Window-Title
    :param main_window_tool:
    :param project_tool:
    :return:
    """
    proj = project_tool.get()
    version = f'{QCoreApplication.translate("MainWindow", "Version")}: {proj.version}'
    phase_names = ",".join(proj.get_phase_by_index(i).name for i in proj.active_phases)
    usecase_names = ",".join(proj.get_usecase_by_index(i).name for i in proj.active_usecases)
    status = " | ".join([proj.name, version, phase_names, usecase_names])
    main_window_tool.set_status_bar_text(status)
    main_window_tool.set_window_title(f"SOM-Toolkit v{som_gui.__version__}")


def toggle_console_clicked(main_window: Type[tool.MainWindow]):
    """
    TOggles if Console is Shown
    :param main_window:
    :return:
    """
    main_window.toggle_console()
    retranslate_ui(main_window) #Changes Text from Show to Hide / from Hide to Show
