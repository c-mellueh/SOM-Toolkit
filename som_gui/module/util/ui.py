from PySide6.QtWidgets import QWidget, QFileDialog
from .qt import file_selector
from . import trigger


class FileSelector(QWidget):
    def __init__(self, name, extension, parent_widget, appdata_text=None, request_folder=False):
        super().__init__()
        self.ui = file_selector.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(name)
        self.parent_widget = parent_widget
        self.request_folder = request_folder
        self.extension = extension
        self.name = name
        self.appdata_text = appdata_text
        self.ui.pushButton.clicked.connect(lambda: trigger.fileselector_clicked(self))
