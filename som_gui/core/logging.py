from __future__ import annotations
from typing import TYPE_CHECKING, Type
from PySide6.QtWidgets import QComboBox, QFormLayout, QLabel, QLineEdit
import logging

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.logging import ui
import os
import logging


def create_logger(logging_tool: Type[tool.Logging], util: Type[tool.Util], main_window: Type[tool.MainWindow]):

    log_dir_path = logging_tool.get_logging_directory()
    if not os.path.exists(log_dir_path):
        util.create_directory(log_dir_path)

    logger = logging_tool.get_logger()
    logger.setLevel(logging_tool.get_log_level())

    logging_tool.get_signaller()  # create signaller
    for handler in logger.handlers:
        logger.removeHandler(handler)

    logger.addHandler(logging_tool.create_console_handler())
    logger.addHandler(logging_tool.create_file_handler(logging_tool.get_logging_filename()))
    logger.addHandler(logging_tool.create_popup_handler(main_window.get()))  # creates Popup if Error/Warning is logged
    logging_tool.create_error_popup()  # creates Popup if error is raised


def settings_accepted(logging_tool: Type[tool.Logging]):
    log_levels: dict[str, int] = logging._nameToLevel
    widget = logging_tool.get_settings_widget()
    cb: QComboBox = widget.layout().itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
    level = log_levels[cb.currentText().upper()]
    logging_tool.set_log_level(level)

    path = widget.layout().itemAt(1, QFormLayout.ItemRole.FieldRole).widget().text()
    logging_tool.set_logging_directory(path)


def settings_widget_created(widget: ui.SettingsWidget, logging_tool: Type[tool.Logging]):
    layout: QFormLayout = widget.layout()
    logging_tool.set_settings_widget(widget)

    log_levels: dict[str, int] = logging._nameToLevel
    names = [l[0].title() for l in sorted(log_levels.items(), key=lambda x: x[1])]
    cb = QComboBox()
    cb.addItems(names)
    current_log_name = logging._levelToName[logging_tool.get_log_level()]
    cb.setCurrentText(current_log_name.title())
    layout.addRow(QLabel(f"LogLevel:"), cb)

    le = QLineEdit(logging_tool.get_logging_directory())
    layout.addRow(QLabel(f"Log Directory"), le)
