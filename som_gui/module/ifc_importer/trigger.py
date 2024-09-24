from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import IfcImportWidget

from som_gui.core import ifc_importer as core
from som_gui import tool
def connect():
    pass


def connect_new_importer(import_widget: IfcImportWidget):
    line_edit = import_widget.widget.line_edit_ifc
    import_widget.widget.button_ifc.clicked.connect(
        lambda: core.ifc_file_dialog_clicked(line_edit, tool.Appdata, tool.IfcImporter))

def on_new_project():
    pass
