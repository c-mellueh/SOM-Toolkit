# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MappingWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
    QFrame,
    QGridLayout,
    QHeaderView,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableView,
    QWidget,
)


class Ui_MappingWidget(object):
    def setupUi(self, MappingWidget):
        if not MappingWidget.objectName():
            MappingWidget.setObjectName("MappingWidget")
        MappingWidget.resize(660, 131)
        MappingWidget.setFrameShape(QFrame.Shape.Box)
        MappingWidget.setFrameShadow(QFrame.Shadow.Sunken)
        MappingWidget.setLineWidth(1)
        MappingWidget.setMidLineWidth(0)
        self.gridLayout = QGridLayout(MappingWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.table_view = QTableView(MappingWidget)
        self.table_view.setObjectName("table_view")
        self.table_view.setFrameShape(QFrame.Shape.NoFrame)
        self.table_view.setFrameShadow(QFrame.Shadow.Plain)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.verticalHeader().setCascadingSectionResizes(True)

        self.gridLayout.addWidget(self.table_view, 3, 0, 1, 2)

        self.button_add_ifc = QPushButton(MappingWidget)
        self.button_add_ifc.setObjectName("button_add_ifc")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.button_add_ifc.sizePolicy().hasHeightForWidth()
        )
        self.button_add_ifc.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.button_add_ifc, 4, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 4, 0, 1, 1)

        self.retranslateUi(MappingWidget)

        QMetaObject.connectSlotsByName(MappingWidget)

    # setupUi

    def retranslateUi(self, MappingWidget):
        MappingWidget.setWindowTitle(
            QCoreApplication.translate("MappingWidget", "Form", None)
        )
        self.button_add_ifc.setText(
            QCoreApplication.translate("MappingWidget", "+", None)
        )

    # retranslateUi
