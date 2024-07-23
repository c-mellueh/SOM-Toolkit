from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
import os
import logging


def create_logger(logging_tool: Type[tool.Logging], util: Type[tool.Util]):
    log_dir_path = logging_tool.get_logging_directory()
    if not os.path.exists(log_dir_path):
        util.create_directory(log_dir_path)
    logger = logging_tool.get_logger()
    for handler in logger.handlers:
        logger.removeHandler(handler)
    if logging_tool.get_log_level() is None:
        logging_tool.set_log_level(logging.WARNING)
    console_handler = logging_tool.create_console_handler()
    file_handler = logging_tool.create_file_handler(logging_tool.get_logging_filename())
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
