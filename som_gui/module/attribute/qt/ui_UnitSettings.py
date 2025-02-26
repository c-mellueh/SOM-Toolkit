# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UnitSettings.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QListWidget,
    QListWidgetItem, QSizePolicy, QSplitter, QVBoxLayout,
    QWidget)

class Ui_UnitSettings(object):
    def setupUi(self, UnitSettings):
        if not UnitSettings.objectName():
            UnitSettings.setObjectName(u"UnitSettings")
        UnitSettings.resize(748, 382)
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
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.list_units = QListWidget(self.verticalLayoutWidget_2)
        self.list_units.setObjectName(u"list_units")

        self.verticalLayout_2.addWidget(self.list_units)

        self.splitter.addWidget(self.verticalLayoutWidget_2)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.list_prefixes = QListWidget(self.verticalLayoutWidget)
        self.list_prefixes.setObjectName(u"list_prefixes")
        self.list_prefixes.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.list_prefixes)

        self.splitter.addWidget(self.verticalLayoutWidget)

        self.verticalLayout_3.addWidget(self.splitter)


        self.retranslateUi(UnitSettings)

        QMetaObject.connectSlotsByName(UnitSettings)
    # setupUi

    def retranslateUi(self, UnitSettings):
        UnitSettings.setWindowTitle(QCoreApplication.translate("UnitSettings", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("UnitSettings", u"Units", None))
        self.label_2.setText(QCoreApplication.translate("UnitSettings", u"Unit Prefixes", None))
    # retranslateUi

