from __future__ import annotations
from typing import TYPE_CHECKING, Type
from som_gui.module.util.constants import PATH_SEPERATOR

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.util import ui


def filesector_clicked(widget: ui.FileSelector, util: Type[tool.Util]):
    paths = util.request_path(widget.name, widget.parent_widget, widget.extension, widget.appdata_text)
    if not paths:
        return
    paths_texts = PATH_SEPERATOR.join(paths)
    widget.ui.lineEdit.setText(paths_texts)
