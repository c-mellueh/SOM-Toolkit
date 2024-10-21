from PySide6.QtWidgets import QFormLayout, QWidget
from som_gui.module import logging


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        from .qt.ui_Widget import Ui_Logging
        self.ui = Ui_Logging()
        self.ui.setupUi(self)
        logging.trigger.settings_widget_created(self)
