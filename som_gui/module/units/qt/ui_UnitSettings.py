# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UnitSettings.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QSizePolicy, QSplitter, QTreeView, QVBoxLayout,
    QWidget)

class Ui_UnitSettings(object):
    def setupUi(self, UnitSettings):
        if not UnitSettings.objectName():
            UnitSettings.setObjectName(u"UnitSettings")
        UnitSettings.resize(748, 592)
        self.verticalLayout_3 = QVBoxLayout(UnitSettings)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(UnitSettings)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setFrameShape(QFrame.Shape.NoFrame)
        self.splitter.setFrameShadow(QFrame.Shadow.Plain)
        self.splitter.setLineWidth(0)
        self.splitter.setMidLineWidth(0)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(5)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.unit_tree = QTreeView(self.verticalLayoutWidget)
        self.unit_tree.setObjectName(u"unit_tree")

        self.verticalLayout.addWidget(self.unit_tree)

        self.splitter.addWidget(self.verticalLayoutWidget)

        self.verticalLayout_3.addWidget(self.splitter)


        self.retranslateUi(UnitSettings)

        QMetaObject.connectSlotsByName(UnitSettings)
    # setupUi

    def retranslateUi(self, UnitSettings):
        UnitSettings.setWindowTitle(QCoreApplication.translate("UnitSettings", u"Form", None))
        self.label.setText(QCoreApplication.translate("UnitSettings", u"Units", None))
    # retranslateUi

