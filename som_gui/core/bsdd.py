from __future__ import annotations
from typing import TYPE_CHECKING, Type
from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QLineEdit
from PySide6.QtCore import Qt
if TYPE_CHECKING:
    from som_gui import tool


def open_window(bsdd: Type[tool.Bsdd]) -> None:
    window = bsdd.get_window()
    if not window:
        window = bsdd.create_window()
        bsdd.set_tabs(bsdd.get_tab_list())

    window.show()


def reset(bsdd: Type[tool.Bsdd]) -> None:
    bsdd.reset_dictionary()


def define_dictionary_widget(bsdd: Type[tool.Bsdd]):
    widget = bsdd.get_dictionary_widget()
    if not widget:
        widget = bsdd.create_dictionary_widget()
    bsdd.add_widget_to_toolbox("Dictionary", widget)


def paint_dictionary(bsdd: Type[tool.Bsdd], project: Type[tool.Project]):
    dictionary = bsdd.get_dictionary()
    if not dictionary:
        dictionary = bsdd.transform_project_to_dict(project.get())
    dict_widget = bsdd.get_dictionary_widget()
    layout: QFormLayout = dict_widget.layout()
    for row in range(layout.rowCount()):
        item = layout.itemAt(row * 2).widget()
        value = getattr(dictionary, item.property('attribute_name'))
        if isinstance(item, QLineEdit):
            item.setText(value)
        elif isinstance(item, QComboBox):
            item.setCurrentText(value)
        elif isinstance(item, QCheckBox):
            item.setChecked(value)


def dict_attribute_changed(value, widget, bsdd: Type[tool.Bsdd]):
    dictionary = bsdd.get_dictionary()
    attribute_name = widget.property('attribute_name')
    if not dictionary:
        return
    if isinstance(value, Qt.CheckState):
        value = True if value == Qt.CheckState.Checked else False
    setattr(dictionary, attribute_name, value)
