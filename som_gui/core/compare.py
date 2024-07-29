from __future__ import annotations

import os.path
from typing import TYPE_CHECKING, Type
from som_gui.module.settings.paths import PATHS_SECTION
from som_gui.module.compare.prop import COMPARE_SETTING
from som_gui.module.project.constants import FILETYPE

from SOMcreator import Project

if TYPE_CHECKING:
    from som_gui import tool


def open_project_selection_window(compare: Type[tool.Compare], settings: Type[tool.Settings],
                                  project: Type[tool.Project],
                                  popups: Type[tool.Popups]):
    import_dialog = compare.create_import_dialog()
    project_path = settings.get_string_setting(PATHS_SECTION, COMPARE_SETTING)
    compare.set_import_dialog_lineedit(project_path)
    import_dialog.widget.label_project.setText(compare.header_name(project.get()))

    if import_dialog.exec_():
        open_compare_window(compare, project, settings, popups)


def switch_clicked(compare: Type[tool.Compare]):
    layout0, layout1 = compare.get_project_layouts()
    input_layout = compare.get_input_layout()
    project_label = compare.get_project_label()

    if compare.is_current_project_input():
        layout0.removeWidget(project_label)
        layout1.removeItem(input_layout)
        layout0.addItem(input_layout)
        layout1.addWidget(project_label)
    else:
        layout0.removeItem(input_layout)
        layout1.removeWidget(project_label)
        layout0.addWidget(project_label)
        layout1.addItem(input_layout)
    compare.toggle_current_project_as_input()


def project_button_clicked(compare: Type[tool.Compare], popups: Type[tool.Popups], settings: Type[tool.Settings]):
    dialog = compare.get_import_dialog()
    path = settings.get_string_setting(PATHS_SECTION, COMPARE_SETTING)
    path = popups.get_path(FILETYPE, dialog, path)
    if not path:
        return
    compare.set_import_dialog_lineedit(path)


def open_compare_window(compare: Type[tool.Compare], project: Type[tool.Project], settings: Type[tool.Settings],
                        popups: Type[tool.Popups]):
    window = compare.create_window()
    window.show()
    other_file_path = compare.get_import_dialog().widget.line_edit.text()
    if os.path.exists(other_file_path):
        settings.set_path(COMPARE_SETTING, other_file_path)
    else:
        popups.create_warning_popup(f"File {other_file_path} does not exist!")
        return

    project_0 = project.get()
    project_1 = Project.open(other_file_path)

    if not compare.get_properties().current_project_as_input:
        project_0, project_1 = project_1, project_0

    compare.set_projects(project_0, project_1)
    compare.create_object_dicts()
    compare.fill_object_tree()

    root = compare.get_object_tree().invisibleRootItem()
    for child_index in range(root.childCount()):
        compare.style_object_tree_item(root.child(child_index))

    compare.set_header_labels(compare.header_name(project_0), compare.header_name(project_1))
    compare.create_triggers(window)
    window.exec()


def object_tree_selection_changed(compare: Type[tool.Compare]):
    obj = compare.get_selected_object()
    compare.fill_pset_table(obj)
    root = compare.get_pset_tree().invisibleRootItem()

    for child_index in range(root.childCount()):
        compare.style_object_tree_item(root.child(child_index))


def pset_tree_selection_changed(compare: Type[tool.Compare]):
    attribute = compare.get_selected_pset()
    compare.fill_value_table(attribute)
