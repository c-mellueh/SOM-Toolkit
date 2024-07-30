from __future__ import annotations

import os.path
from typing import TYPE_CHECKING, Type
from som_gui.module.settings.paths import PATHS_SECTION
from som_gui.module.compare.prop import COMPARE_SETTING
from som_gui.module.project.constants import FILETYPE

from SOMcreator import Project

if TYPE_CHECKING:
    from som_gui import tool


def open_project_selection_window(compare: Type[tool.Compare], project_selector: Type[tool.CompareProjectSelector],
                                  settings: Type[tool.Settings],
                                  project: Type[tool.Project],
                                  popups: Type[tool.Popups]):
    if compare.get_window():
        if compare.get_window().exec():
            compare.delete_window()
        return
    compare.reset_properties()
    proj_select_dialog = project_selector.create_project_select_dialog()
    project_selector.connect_project_select_dialog(proj_select_dialog)

    path = settings.get_string_setting(PATHS_SECTION, COMPARE_SETTING)
    project_selector.fill_project_select_dialog(project.get(), path)

    if proj_select_dialog.exec():
        open_compare_window(compare, project_selector, project, settings, popups)


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
                           settings: Type[tool.Settings]):
    dialog = project_selector.get_project_select_dialog()
    path = settings.get_string_setting(PATHS_SECTION, COMPARE_SETTING)
    path = popups.get_path(FILETYPE, dialog, path)
    if not path:
        return
    project_selector.set_project_select_path(path)


def open_compare_window(compare: Type[tool.Compare], project_selector: Type[tool.CompareProjectSelector],
                        project: Type[tool.Project], settings: Type[tool.Settings],
                        popups: Type[tool.Popups]):
    window = compare.create_window()
    window.show()
    other_file_path = project_selector.get_project_select_path()
    if os.path.exists(other_file_path):
        settings.set_path(COMPARE_SETTING, other_file_path)
    else:
        popups.create_warning_popup(f"File {other_file_path} does not exist!")
        return

    project_0 = project.get()
    project_1 = Project.open(other_file_path)

    if not compare.get_properties().is_current_proj_input:
        project_0, project_1 = project_1, project_0

    compare.set_projects(project_0, project_1)
    compare.create_object_dicts()
    compare.fill_object_tree()

    root = compare.get_object_tree().invisibleRootItem()
    for child_index in range(root.childCount()):
        compare.style_tree_item(root.child(child_index))

    compare.set_header_labels(compare.get_header_name_from_project(project_0),
                              compare.get_header_name_from_project(project_1))
    compare.create_compare_window_triggers(window)
    window.hide()
    if window.exec():
        compare.delete_window()


def object_tree_selection_changed(compare: Type[tool.Compare]):
    obj = compare.get_selected_item_from_tree(compare.get_object_tree())
    compare.fill_pset_table(obj)
    root = compare.get_pset_tree().invisibleRootItem()

    for child_index in range(root.childCount()):
        compare.style_tree_item(root.child(child_index))


def pset_tree_selection_changed(compare: Type[tool.Compare]):
    attribute = compare.get_selected_item_from_tree(compare.get_pset_tree())
    compare.fill_value_table(attribute)
