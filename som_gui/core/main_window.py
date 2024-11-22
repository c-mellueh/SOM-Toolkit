from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtWidgets import QApplication

import som_gui
from som_gui.core import project as core_project

if TYPE_CHECKING:
    from som_gui.tool import MainWindow, Appdata, Project, Popups
    from som_gui import tool
from PySide6.QtCore import QCoreApplication


def create_main_menu_actions(main_window: Type[tool.MainWindow]):
    from som_gui.module.main_window import trigger
    open_window_action = main_window.add_action("menuEdit", "ToggleConsole", trigger.toggle_console)
    main_window.set_action("toggle_console", open_window_action)


def retranslate_ui(main_window: Type[tool.MainWindow]):
    action = main_window.get_action("toggle_console")
    if main_window.is_console_visible():
        action.setText(QCoreApplication.translate("MainWindow", "Hide Console"))
    else:
        action.setText(QCoreApplication.translate("MainWindow", "Show Console"))
    main_window.get().ui.retranslateUi(main_window.get())


def create_main_window(application: QApplication, main_window: Type[tool.MainWindow]):
    """
    Creates the main window from the given application and hides the console.
    :param application:
    :param main_window:
    :return:
    """
    mw = main_window.create(application)
    mw.show()
    main_window.hide_console()


def close_event(project_tool: Type[Project], appdata: Type[Appdata],
                popups_tool: Type[Popups], main_window: Type[tool.MainWindow]):
    reply = popups_tool.request_save_before_exit()
    if reply is None:  # abort Dialog
        return False
    if reply is False:  # No
        return True
    core_project.save_clicked(project_tool, popups_tool, appdata, main_window)
    return True


def refresh_main_window(main_window_tool: Type[MainWindow], project_tool: Type[Project]):
    proj = project_tool.get()
    name = proj.name
    version = f'{QCoreApplication.translate("MainWindow", "Version")}: {proj.version}'
    phase_names = ",".join(proj.get_phase_by_index(i).name for i in proj.active_phases)
    usecase_names = ",".join(proj.get_usecase_by_index(i).name for i in proj.active_usecases)
    status = " | ".join([name, version, phase_names, usecase_names])
    main_window_tool.set_status_bar_text(status)
    main_window_tool.set_window_title(f"SOM-Toolkit v{som_gui.__version__}")


def toggle_console_clicked(main_window: Type[tool.MainWindow]):
    main_window.toggle_console()
    retranslate_ui(main_window)
