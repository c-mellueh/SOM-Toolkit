from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from som_gui.module.util.constants import PATH_SEPERATOR

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.util import ui


def filesector_clicked(widget: ui.FileSelector, util: Type[tool.Util]):
    logging.debug(f"filerequest clicked")
    paths = util.request_path(widget)
    if not paths:
        return
    paths_texts = PATH_SEPERATOR.join(paths)
    widget.ui.lineEdit.setText(paths_texts)


def update_file_selector(widget: ui.FileSelector):
    if widget.name:
        widget.ui.label.show()
        widget.ui.label.setText(widget.name)
    else:
        widget.ui.label.hide()


def fill_main_attribute_selector(
    widget: ui.PropertySelector, util: Type[tool.Util], project: Type[tool.Project]
):
    pset, attribute = project.get().get_main_property()
    util.fill_main_attribute(widget, pset, attribute)
