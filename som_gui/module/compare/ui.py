from PySide6.QtWidgets import QDialog, QHeaderView, QWidget, QTreeWidget
from . import window, import_window, attribute_widget, trigger
from som_gui.icons import get_icon, ICON_PATH, ICON_DICT, get_switch
from PySide6.QtGui import QIcon, QPalette, QPixmap, QTransform
from PySide6.QtCore import QModelIndex, Qt, QRect, QSize
import os


class CompareDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr("Projekte Vergleichen"))
        self.widget.tabWidget.setTabText(0, self.tr("Attribute"))


class AttributeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = attribute_widget.Ui_Form()
        self.widget.setupUi(self)
        self.widget.tree_widget_object.setColumnCount(2)
        self.widget.tree_widget_propertysets.setColumnCount(2)
        self.widget.table_widget_values.setColumnCount(2)


class ProjectSelectDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = import_window.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle(self.tr("Projekte Vergleichen"))
        self.widget.button_switch.setText("")
        pixmap = QPixmap(os.path.join(ICON_PATH, ICON_DICT["switch"]))
        icon = QIcon(pixmap.transformed(QTransform().rotate(90), Qt.TransformationMode.FastTransformation))
        icon = get_switch()
        self.widget.button_switch.setIcon(icon)


class WordWrapHeaderView(QHeaderView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sectionSizeFromContents(self, logicalIndex):
        text = str(self.model().headerData(logicalIndex, self.orientation(), Qt.ItemDataRole.DisplayRole))
        max_width = self.sectionSize(logicalIndex)
        print(max_width)
        maxheight = 5000
        alignement = self.defaultAlignment()
        metrics = self.fontMetrics()
        rect = metrics.boundingRect(QRect(0, 0, max_width, maxheight), alignement, text)
        text_margin_buffer = QSize(2, 2)
        return rect.size() + text_margin_buffer


class EntityTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def drawBranches(self, painter, rect, index: QModelIndex):
        results = trigger.draw_branches(self, painter, rect, index)
        super().drawBranches(*results)
