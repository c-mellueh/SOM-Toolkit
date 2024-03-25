from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import ModelcheckExternalWindow
    from som_gui.module.modelcheck_window.ui import ObjectTree
    import SOMcreator
class ModelcheckExternalProperties():
    window: ModelcheckExternalWindow = None
