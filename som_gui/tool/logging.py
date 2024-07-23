from __future__ import annotations
from typing import TYPE_CHECKING

import appdirs

import som_gui.core.tool
import os
import som_gui
import datetime
import logging

if TYPE_CHECKING:
    from som_gui.module.logging.prop import LoggingProperties


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
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


class Logging(som_gui.core.tool.Logging):
    @classmethod
    def get_properties(cls) -> LoggingProperties:
        return som_gui.LoggingProperties

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
