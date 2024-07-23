from PySide6.QtWidgets import QDialog
from .ui_delete_request import Ui_Dialog
from som_gui.icons import get_icon


class DeleteRequestDialog(QDialog):
    def __init__(self, ):
        super().__init__()
        self.widget = Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
