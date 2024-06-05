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
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(trigger.context_menu_requested)
        self.setRubberBandSelectionMode(Qt.ItemSelectionMode.ContainsItemBoundingRect)
        self.rubberBandChanged.connect(trigger.rubber_band_changed)

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.view_paint_event()

    def mouseMoveEvent(self, event):
        trigger.mouse_move_event(event.pos())

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        trigger.mouse_press_event(event.pos())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        trigger.mouse_release_event(event.pos())
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        # super().wheelEvent(event)
        trigger.mouse_wheel_event(event)
class AggregationScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
