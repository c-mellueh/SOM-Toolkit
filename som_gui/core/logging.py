from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
import os
import logging


def create_logger(logging_tool: Type[tool.Logging], util: Type[tool.Util], main_window: Type[tool.MainWindow]):
    log_dir_path = logging_tool.get_logging_directory()
    if not os.path.exists(log_dir_path):
        util.create_directory(log_dir_path)
    logger = logging_tool.get_logger()
    signaller = logging_tool.get_signaller()  # create signaller
    for handler in logger.handlers:
        logger.removeHandler(handler)
    if logging_tool.get_log_level() is None:
        logging_tool.set_log_level(logging.WARNING)
    console_handler = logging_tool.create_console_handler()
    file_handler = logging_tool.create_file_handler(logging_tool.get_logging_filename())
    popup_handler = logging_tool.create_popup_handler(main_window.get())  # creates Popup if Error/Warning is logged
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(popup_handler)
    logging_tool.create_error_popup()  # creates Popup if error is raised
