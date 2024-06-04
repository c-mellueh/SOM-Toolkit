from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from . import trigger
from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent

class AggregationView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.view_paint_event()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        trigger.mouse_move_event(event.pos())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        trigger.mouse_press_event(event.pos())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        trigger.mouse_release_event()

    def wheelEvent(self, event: QWheelEvent):
        # super().wheelEvent(event)
        trigger.mouse_wheel_event(event)
class AggregationScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
