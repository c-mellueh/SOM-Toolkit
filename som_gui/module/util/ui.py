from PySide6.QtWidgets import QWidget, QFileDialog
from .qt import file_selector, main_attribute_select, progressbar
from . import trigger


class FileSelector(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = file_selector.Ui_Form()
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


class MainAttributeSelector(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = main_attribute_select.Ui_Form()
        self.ui.setupUi(self)
        trigger.main_attribute_selector_created(self)


class Progressbar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = progressbar.Ui_Form()
        self.ui.setupUi(self)
