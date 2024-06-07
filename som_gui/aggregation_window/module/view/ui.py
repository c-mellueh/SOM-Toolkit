from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from . import trigger
from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent, QPaintEvent, QMouseEvent


class AggregationView(QGraphicsView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(trigger.context_menu_requested)
        self.setRubberBandSelectionMode(Qt.ItemSelectionMode.ContainsItemBoundingRect)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        trigger.view_paint_event()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        trigger.mouse_move_event(event.pos())

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        trigger.mouse_press_event(event.pos())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        trigger.mouse_release_event(event.pos())
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        trigger.mouse_wheel_event(event)


class AggregationScene(QGraphicsScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
