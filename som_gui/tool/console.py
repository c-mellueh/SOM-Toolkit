from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import som_gui.core.tool
from som_gui.module.console import ui

if TYPE_CHECKING:
    from som_gui.module.console.prop import ConsoleProperties

class Console(som_gui.core.tool.Console):
    @classmethod
    def get_properties(cls) -> ConsoleProperties:
        return som_gui.ConsoleProperties

    @classmethod
    def create_console(cls):
        if cls.get_properties().console is None:
            console = ui.Console()
            console.show()
            console.eval_in_thread()
            cls.get_properties().console = console
        return cls.get_properties().console

    @classmethod
    def close_console(cls):
        logging.debug("Close Console")
        cls.get_properties().console = None
