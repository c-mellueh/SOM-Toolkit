from __future__ import annotations
from PySide6.QtWidgets import QPushButton, QWidget, QTreeWidgetItem, QVBoxLayout, \
    QGraphicsProxyWidget, QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QStyleOptionGraphicsItem, \
    QGraphicsSceneHoverEvent, QTreeWidget, QGraphicsEllipseItem
from . import trigger


class NodeProxy(QGraphicsProxyWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def widget(self) -> QWidget | NodeWidget:
        return super().widget()


class NodeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.button = QPushButton(self.tr('Subelement hinzufügen'))
        self.layout().addWidget(self.button)
        self.button.hide()

    def graphicsProxyWidget(self) -> NodeProxy:
        return super(NodeWidget, self).graphicsProxyWidget()


class PropertySetTree(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemDoubleClicked.connect(trigger.pset_tree_double_clicked)


class Header(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)

    def paint(self, painter, option, widget):
        trigger.paint_header(self, painter)

    def mouseMoveEvent(self, event):
        last_pos = self.pos()
        super().mouseMoveEvent(event)
        new_pos = self.pos()
        dif = new_pos - last_pos
        trigger.drag_move(self, dif)


class Frame(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, False)
