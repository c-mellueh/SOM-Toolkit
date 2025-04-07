from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from . import ui

from PySide6.QtCore import (
    QAbstractItemModel,
    QAbstractTableModel,
    QCoreApplication,
    QItemSelectionModel,
    QModelIndex,
    Qt,
    Signal,
    QSize,
    QRect,
    QPoint,
)
from PySide6.QtGui import QMouseEvent, QColor, QPainter, QPalette, QBrush
from PySide6.QtWidgets import (
    QLineEdit,
    QTreeView,
    QWidget,
    QHeaderView,
    QStyleOptionHeader,
    QStyle,
)
import SOMcreator
import som_gui
from som_gui import tool
from . import trigger


class CustomHeaderView(QHeaderView):
    sectionPressed = Signal(int, int)

    def __init__(self, first_columns: list[str], parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.first_columns = first_columns
        self.sectionResized.connect(self.onSectionResized)

    @property
    def column_overlap(self):
        return len(self.first_columns)

    def parentWidget(self) -> ui.FilterTreeView:
        return super().parentWidget()

    def setModel(self, model):
        super().setModel(model)

    def setCellLabel(self, row: int, column: int, label: str):
        self.model().setData(
            self.model().index(row, column), label, Qt.ItemDataRole.DisplayRole
        )

    def setCellBackgroundColor(self, row: int, column: int, color: QColor):
        self.model().setData(
            self.model().index(row, column), color, Qt.ItemDataRole.BackgroundRole
        )

    def setCellForegroundColor(self, row: int, column: int, color: QColor):
        self.model().setData(
            self.model().index(row, column), color, Qt.ItemDataRole.ForegroundRole
        )

    def indexAt(self, pos: QPoint):
        tblModel = self.model()
        rows = tblModel.rowCount()
        cols = tblModel.columnCount()
        logicalIdx = self.logicalIndexAt(pos)
        delta = 0
        if self.orientation() == Qt.Orientation.Horizontal:
            for row in range(rows):
                cellIndex = tblModel.index(row, logicalIdx)
                delta += cellIndex.data(Qt.ItemDataRole.SizeHintRole).height()
                if pos.y() <= delta:
                    return cellIndex
        else:
            for col in range(cols):
                cellIndex = tblModel.index(logicalIdx, col)
                delta += cellIndex.data(Qt.ItemDataRole.SizeHintRole).width()
                if pos.x() <= delta:
                    return cellIndex
        return QModelIndex()

    def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int):
        logging.debug(f"Paint Section {logicalIndex}")
        tblModel: CustomHeaderModel = self.model()
        for i in range(tblModel.rowCount()):
            cellIndex = tblModel.index(i, logicalIndex)
            cellSize: QSize = cellIndex.data(Qt.ItemDataRole.SizeHintRole)
            sectionRect = QRect(rect)

            sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, i))
            sectionRect.setSize(cellSize)

            colSpanIdx: QModelIndex = self.columnSpanIndex(cellIndex)
            rowSpanIdx: QModelIndex = self.rowSpanIndex(cellIndex)
            if colSpanIdx.isValid():
                colSpanFrom: int = colSpanIdx.column()
                colSpanCnt = colSpanIdx.data(CustomHeaderModel.ColumnSpanRole)
                colSpanTo = colSpanFrom + colSpanCnt - 1
                colSpan = self.columnSpanSize(cellIndex.row(), colSpanFrom, colSpanCnt)
                sectionRect.setLeft(self.sectionViewportPosition(colSpanFrom))
                sectionRect.setWidth(colSpan)
                subRowSpanData = colSpanIdx.data(CustomHeaderModel.RowSpanRole)
                if subRowSpanData is not None:
                    subRowSpanFrom = colSpanIdx.row()
                    subRowSpanCnt = int(subRowSpanData)
                    subRowSpanTo = subRowSpanFrom + subRowSpanCnt - 1
                    subRowSpan = self.rowSpanSize(
                        colSpanFrom, subRowSpanFrom, subRowSpanCnt
                    )
                    sectionRect.setTop(self.rowSpanSize(colSpanFrom, 0, subRowSpanFrom))
                    i = subRowSpanTo
                    sectionRect.setHeight(subRowSpan)
                cellIndex = colSpanIdx

            if rowSpanIdx.isValid():
                rowSpanFrom = rowSpanIdx.row()
                rowSpanCnt = int(rowSpanIdx.data(CustomHeaderModel.RowSpanRole))
                rowSpanTo = rowSpanFrom + rowSpanCnt - 1
                rowSpan = self.rowSpanSize(cellIndex.column(), rowSpanFrom, rowSpanCnt)
                sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, rowSpanFrom))
                i = rowSpanTo

                sectionRect.setHeight(rowSpan)

                # check up if the row span index has column span
                subColSpanData = rowSpanIdx.data(CustomHeaderModel.ColumnSpanRole)
                if subColSpanData is not None:
                    subColSpanFrom = rowSpanIdx.column()
                    subColSpanCnt = int(subColSpanData)
                    subColSpanTo = subColSpanFrom + subColSpanCnt - 1
                    subColSpan = self.columnSpanSize(
                        rowSpanFrom, subColSpanFrom, subColSpanCnt
                    )
                    sectionRect.setLeft(self.sectionViewportPosition(subColSpanFrom))

                    sectionRect.setWidth(subColSpan)
                cellIndex = rowSpanIdx

            opt = QStyleOptionHeader()
            self.initStyleOption(opt)
            opt.textAlignment = Qt.AlignmentFlag.AlignCenter
            opt.section = logicalIndex
            opt.text = cellIndex.data(Qt.ItemDataRole.DisplayRole)
            opt.rect = sectionRect
            painter.save()
            self.style().drawControl(QStyle.CE_Header, opt, painter, self)
            painter.restore()

    def sectionSizeFromContents(self, logicalIndex: int):
        tblModel = self.model()
        level = tblModel.rowCount()

        size = super().sectionSizeFromContents(logicalIndex)
        height = 0
        if logicalIndex >= self.model().columnCount():
            return QSize()
        for i in range(level):
            cellIndex = tblModel.index(i, logicalIndex)
            colSpanIdx: QModelIndex = self.columnSpanIndex(cellIndex)
            size: QSize = cellIndex.data(Qt.ItemDataRole.SizeHintRole)

            if colSpanIdx.isValid():
                colSpanFrom = colSpanIdx.column()
                colSpanCnt = int(colSpanIdx.data(CustomHeaderModel.ColumnSpanRole))
                colSpanTo = colSpanFrom + colSpanCnt - 1
                size.setWidth(
                    self.columnSpanSize(colSpanIdx.row(), colSpanFrom, colSpanCnt)
                )
            height += cellIndex.data(Qt.ItemDataRole.SizeHintRole).height()
        size.setHeight(height)
        return size

    def setRowHeight(self, row: int, height: int):
        m = self.model()
        cols = m.columnCount()
        for col in range(cols):
            sz: QSize = m.index(row, col).data(Qt.ItemDataRole.SizeHintRole)
            sz.setHeight(height)
            m.setData(m.index(row, col), sz, Qt.ItemDataRole.SizeHintRole)

    def model(self) -> CustomHeaderModel:
        return super().model()

    def setColumnWidth(self, col: int, width: int):
        m = self.model()
        rows = m.rowCount()
        for row in range(rows):
            sz: QSize = m.index(row, col).data(Qt.ItemDataRole.SizeHintRole)
            sz.setWidth(width)
            m.setData(m.index(row, col), sz, Qt.ItemDataRole.SizeHintRole)
        self.resizeSection(col, width)

    def setSpan(
        self,
        row: int,
        column: int,
        rowSpanCount: int = None,
        columnSpanCount: int = None,
    ):
        md = self.model()
        if rowSpanCount is None:
            rowSpanCount = md.rowCount()
        if columnSpanCount is None:
            columnSpanCount = 1
        idx = md.index(row, column)
        if rowSpanCount > 0:
            md.setData(idx, rowSpanCount, CustomHeaderModel.RowSpanRole)
        if columnSpanCount > 0:
            md.setData(idx, columnSpanCount, CustomHeaderModel.ColumnSpanRole)

    def columnSpanIndex(self, index: QModelIndex) -> QModelIndex:
        tblModel = self.model()
        curRow = index.row()
        curCol = index.column()
        i = curCol
        while i >= 0:
            spanIndex = tblModel.index(curRow, i)
            span = spanIndex.data(CustomHeaderModel.ColumnSpanRole)
            if span is not None and spanIndex.column() + int(span) - 1 >= curCol:
                return spanIndex
            i -= 1
        return QModelIndex()

    def rowSpanIndex(self, index: QModelIndex) -> QModelIndex:
        tblModel = self.model()
        curRow = index.row()
        curCol = index.column()
        i = curRow
        while i >= 0:
            spanIndex = tblModel.index(i, curCol)
            span = spanIndex.data(CustomHeaderModel.RowSpanRole)
            if span is not None and spanIndex.row() + int(span) - 1 >= curRow:
                return spanIndex
            i -= 1
        return QModelIndex()

    def columnSpanSize(self, row: int, from_: int, spanCount: int) -> int:
        tblModel = self.model()
        span = 0
        for i in range(from_, from_ + spanCount):
            cellSize = tblModel.index(row, i).data(Qt.ItemDataRole.SizeHintRole)
            span += self.get_tree_column_width(i)
        return span

    def rowSpanSize(self, column, from_, spanCount) -> int:
        tblModel = self.model()
        span = 0
        for i in range(from_, from_ + spanCount):
            cellSize = tblModel.index(i, column).data(Qt.ItemDataRole.SizeHintRole)
            span += cellSize.height()
        return span

    def getSectionRange(self, index: QModelIndex, beginSection: int, endSection: int):
        # TODO fix output of beginSection and endSection
        colSpanIdx = self.columnSpanIndex(index)
        rowSpanIdx = self.rowSpanIndex(index)
        if colSpanIdx.isValid():
            colSpanFrom = colSpanIdx.column()
            colSpanCnt = int(colSpanIdx.data(CustomHeaderModel.ColumnSpanRole))

            colSpanTo = colSpanFrom + colSpanCnt - 1
            if self.orientation() == Qt.Orientation.Horizontal:
                beginSection = colSpanFrom
                endSection = colSpanTo
                index = colSpanIdx
                return colSpanCnt, beginSection, endSection
            else:
                subRowSpanData = colSpanIdx.data(CustomHeaderModel.RowSpanRole)
                if subRowSpanData is not None:
                    subRowSpanFrom = colSpanIdx.row()
                    subRowSpanCnt = int(subRowSpanData)
                    subRowSpanTo = subRowSpanFrom + subRowSpanCnt - 1
                    beginSection = subRowSpanFrom
                    endSection = subRowSpanTo
                    index = colSpanIdx
                    return subRowSpanCnt, beginSection, endSection
        if rowSpanIdx.isValid():
            rowSpanFrom = rowSpanIdx.row()
            rowSpanCnt = int(rowSpanIdx.data(CustomHeaderModel.RowSpanRole))
            rowSpanTo = rowSpanFrom + rowSpanCnt - 1
            subColSpanData = rowSpanIdx.data(CustomHeaderModel.ColumnSpanRole)
            if subColSpanData is not None:
                subColSpanFrom = rowSpanIdx.column()
                subColSpanCnt = int(subColSpanData)
                subColSpanTo = subColSpanFrom + subColSpanCnt - 1
                beginSection = subColSpanFrom
                endSection = subColSpanTo
                index = rowSpanIdx
                return subColSpanCnt, beginSection, endSection
        return 0, beginSection, endSection

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        index = self.indexAt(event.pos())
        if index.isValid():
            beginSection = index.column()
            endSection = beginSection
            result, beginSection, endSection = self.getSectionRange(
                index, beginSection, endSection
            )
            if result > 0:
                self.sectionPressed.emit(beginSection, endSection)
            else:
                self.sectionPressed.emit(beginSection, endSection)

    def onSectionResized(self, logicalIndex: int, oldSize: int, newSize: int):
        tblModel: CustomHeaderModel = self.model()
        level = tblModel.rowCount()
        pos = self.sectionViewportPosition(logicalIndex)
        xx = pos
        yy = 0
        sectionRect = QRect(xx, yy, 0, 0)
        for i in range(level):
            cellIndex = tblModel.index(i, logicalIndex)
            cellSize: QSize = cellIndex.data(Qt.ItemDataRole.SizeHintRole)
            sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, i))
            cellSize.setWidth(newSize)

            tblModel.setData(cellIndex, cellSize, Qt.ItemDataRole.SizeHintRole)
            colSpanIdx = self.columnSpanIndex(cellIndex)
            rowSpanIdx = self.rowSpanIndex(cellIndex)
            if colSpanIdx.isValid():
                colSpanFrom = colSpanIdx.column()
                sectionRect.setLeft(self.sectionViewportPosition(colSpanFrom))

            if rowSpanIdx.isValid():
                rowSpanFrom = rowSpanIdx.row()
                sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, rowSpanFrom))
            rToUpdate = QRect(sectionRect)
            rToUpdate.setWidth(self.viewport().width() - sectionRect.left())
            rToUpdate.setHeight(self.viewport().height() - sectionRect.top())
            self.viewport().update(rToUpdate.normalized())

    def get_tree_column_width(self, logicalIndex: int):
        parent: ui.FilterTreeView = self.parent()
        return parent.columnWidth(logicalIndex)


class CustomHeaderModel(QAbstractTableModel):
    ColumnSpanRole = Qt.ItemDataRole.UserRole + 1
    RowSpanRole = Qt.ItemDataRole.UserRole + 2

    def __init__(
        self, proj: SOMcreator.SOMProject, first_columns: list[str], parent=None
    ):
        super().__init__(parent)
        self.first_columns = first_columns
        self.proj = proj
        self.data_dict = dict()
        self.size_hint_dict = dict()

    @property
    def column_overlap(self):
        return len(self.first_columns)

    def get_active_phases(self, usecase: SOMcreator.UseCase):
        phases = self.proj.get_phases()
        return [phase for phase in phases if self.proj.get_filter_state(phase, usecase)]

    def get_usecase_matrix(self):
        matrix = list()
        for usecase in self.proj.get_usecases():
            active_phases = self.get_active_phases(usecase)
            if active_phases:
                matrix.append((usecase, active_phases))
        return matrix

    def get_usecase_by_column(self, column: int):
        column -= self.column_overlap
        matrix = self.get_usecase_matrix()
        for use_case, phase_list in matrix:
            column -= len(phase_list)
            if column < 0:
                return use_case

    def get_phase_by_column(self, column: int):
        column -= self.column_overlap
        matrix = self.get_usecase_matrix()
        for use_case, phase_list in matrix:
            if 0 <= column < len(phase_list):
                return phase_list[column]
            column -= len(phase_list)

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()):
        if column < self.column_overlap:
            return self.createIndex(row, column, None)
        if row == 0:
            return self.createIndex(row, column, self.get_usecase_by_column(column))
        if row == 1:
            return self.createIndex(row, column, self.get_phase_by_column(column))
        return self.createIndex(row, column, None)

    def rowCount(self, parent=None):
        return 2

    def columnCount(self, parent=None):
        matrix = self.get_usecase_matrix()
        return sum(len(p) for (u, p) in matrix) + self.column_overlap

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return super().flags(index)

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        if (
            index.row() >= self.rowCount()
            or index.row() < 0
            or index.column() >= self.columnCount()
            or index.column() < 0
        ):
            return None
        if role == Qt.ItemDataRole.SizeHintRole:
            sh = self.size_hint_dict.get((index.row(), index.column()))
            if not sh:
                baseSectionSize = QSize()
                baseSectionSize.setWidth(50)
                baseSectionSize.setHeight(20)
                self.setData(index, Qt.ItemDataRole.SizeHintRole, baseSectionSize)
                return baseSectionSize
            return self.size_hint_dict[(index.row(), index.column())]

        if index.column() < self.column_overlap:
            if role == self.ColumnSpanRole:
                return 1
            if role == self.RowSpanRole and index.row() == 0:
                return 2
            if role == Qt.ItemDataRole.DisplayRole:
                return self.first_columns[index.column()]
            return None

        item: SOMcreator.UseCase | SOMcreator.Phase = index.internalPointer()
        sibling = index.siblingAtColumn(index.column() - 1) or QModelIndex()
        if role == self.ColumnSpanRole:
            if sibling.internalPointer() == item:
                return None
            if index.row() == 1:
                return 1
            else:
                return len(self.get_active_phases(item))
        if role == self.RowSpanRole:
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return str(item.name)

        if not self.data_dict.get(item):
            self.data_dict[item] = dict()
        return self.data_dict[item].get(role)

    def setData(self, index: QModelIndex, value, role):
        if index is not None:
            item: SOMcreator.UseCase | SOMcreator.Phase = index.internalPointer()
            if role == self.ColumnSpanRole:
                pass
            if role == Qt.ItemDataRole.SizeHintRole:
                self.size_hint_dict[(index.row(), index.column())] = value
            else:
                if not self.data_dict.get(item):
                    self.data_dict[item] = dict()
                self.data_dict[item][role] = value
            return True
        return False
