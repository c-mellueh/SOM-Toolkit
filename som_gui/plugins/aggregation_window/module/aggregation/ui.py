from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QLineEdit

from . import trigger


class ObjectInfoLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        trigger.refresh_object_info_line_edit()
