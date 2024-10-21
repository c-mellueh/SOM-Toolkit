from PySide6.QtWidgets import QWidget, QFileDialog
from .qt import ui_FileSelector, ui_AttributeSelect, ui_Progressbar
from . import trigger


class FileSelector(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = ui_FileSelector.Ui_Form()
        self.ui.setupUi(self)
        self.request_folder = None
        self.extension = None
        self.name = None
        self.appdata_text = None
        self.request_save = None
        self.single_request = None
        self.ui.pushButton.clicked.connect(lambda: trigger.fileselector_clicked(self))

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.paint_file_selector(self)


class AttributeSelector(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = ui_AttributeSelect.Ui_Form()
        self.ui.setupUi(self)
        trigger.main_attribute_selector_created(self)


class Progressbar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = ui_Progressbar.Ui_Form()
        self.ui.setupUi(self)
