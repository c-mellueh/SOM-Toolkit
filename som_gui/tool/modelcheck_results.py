from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import som_gui

if TYPE_CHECKING:
    from som_gui.module.modelcheck_results.prop import ModelcheckResultProperties


class ModelcheckResults(som_gui.core.tool.ModelcheckResults):
    @classmethod
    def get_properties(cls) -> ModelcheckResultProperties:
        return som_gui.ModelcheckResultProperties
