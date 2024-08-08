from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.tool.logging import Signaller


class LoggingProperties:
    log_path: str = None
    log_format = "%(asctime)s | %(levelname)6s | %(module_func)50s [%(lineno)04d] |  %(message)s"
    log_level = None
    custom_formatter = None
    ignore_texts = list()
    signaller: Signaller = None
