from __future__ import annotations
import os
import logging
from typing import TYPE_CHECKING, Type
from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QLineEdit
from PySide6.QtCore import Qt, QCoreApplication
if TYPE_CHECKING:
    from som_gui import tool

BSDD_PATH = "../../SOMcreator/exporter/bsdd"


def create_main_menu_actions(bsdd: Type[tool.Bsdd], main_window: Type[tool.MainWindow]):
    from som_gui.module.bsdd import trigger
    open_window_action = main_window.add_action2("menuExport", "BSDD", trigger.open_window)
    bsdd.set_action("open_window", open_window_action)


def retranslate_ui(bsdd: Type[tool.Bsdd], util:Type[tool.Util]):
    open_window_action = bsdd.get_action("open_window")
    title = QCoreApplication.translate("BSDD", "bsDD")
    open_window_action.setText(title)
    window = bsdd.get_window()
    if window:
        window.ui.retranslateUi(window)
        window.setWindowTitle(util.get_window_title(title))

def open_window(bsdd: Type[tool.Bsdd], settings: Type[tool.Appdata]) -> None:
    window = bsdd.get_window()
    if not window:
        window = bsdd.create_window()
        bsdd.get_path_line_edit().setText(settings.get_path(BSDD_PATH))
        bsdd.set_tabs(bsdd.get_tab_list())
    from som_gui.module.bsdd import trigger
    trigger.retranslate_ui()
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
            item.setText(value or "")
        elif isinstance(item, QComboBox):
            item.setCurrentText(value or "")
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


def export_path_requested(bsdd: Type[tool.Bsdd], popups: Type[tool.Popups], appdata: Type[tool.Appdata]):
    path = appdata.get_path(BSDD_PATH)
    window = bsdd.get_window()
    path = popups.get_save_path("JSON (*.json);;", window, path, "bsDD Json Export")
    if not path:
        return
    appdata.set_path(BSDD_PATH, path)
    bsdd.get_path_line_edit().setText(path)


def export_dictionary(bsdd: Type[tool.Bsdd], project: Type[tool.Project], popups: Type[tool.Popups]):
    path = bsdd.get_path_line_edit().text()
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        logging.error(f"folder '{dirname}' does not exist")
        return

    bsdd.add_objects_to_dictionary(project.get())
    bsdd.export_to_json(path)
    popups.create_info_popup("Export Abgeschlossen", "Export ist abgeschlossen")
