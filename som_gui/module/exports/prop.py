from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget


class ExportProperties:
    settings_widget: QWidget = None
    actions: dict[str, QAction] = dict()
