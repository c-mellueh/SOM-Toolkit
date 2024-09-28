from PySide6.QtWidgets import QWidget
from som_gui.module import plugins


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        plugins.trigger.settings_widget_created(self)
