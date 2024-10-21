from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QAction


class ExportProperties:
    settings_widget: QWidget = None
    actions: dict[str, QAction] = dict()
