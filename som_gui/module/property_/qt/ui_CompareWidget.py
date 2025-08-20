# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CompareWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHeaderView,
    QSizePolicy,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from som_gui.module.compare.ui import EntityTreeWidget


class Ui_PropertyCompare(object):
    def setupUi(self, PropertyCompare):
        if not PropertyCompare.objectName():
            PropertyCompare.setObjectName("PropertyCompare")
        PropertyCompare.resize(868, 576)
        self.verticalLayout = QVBoxLayout(PropertyCompare)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_3 = QSplitter(PropertyCompare)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.tree_widget_class = EntityTreeWidget(self.splitter_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, "1")
        self.tree_widget_class.setHeaderItem(__qtreewidgetitem)
        self.tree_widget_class.setObjectName("tree_widget_class")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tree_widget_class.sizePolicy().hasHeightForWidth()
        )
        self.tree_widget_class.setSizePolicy(sizePolicy)
        self.splitter_3.addWidget(self.tree_widget_class)
        self.splitter_2 = QSplitter(self.splitter_3)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.tree_widget_propertysets = EntityTreeWidget(self.splitter_2)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, "1")
        self.tree_widget_propertysets.setHeaderItem(__qtreewidgetitem1)
        self.tree_widget_propertysets.setObjectName("tree_widget_propertysets")
        sizePolicy.setHeightForWidth(
            self.tree_widget_propertysets.sizePolicy().hasHeightForWidth()
        )
        self.tree_widget_propertysets.setSizePolicy(sizePolicy)
        self.splitter_2.addWidget(self.tree_widget_propertysets)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.table_widget_values = QTableWidget(self.splitter)
        self.table_widget_values.setObjectName("table_widget_values")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.table_widget_values.sizePolicy().hasHeightForWidth()
        )
        self.table_widget_values.setSizePolicy(sizePolicy1)
        self.table_widget_values.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.splitter.addWidget(self.table_widget_values)
        self.table_widget_values.horizontalHeader().setStretchLastSection(True)
        self.table_infos = QTableWidget(self.splitter)
        self.table_infos.setObjectName("table_infos")
        sizePolicy1.setHeightForWidth(self.table_infos.sizePolicy().hasHeightForWidth())
        self.table_infos.setSizePolicy(sizePolicy1)
        self.splitter.addWidget(self.table_infos)
        self.table_infos.horizontalHeader().setStretchLastSection(True)
        self.splitter_2.addWidget(self.splitter)
        self.splitter_3.addWidget(self.splitter_2)

        self.verticalLayout.addWidget(self.splitter_3)

        self.retranslateUi(PropertyCompare)

        QMetaObject.connectSlotsByName(PropertyCompare)

    # setupUi

    def retranslateUi(self, PropertyCompare):
        PropertyCompare.setWindowTitle(
            QCoreApplication.translate("PropertyCompare", "Form", None)
        )

    # retranslateUi
