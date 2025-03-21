from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel

from som_gui.resources.icons import get_icon
from .qt.ui_DeleteRequest import Ui_DeleteRequest


class DeleteRequestDialog(QDialog):
    def __init__(
        self,
    ):
        super().__init__()
        self.widget = Ui_DeleteRequest()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())


class CompleterDialog(QDialog):
    def __init__(self, parent, title, request_text, prefill="", completer=None):
        super().__init__(parent)
        self.setWindowTitle("Input Dialog with Completer")

        layout = QVBoxLayout(self)
        self.setWindowTitle(title)
        self.line_edit = QLineEdit(self)
        if completer:
            self.line_edit.setCompleter(completer)
        self.line_edit.setText(prefill)
        layout.addWidget(QLabel(request_text))
        layout.addWidget(self.line_edit)
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def getText(self):
        return self.line_edit.text()
