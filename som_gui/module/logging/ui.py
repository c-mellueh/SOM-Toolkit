from PySide6.QtWidgets import QFormLayout, QWidget
from som_gui.module import logging


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QFormLayout())
        logging.trigger.settings_widget_created(self)
