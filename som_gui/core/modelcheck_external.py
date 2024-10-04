from __future__ import annotations
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from som_gui import tool


def open_window(modelcheck_external: Type[tool.ModelcheckExternal], modelcheck_window: Type[tool.ModelcheckWindow]):
    window = modelcheck_external.create_window()
    modelcheck_window.get_properties().active_window = window
    modelcheck_external.create_menubar(window)
    window.show()


def close_window(modelcheck_external: Type[tool.ModelcheckExternal]):
    modelcheck_external.get_window().close()
    modelcheck_external.get_window().hide()
