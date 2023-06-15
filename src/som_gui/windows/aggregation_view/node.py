from __future__ import annotations  # make own class referencable

from PySide6.QtCore import Qt, QRectF, QPointF, QPoint, QRect
from PySide6.QtGui import QColor, QPen, QPainter, QBrush
from PySide6.QtWidgets import QPushButton, QWidget, QGraphicsScene, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsSceneMouseEvent, QGraphicsRectItem, QGraphicsSceneResizeEvent, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsTextItem,QGraphicsView

from src.som_gui.data.constants import HEADER_HEIGHT
from aggregation_window import  AggregationScene, MainView
