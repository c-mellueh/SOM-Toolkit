import som_gui.core.tool
from som_gui.module.ifc_importer import ui


class IfcImporter(som_gui.core.tool.IfcImporter):

    @classmethod
    def create_importer(cls):
        return ui.IfcImportWidget()
