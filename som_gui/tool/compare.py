from __future__ import annotations

from typing import Callable, TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon

import som_gui
import som_gui.core.tool
from som_gui.module.compare import trigger
from som_gui.module.compare import ui

if TYPE_CHECKING:
    from som_gui.module.compare.prop import (
        CompareWindowProperties,
        CompareProjectSelectProperties,
    )


class CompareProjectSelector(som_gui.core.tool.CompareProjectSelector):
    @classmethod
    def get_properties(cls) -> CompareProjectSelectProperties:
        return som_gui.CompareProjectSelectProperties

    @classmethod
    def create_project_select_dialog(cls):
        dialog = ui.ProjectSelectDialog()
        cls.get_properties().proj_select_dialog = dialog
        cls.get_properties().layout_proj0 = dialog.widget.layout_top
        cls.get_properties().layout_proj1 = dialog.widget.layout_bottom
        cls.get_properties().label_project = dialog.widget.label_project
        cls.get_properties().layout_input = dialog.widget.layout_input
        return dialog

    @classmethod
    def get_project_select_dialog(cls) -> ui.ProjectSelectDialog:
        return cls.get_properties().proj_select_dialog

    @classmethod
    def connect_project_select_dialog(cls, dialog: ui.ProjectSelectDialog):
        dialog.widget.button.clicked.connect(trigger.project_button_clicked)
        dialog.widget.button_switch.clicked.connect(trigger.switch_button_clicked)

    @classmethod
    def fill_project_select_dialog(cls, project, open_path):
        cls.set_project_select_path(open_path)
        name = f"{project.name} v{project.version}"
        cls.get_properties().label_project.setText(name)

    @classmethod
    def get_project_layouts(cls):
        prop = cls.get_properties()
        return prop.layout_proj0, prop.layout_proj1

    @classmethod
    def get_input_layout(cls):
        return cls.get_properties().layout_input

    @classmethod
    def get_project_label(cls):
        return cls.get_properties().label_project

    @classmethod
    def toggle_current_project_as_input(cls):
        prop = cls.get_properties()
        prop.is_current_proj_input = not prop.is_current_proj_input

    @classmethod
    def is_current_project_input(cls):
        return cls.get_properties().is_current_proj_input

    @classmethod
    def set_project_select_path(cls, project_path: str):
        cls.get_project_select_dialog().widget.line_edit.setText(project_path)

    @classmethod
    def get_project_select_path(cls) -> str:
        return cls.get_project_select_dialog().widget.line_edit.text()

    @classmethod
    def accept_clicked(cls):
        trigger.accept_clicked()


class CompareWindow(som_gui.core.tool.CompareWindow):
    @classmethod
    def get_properties(cls) -> CompareWindowProperties:
        return som_gui.CompareWindowProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

    @classmethod
    def connect_triggers(cls):
        window = cls.get_window()
        window.widget.button_download.clicked.connect(trigger.download_clicked)

    @classmethod
    def add_tab(cls, name_getter: Callable, widget, init_func, _tool, export_func):
        prop = cls.get_properties()
        prop.name_getter.append(name_getter)
        prop.widgets.append(widget)
        prop.init_functions.append(init_func)
        prop.tools.append(_tool)
        prop.export_funcs.append(export_func)

    @classmethod
    def get_export_functions(cls) -> list[Callable]:
        return cls.get_properties().export_funcs

    @classmethod
    def create_window(cls):
        cls.get_properties().window = ui.CompareDialog()
        return cls.get_window()

    @classmethod
    def get_window(cls) -> ui.CompareDialog:
        return cls.get_properties().window

    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_tabwidget(cls):
        return cls.get_window().widget.tabWidget

    @classmethod
    def init_tabs(cls, project0, project1):
        names = cls.get_properties().name_getter
        widgets = cls.get_properties().widgets
        init_functions = cls.get_properties().init_functions
        tab_widget = cls.get_tabwidget()
        for name_getter, widget_getter, init_func in zip(
            names, widgets, init_functions
        ):
            tab_widget.addTab(widget_getter(), QIcon(), name_getter())
            init_func(project0, project1)

    @classmethod
    def reset(cls):
        prop = cls.get_properties()
        prop.window = None
        for _tool in cls.get_properties().tools:
            _tool.reset()
