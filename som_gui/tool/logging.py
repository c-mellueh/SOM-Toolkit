from __future__ import annotations

from typing import TYPE_CHECKING
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMessageBox, QCheckBox
import appdirs
import sys
import som_gui.core.tool
import os
import som_gui
import datetime
import logging
import traceback

if TYPE_CHECKING:
    from som_gui.module.logging.prop import LoggingProperties
from som_gui.icons import get_icon
from som_gui import tool


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record: logging.LogRecord):
        # Combine module and function name
        path_name = record.pathname.split("\\")[-2]
        module_func = f"{path_name}.{record.module}.{record.funcName}"
        # Ensure the combined string is 50 characters long
        if len(module_func) > 50:
            module_func = module_func[:47] + '...'
        else:
            module_func = module_func.ljust(50)

        # Set the custom attribute
        record.module_func = module_func

        return super().format(record)


class Signaller(QObject):
    error = Signal(int, str, str)


class PopupHandler(logging.Handler):
    error_sigal = Signal()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.signaller = tool.Logging.get_signaller()

    def emit(self, record):
        if record.levelno >= logging.WARNING:
            msg = self.format(record)
            print(record.levelno, msg, record.message)
            self.signaller.error.emit(record.levelno, msg, record.message)


class Logging(som_gui.core.tool.Logging):

    @classmethod
    def show_popup(cls, level_no, message, base_message=None):
        if base_message is None:
            base_message = message
        if base_message in cls.get_properties().ignore_texts:
            return
        msg_box = QMessageBox()
        states = [
            (QMessageBox.Icon.Information, "Information"),
            (QMessageBox.Icon.Warning, "Warning"),
            (QMessageBox.Icon.Critical, "Error"),
        ]
        icon, level = states[0] if level_no < logging.WARNING else states[1] if level_no < logging.ERROR else states[2]
        msg_box.setIcon(icon)
        cb = QCheckBox("nicht erneut anzeigen")
        msg_box.setCheckBox(cb)
        msg_box.setWindowIcon(get_icon())
        msg_box.setWindowTitle(f"{level}")
        msg_box.setText(f"An {level} occurred:")
        msg_box.setDetailedText(message)
        if msg_box.exec_() and cb.isChecked():
            cls.get_properties().ignore_texts.append(base_message)

    @classmethod
    def get_properties(cls) -> LoggingProperties:
        return som_gui.LoggingProperties

    @classmethod
    def get_signaller(cls):
        if cls.get_properties().signaller is None:
            cls.get_properties().signaller = Signaller()
            cls.get_properties().signaller.error.connect(cls.show_popup)
        return cls.get_properties().signaller

    @classmethod
    def get_log_level(cls):
        return cls.get_properties().log_level

    @classmethod
    def set_log_level(cls, log_level):
        cls.get_properties().log_level = log_level
        cls.get_logger().setLevel(log_level)
        for handler in cls.get_logger().handlers:
            handler.setLevel(log_level)

    @classmethod
    def get_logger(cls):
        return logging.getLogger()

    @classmethod
    def get_logging_directory(cls):
        return appdirs.user_log_dir(som_gui.__name__)

    @classmethod
    def get_logging_filename(cls):
        if cls.get_properties().log_path is None:
            dir_path = cls.get_logging_directory()
            file_name = f"{datetime.datetime.utcnow()}.log"
            file_name = file_name.replace(":", "_")
            file_name = file_name.replace(" ", "_")
            logpath = os.path.join(dir_path, file_name)

            cls.get_properties().log_path = logpath
        return cls.get_properties().log_path

    @classmethod
    def create_console_handler(cls):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(cls.get_log_level())
        console_handler.setFormatter(cls.get_custom_formatter())
        return console_handler

    @classmethod
    def create_file_handler(cls, path):
        path = path.replace("\\", "/")
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(cls.get_log_level())
        file_handler.setFormatter(cls.get_custom_formatter())
        return file_handler

    @classmethod
    def get_custom_formatter(cls) -> CustomFormatter:
        if cls.get_properties().custom_formatter is None:
            log_format = cls.get_properties().log_format
            cls.get_properties().custom_formatter = CustomFormatter(log_format)
        return cls.get_properties().custom_formatter

    @classmethod
    def create_popup_handler(cls, main_window):
        popup_handler = PopupHandler(main_window)

        popup_handler.setLevel(cls.get_log_level())
        popup_handler.setFormatter(cls.get_custom_formatter())
        return popup_handler

    @classmethod
    def create_error_popup(cls):
        sys.excepthook = cls.show_exception_popup

    @classmethod
    def show_exception_popup(cls, exctype, value, tb):
        error_message = ''.join(traceback.format_exception(exctype, value, tb))
        cls.get_signaller().error.emit(logging.ERROR, error_message, error_message)
        print(error_message)
