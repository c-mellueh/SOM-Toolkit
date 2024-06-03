from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from . import trigger

class AggregationView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, event):
        super().paintEvent(event)
        trigger.view_paint_event()

class AggregationScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
