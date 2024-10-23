from PySide6.QtWidgets import QDialog
from .qt.ui_DeleteRequest import Ui_DeleteRequest
from som_gui.ressources.icons import get_icon


class DeleteRequestDialog(QDialog):
    def __init__(self, ):
        super().__init__()
        self.widget = Ui_DeleteRequest()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
