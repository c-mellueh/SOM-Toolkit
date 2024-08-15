from __future__ import annotations
import os.path
from typing import TYPE_CHECKING, Type
from som_gui.module.compare.constants import COMPARE_SETTING, EXPORT_PATH
import SOMcreator
from PySide6.QtCore import Qt
from som_gui.module.settings.paths import PATHS_SECTION
from som_gui.module.project.constants import FILETYPE

from SOMcreator import Project

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.compare import ui
    from PySide6.QtCore import QModelIndex
    from PySide6.QtGui import QPainter
    from PySide6.QtWidgets import QTreeWidget


def open_project_selection_window(compare_window: Type[tool.CompareWindow],
                                  project_selector: Type[tool.CompareProjectSelector],
                                  settings: Type[tool.Settings],
                                  project: Type[tool.Project], ):
    window = compare_window.get_window()
    if window is not None:
        if window.exec():
            compare_window.reset()
        return

    proj_select_dialog = project_selector.create_project_select_dialog()
    project_selector.connect_project_select_dialog(proj_select_dialog)

    path = settings.get_string_setting(PATHS_SECTION, COMPARE_SETTING)
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
                           settings: Type[tool.Settings]):
    dialog = project_selector.get_project_select_dialog()
    path = settings.get_string_setting(PATHS_SECTION, COMPARE_SETTING)
    path = popups.get_open_path(FILETYPE, dialog, path)
    if not path:
        return
    project_selector.set_project_select_path(path)


def open_compare_window(compare_window: Type[tool.CompareWindow], project_selector: Type[tool.CompareProjectSelector],
                        project: Type[tool.Project], settings: Type[tool.Settings],
                        popups: Type[tool.Popups]):
    other_file_path = project_selector.get_project_select_path()
    if not os.path.exists(other_file_path):
        popups.create_warning_popup(f"File {other_file_path} does not exist!")
        return

    window = compare_window.create_window()
    compare_window.connect_triggers()

    settings.set_path(COMPARE_SETTING, other_file_path)
    project_0 = project.get()
    project_1 = Project.open(other_file_path)

    if not project_selector.is_current_project_input():
        project_0, project_1 = project_1, project_0

    compare_window.set_projects(project_0, project_1)

    compare_window.init_tabs(project_0, project_1)

    if window.exec():
        compare_window.reset()


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


def object_tree_selection_changed(widget: ui.AttributeWidget,
                                  attribute_compare: Type[tool.AttributeCompare]):
    obj = attribute_compare.get_selected_entity(attribute_compare.get_object_tree(widget))
    tree = attribute_compare.get_pset_tree(widget)
    attribute_compare.fill_pset_tree(tree, obj, add_missing=True)
    root = attribute_compare.get_pset_tree(widget).invisibleRootItem()
    for child_index in range(root.childCount()):
        attribute_compare.style_tree_item(root.child(child_index))


def pset_tree_selection_changed(widget: ui.AttributeWidget, attribute_compare: Type[tool.AttributeCompare]):
    attribute = attribute_compare.get_selected_entity(attribute_compare.get_pset_tree(widget))
    attribute_compare.fill_value_table(attribute_compare.get_value_table(widget), attribute)


def add_attribute_compare_widget(attribute_compare: Type[tool.AttributeCompare],
                                 compare_window: Type[tool.CompareWindow]):
    compare_window.add_tab("Attributes", attribute_compare.get_widget,
                           lambda p0, p1: init_attribute_compare(p0, p1, attribute_compare),
                           attribute_compare, lambda file: export_attribute_differences(file, attribute_compare))


def export_attribute_differences(file, attribute_compare: Type[tool.AttributeCompare]):
    objects0: list[SOMcreator.Object] = attribute_compare.get_missing_objects(0)
    objects1: list[SOMcreator.Object] = attribute_compare.get_missing_objects(1)
    file.write("\nATTRIBUTE COMPARISON\n\n")

    for obj in sorted(objects0, key=lambda x: x.name):
        file.write(f"{obj.name} ({obj.ident_value}) was deleted\n")

    for obj in sorted(objects1, key=lambda x: x.name):
        file.write(f"{obj.name} ({obj.ident_value}) was added\n")

    if objects0 or objects1:
        file.write("\n\n")

    attribute_compare.export_object_differences(file)


def init_attribute_compare(project0, project1, attribute_compare: Type[tool.AttributeCompare]):
    attribute_compare.set_projects(project0, project1)
    attribute_compare.create_object_lists()
    widget = attribute_compare.get_widget()
    object_tree_widget = attribute_compare.get_object_tree(widget)
    pset_tree = attribute_compare.get_pset_tree(widget)
    value_table = attribute_compare.get_value_table(widget)

    attribute_compare.fill_object_tree(object_tree_widget, add_missing=True)
    root = object_tree_widget.invisibleRootItem()
    for child_index in range(root.childCount()):
        attribute_compare.style_tree_item(root.child(child_index))

    header_labels = [attribute_compare.get_header_name_from_project(project0),
                     attribute_compare.get_header_name_from_project(project1)]
    attribute_compare.set_header_labels(object_tree_widget, pset_tree, value_table, header_labels)
    attribute_compare.create_tree_selection_trigger(widget)


def download_changelog(compare_window: Type[tool.CompareWindow], popups: Type[tool.Popups],
                       settings: Type[tool.Settings]):
    path = settings.get_path(EXPORT_PATH)
    path = popups.get_save_path("txt Files (*.txt);;", compare_window.get_window(), path)
    if not path:
        return
    settings.set_path(EXPORT_PATH, path)
    with open(path, "w") as file:
        for func in compare_window.get_export_functions():
            file.write(f'{"**" * 75}\n{"**" * 75}\n')
            func(file)
