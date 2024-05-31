from PySide6.QtWidgets import QGraphicsView, QGraphicsScene


class AggregationView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AggregationScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
