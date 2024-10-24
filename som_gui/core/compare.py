from __future__ import annotations
import os.path
from typing import TYPE_CHECKING, Type
from som_gui.module.compare.constants import COMPARE_SETTING, EXPORT_PATH
import SOMcreator
from PySide6.QtCore import Qt, QCoreApplication
from som_gui.module.project.constants import FILETYPE

from SOMcreator import Project

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.compare import ui
    from PySide6.QtCore import QModelIndex
    from PySide6.QtGui import QPainter
    from PySide6.QtWidgets import QTreeWidget


def create_main_menu_actions(compare_window: Type[tool.CompareWindow], main_window: Type[tool.MainWindow]):
    from som_gui.module.compare import trigger
    open_window_action = main_window.add_action("menuFile", "Compare", trigger.open_window)
    compare_window.set_action("open_window", open_window_action)


def retranslate_ui(compare_window: Type[tool.CompareWindow],util:Type[tool.Util] ):
    title = QCoreApplication.translate("CompareWindow", "Compare Projects")
    open_window_action = compare_window.get_action("open_window")
    open_window_action.setText(title)
    window = compare_window.get_window()
    if not window:
        return
    window.setWindowTitle(util.get_window_title(title))

    tab_widget = compare_window.get_tabwidget()
    names = [ng() for ng in compare_window.get_properties().name_getter]
    for name,i in zip(names,range(tab_widget.count())):
        tab_widget.setTabText(i,name)

def open_project_selection_window(compare_window: Type[tool.CompareWindow],
                                  project_selector: Type[tool.CompareProjectSelector],
                                  appdata: Type[tool.Appdata],
                                  project: Type[tool.Project], ):
    window = compare_window.get_window()
    if window is not None:
        if window.exec():
            compare_window.reset()
        return

    proj_select_dialog = project_selector.create_project_select_dialog()
    project_selector.connect_project_select_dialog(proj_select_dialog)

    path = appdata.get_path(COMPARE_SETTING)
    project_selector.fill_project_select_dialog(project.get(), path)

    if proj_select_dialog.exec():
        project_selector.accept_clicked()


def switch_clicked(project_selector: Type[tool.CompareProjectSelector]):
    layout0, layout1 = project_selector.get_project_layouts()
    input_layout = project_selector.get_input_layout()
    project_label = project_selector.get_project_label()

    if project_selector.is_current_project_input():
        layout0.removeWidget(project_label)
        layout1.removeItem(input_layout)
        layout0.addItem(input_layout)
        layout1.addWidget(project_label)
    else:
        layout0.removeItem(input_layout)
        layout1.removeWidget(project_label)
        layout0.addWidget(project_label)
        layout1.addItem(input_layout)
    project_selector.toggle_current_project_as_input()


def project_button_clicked(project_selector: Type[tool.CompareProjectSelector], popups: Type[tool.Popups],
                           appdata: Type[tool.Appdata]):
    dialog = project_selector.get_project_select_dialog()
    path = appdata.get_path(COMPARE_SETTING)
    path = popups.get_open_path(FILETYPE, dialog, path)
    if not path:
        return
    project_selector.set_project_select_path(path)


def open_compare_window(compare_window: Type[tool.CompareWindow], project_selector: Type[tool.CompareProjectSelector],
                        project: Type[tool.Project], appdata: Type[tool.Appdata],
                        popups: Type[tool.Popups]):
    other_file_path = project_selector.get_project_select_path()
    if not os.path.exists(other_file_path):
        warning = QCoreApplication.translate("Compare","File '{}' doesn't exist").format(other_file_path)
        popups.create_warning_popup(warning)
        return

    window = compare_window.create_window()

    compare_window.connect_triggers()

    appdata.set_path(COMPARE_SETTING, other_file_path)
    project_0 = project.get()
    project_1 = Project.open(other_file_path)

    if not project_selector.is_current_project_input():
        project_0, project_1 = project_1, project_0

    compare_window.set_projects(project_0, project_1)

    compare_window.init_tabs(project_0, project_1)
    window.show()
    window.raise_()
    window.activateWindow()
    window.accepted.connect(compare_window.reset)

def draw_tree_branch(tree: QTreeWidget, painter: QPainter, rect, index: QModelIndex,
                     attribute_compare: Type[tool.AttributeCompare]):
    level = attribute_compare.get_level(index)
    item = tree.itemFromIndex(index)

    width = rect.width()
    arrow_width = width / level
    start_point = width - arrow_width
    color = attribute_compare.get_branch_color(index)

    if item.childCount() and color is not None:
        painter.setBackground(Qt.GlobalColor.red)
        painter.setBrush(color)
        painter.setPen(Qt.GlobalColor.transparent)
        rect.setRect(start_point, rect.y(), arrow_width, rect.height())
        painter.drawRect(rect)
    return painter, rect, index





def download_changelog(compare_window: Type[tool.CompareWindow], popups: Type[tool.Popups],
                       appdata: Type[tool.Appdata]):
    path = appdata.get_path(EXPORT_PATH)
    path = popups.get_save_path("txt Files (*.txt);;", compare_window.get_window(), path)
    if not path:
        return
    appdata.set_path(EXPORT_PATH, path)
    with open(path, "w") as file:
        for func in compare_window.get_export_functions():
            file.write(f'{"**" * 75}\n{"**" * 75}\n')
            func(file)
