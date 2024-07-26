from PySide6.QtWidgets import QDialog
from .window import Ui_Dialog
from som_gui.icons import get_icon


class CompareDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr("Projekte Vergleichen"))

        self.widget.tree_widget_object.setColumnCount(4)
        self.widget.tree_widget_propertysets.setColumnCount(2)
        self.widget.table_widget_values.setColumnCount(2)
