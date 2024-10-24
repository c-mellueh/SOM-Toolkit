from PySide6.QtWidgets import QDialog

from som_gui.resources.icons import get_icon
from .qt.ui_DeleteRequest import Ui_DeleteRequest


class DeleteRequestDialog(QDialog):
    def __init__(self, ):
        super().__init__()
        self.widget = Ui_DeleteRequest()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
