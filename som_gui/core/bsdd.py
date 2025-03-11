from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QLineEdit
from som_gui.module.bsdd.constants import OPEN_WINDOW_ACTION, FILE_FORMAT, BSDD_PATH

if TYPE_CHECKING:
    from som_gui import tool


def create_main_menu_actions(
    bsdd: Type[tool.Bsdd], main_window: Type[tool.MainWindow]
) -> None:
    """
    add Bsdd menu entry
    :return:
    """
    open_window_action = main_window.add_action(
        "menuExport", "BSDD", bsdd.get_open_window_trigger()
    )
    bsdd.set_action(OPEN_WINDOW_ACTION, open_window_action)


def retranslate_ui(bsdd: Type[tool.Bsdd], util: Type[tool.Util]) -> None:
    """
    retranslate UI
    """
    open_window_action = bsdd.get_action(OPEN_WINDOW_ACTION)
    title = QCoreApplication.translate("BSDD", "bsDD")
    open_window_action.setText(title)

    # translate window if existing
    window = bsdd.get_window()
    if window:
        window.ui.retranslateUi(window)
        window.setWindowTitle(util.get_window_title(title))


def open_window(bsdd: Type[tool.Bsdd], appdata: Type[tool.Appdata]) -> None:
    """
    Open bsDD Settings/Export Window
    """
    # create window if not existing
    window = bsdd.get_window()
    if not window:
        window = bsdd.create_window()
        bsdd_export_path = appdata.get_path(BSDD_PATH)
        bsdd.get_path_line_edit().setText(bsdd_export_path)
        bsdd.set_tabs(bsdd.get_tab_list())  # create Tabs of bsdd Widget

    # update Texts
    bsdd.trigger_retranslation()
    window.show()
    window.activateWindow()


def reset(bsdd: Type[tool.Bsdd]) -> None:
    """
    reset Dictionary so it is empty again
    :param bsdd:
    :return:
    """
    bsdd.reset_dictionary()


def define_dictionary_widget(bsdd: Type[tool.Bsdd]):
    """
    Create Widget for Dictionary Class
    """
    widget = bsdd.get_dictionary_widget()
    if not widget:
        widget = bsdd.create_dictionary_widget()
    bsdd.add_widget_to_toolbox(QCoreApplication.translate("BSDD", "Dictionary"), widget)


def update_dictionary(bsdd: Type[tool.Bsdd], project: Type[tool.Project]):
    """
    update Dictionary entries based on defined variables
    """
    if bsdd.is_update_blocked():
        return
    logging.debug("update Dictionary")
    dictionary = bsdd.get_dictionary()
    if not dictionary:
        dictionary = bsdd.transform_project_to_dict(project.get())
    layout: QFormLayout = bsdd.get_dictionary_widget().layout()
    for row in range(layout.rowCount()):
        item = layout.itemAt(
            row * 2
        ).widget()  # get Value Widget "*2" is needed because QFormLayout item handling
        value = getattr(dictionary, bsdd.get_linked_property_name(item))
        if isinstance(item, QLineEdit):
            item.setText(value or "")
        elif isinstance(item, QComboBox):
            item.setCurrentText(value or "")
        elif isinstance(item, QCheckBox):
            item.setChecked(value)


def update_dictionary_property(
    value, property_name: str, bsdd: Type[tool.Bsdd]
) -> None:
    """
    update Dictionary properties based on new value set in UI
    :param value: new Value
    :param property_name: name of the Property of the Dictionary which will be updated
    :param bsdd:
    :return:
    """
    logging.debug(f"Update Property '{property_name}' -> {value}")
    dictionary = bsdd.get_dictionary()
    if not dictionary:
        return
    if isinstance(value, Qt.CheckState):
        value = True if value == Qt.CheckState.Checked else False
    setattr(dictionary, property_name, value)


def open_export_path_popup(
    bsdd: Type[tool.Bsdd], popups: Type[tool.Popups], appdata: Type[tool.Appdata]
):
    """
    Open Popup which requests the save_path of the BSDD. Writes the Path into the export lineEdit and Appdata
    :param bsdd:
    :param popups:
    :param appdata:
    :return:
    """
    path = appdata.get_path(BSDD_PATH)
    window = bsdd.get_window()
    title = QCoreApplication.translate("BSDD", "bsDD JSON Export")
    path = popups.get_save_path(FILE_FORMAT, window, path, title)
    if not path:
        return
    appdata.set_path(BSDD_PATH, path)
    bsdd.get_path_line_edit().setText(path)


def export_dictionary(
    bsdd: Type[tool.Bsdd], project: Type[tool.Project], popups: Type[tool.Popups]
):
    """
    starts Exporter. Uses Path and Data defined in UI
    :return:
    """
    path = bsdd.get_export_path()
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        text = QCoreApplication.translate("BSDD", "folder '{}' does not exist")
        logging.error(text.format(dirname))
        return

    bsdd.reset_classes()
    bsdd.reset_properties()
    bsdd.add_classes_to_dictionary(project.get())
    bsdd.export_to_json(path)
    text = QCoreApplication.translate("BSDD", "Export Done!")
    popups.create_info_popup(text, text)
